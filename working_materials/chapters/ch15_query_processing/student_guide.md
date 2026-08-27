# Chapter 15: Query Processing

SQL說明要取得什麼結果，DBMS仍必須決定如何取得。Query processing包含把SQL轉成內部
表示、選擇可執行plan，並由execution engine執行operators。本章學習讀plan中的access
與join工作，不要求背完整sorting、join演算法或I/O公式。

搭配檔案：`student_lab.sql`。

Ch15與Ch16共同授課。Ch15的課堂核心是logical/physical plan、scan、index
search、join order及query-plan evidence。Parsing/translation只作流程銜接；
materialization、pipelining及完整join algorithms留作課後延伸。

## 與前章及下一章的關係

Ch14建立indexes作access paths。Ch15說明scan、selection、join等physical operations
如何組成query plan；Ch16再解釋optimizer如何用equivalence與statistics在多個valid
plans中選擇一個。Plan沒使用某個index不表示index損壞，可能是cost decision。

## 學習目標

完成本章後，你應能：

1. 概述parsing/translation、optimization及evaluation之間的關係。
2. 區分logical relational operation、physical operator及query-execution plan。
3. 讀出plan中的table scan、index search、join order及temporary work。
4. 比較file scan與index scan適用條件，不宣稱index必然較快。
5. 以小型例子比較nested-loop與indexed inner lookup概念。
6. 以input size、matching rows、I/O、CPU、memory及intermediate results解釋cost。
7. 用相同SQL結果與plan evidence比較兩個physical designs。

## 1. Query-processing steps

典型流程有三個主要steps：

1. Parsing and translation：檢查SQL syntax、relation/column names及permissions等，並轉成
   internal representation，常以extended relational algebra或annotated tree表示。
2. Optimization：找出多個equivalent choices，估計各plan cost，選擇一個execution plan。
3. Evaluation：execution engine依plan執行operators並產生query result。

各DBMS內部表示不一定完全相同，但這三種工作提供共同理解方式。

### Worked example

```sql
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';
```

Parser確認table與columns存在，translation建立selection加projection的logical
expression。Optimizer可在linear table scan與title index search間選擇。Evaluation依最終
plan讀取row並只輸出兩個columns。SQL文字沒有指定「一定用B+ tree」。

### 你來判斷

若把`course_idd`拼錯，錯誤主要在哪個step被發現？若SQL合法但planner選了table scan，
哪個step作出選擇？最後真正讀取pages是哪個step？

### 檢查方式

依序是parsing/translation、optimization、evaluation。不能把syntax error說成index問題。

## 2. Logical expression, operator, and plan

Logical relational algebra說明selection、projection、join等結果關係；physical operator說明
如何執行，例如linear scan或index search。Query-execution plan把operators、access paths、
join order及資料流組成可執行tree。

### Worked example

同一logical selection `title = 'Course 04999'`可有兩個physical plans：

```text
Plan A: SCAN ch15_course -> test title on every row -> project two columns
Plan B: SEARCH ch15_course USING title index -> fetch matching row -> project
```

兩者必須回相同result。若Plan B在目前data中讀較少entries，這是physical difference，
不是另一個SQL meaning。

### 你來操作

先預測`student_lab.sql` Phase 1與Phase 2的selection plan，再執行並圈出`SCAN`、
`SEARCH`、index name及covered predicate。

### 預期與回饋

在已驗證SQLite 3.45.3中，Phase 1是table scan；建立title index後是index search。若版本
不同，保留完整plan及version再分析，不強行改成預期字串。

## 3. Query cost means estimated resources

Optimizer通常比較estimated total resource consumption，而不是準確預測wall-clock time。
可能納入storage reads/writes、random與sequential access、CPU operations、available memory，
以及distributed systems中的communication。Estimated rows會影響每項成本。

Elapsed time也受cache、其他users、storage及OS狀態影響。相同plan第二次執行可能因pages已
在memory而更快；因此單次時間不等於演算法或index的普遍證明。

### Worked example

Course有5,000 rows，title只match 1 row。Plan A要檢查所有5,000 rows；Plan B先走index
再取1 row，通常有較低work estimate。若predicate match 4,500 rows而每筆仍需回table，
secondary index造成的many lookups可能比sequential scan更貴，optimizer可合理選scan。

### 你來判斷

兩個plans實測分別為8 ms與11 ms，但第二次變成4 ms與3 ms。列出至少三個在宣布「Plan
A較快」前要控制或記錄的因素。

### 回饋重點

可包含cache state、row counts、statistics、concurrent load、DBMS/version、repeated runs、
plan是否相同。只重跑直到得到想要的數字不算有效比較。

## 4. Selection: file scan and index scan

Linear/file scan逐blocks讀relation並測試predicate，可套用任何file與一般condition。Index
scan/search以predicate導引access path，適合能由index定位且預期取回較少records的情況。
若大量matching records散落在不同pages，secondary index不一定勝過scan。

### Worked example

在lab中：

```sql
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';
```

無title index時，SQLite顯示`SCAN ch15_course`。建立
`ch15_idx_course_title(title)`及`ANALYZE`後，plan顯示`SEARCH ... title=?`。Result仍是
`C04999, Course 04999`。

另一個predicate `credits = 3`約match五分之一rows。即使建立credits index，也不能只靠
「有index」宣稱它較快；要看projection、matching pages及optimizer estimate。

### 你來操作

執行兩個phases並保留plan。再對`credits=3`先算matching rows比例，提出scan或index的
假設，但不新增index；說明還需要哪個plan evidence。

### 檢查方式

Title plan應從SCAN變成SEARCH且結果不變。Credits共有1,000/5,000 rows；答案必須把它
視為需要optimizer及實測判斷，而不是直接指定index。

## 5. Join processing

Join需要產生符合join condition的row pairs。最簡單的nested-loop概念是：對outer relation
的每個tuple，在inner relation找matching tuples。沒有index時可能反覆scan；若inner join
attribute有index，可對每個outer tuple做index lookup，形成indexed nested-loop join。

實際DBMS也可能用block nested-loop、merge join或hash join。這些方法在本課只作選擇概念：
merge join利用sorted equi-join inputs；hash join以equality join keys分組。完整演算法與cost
公式不列入主要教學。

### Worked example: without useful join indexes

```sql
SELECT c.course_id, c.title
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042';
```

Phase 1沒有department-name及course-department secondary indexes，且關閉SQLite automatic
indexes。Planner必須scan其中一側，再用可用的primary-key lookup或另一個scan檢查join。
重點是讀出哪一個operator在外層、每找到一列後如何存取另一表。

### Worked example: indexed inner lookup

Phase 2建立：

```sql
CREATE UNIQUE INDEX ch15_idx_department_name
ON ch15_department(dept_name);

CREATE INDEX ch15_idx_course_dept
ON ch15_course(dept_id);
```

Plan先以department name找唯一department，再以該`dept_id`搜尋course index。這可視為很小
outer result驅動inner index lookup；結果為該department的50門courses。

### 你來操作

讀取Phase 1與Phase 2 join plans，依plan輸出順序寫出outer與inner access。若移除
`WHERE dept_name=...`而要列出全校所有courses，你是否仍能宣稱相同join order最佳？

### 預期與回饋

建立indexes後應有兩個SEARCH operators，先department name，再course dept ID。移除
selective filter後outer size改變，原結論不能直接沿用；需新statistics與plan。

## 6. Join-order and cardinality reasoning

Join order影響每個operator收到多少rows。先執行selective condition通常可以縮小後續work，
但「通常」仍需要statistics支持；estimated cardinality若錯，optimizer可能選到成本較高的
plan。

### Worked example

Department name是unique，因此filter預期1 row；再查course dept index約回50 rows。若先
掃5,000 course rows再逐一檢查department，雖結果相同，處理的candidates較多。這是本
lab可由row counts及plan支持的比較。

### 你來判斷

把condition改為`credits=3`後約有1,000 courses。比較先filter course再joindepartment，與
先讀all departments再找courses；列出決定優劣還需要的index及distribution資訊。

### 回饋重點

必須提到credits index是否存在、每department課程分布、matching rows及join access path。
「小表永遠放外層」不是不帶條件的規則。

## 7. Materialization and pipelining（課後延伸）

Materialized evaluation把intermediate result存成temporary relation，再由next operator讀取。
Pipelined evaluation在上游產生tuple時直接交給下游，可能減少temporary I/O並較早輸出
結果。但sorting等blocking operation通常要先看到全部或大量input才能按順序輸出。

### Worked example

對「filter Department 042 -> join Course -> project title」：

- Materialized：先存department filter result，再join並存join result，最後project。
- Pipelined：filter找到department row後立即驅動course lookup；每個matching course立即只
  輸出title，不必先保存完整50-row join result。

SQLite的compact `EXPLAIN QUERY PLAN`不直接證明每條edge是否pipelined，因此這一段是
教科書概念，不從lab plan自行推定internal buffering。

### 你來判斷

為結果加入`ORDER BY c.title`，若現有access path不能提供title order，哪一步可能需要先
收集rows？在plan看到temporary B-tree時可支持什麼結論？

### 檢查方式

Sort可能是blocking並需要temporary work。Plan可支持「此plan另做sort」，不能單獨給出
所有memory/disk細節或實際temporary bytes。

## 課堂比較與個人學習證據

各組收到同一SQL及兩份匿名plans，先回答result是否等價，再以access method、estimated
input/output rows、join order、index及temporary work比較。教師最後依plan可觀察證據
回饋，學生修正一項過度推論。

個人保存：SQL、schema/data counts、before/after plans、result equality check、plan逐行
說明，以及一項「plan未提供的資訊」。

## 常見錯誤

1. 把SQL execution順序直接等同於SQL文字的書寫順序。
2. 認為logical join只有一個physical algorithm。
3. 看到index存在就宣稱planner一定使用。
4. 只比較elapsed time，沒有確認results及plans相同。
5. 把estimated cost或rows當成actual measurement。
6. 從SQLite plan名稱推定其他DBMS必然相同。
7. 看到nested loops就直接說慢，沒有看outer rows與inner index。

## 本章總結

Query processing把logical request轉成physical plan。Scan、index search及join access各有
適用條件，cost取決於rows、storage、CPU、memory及intermediate work。可靠判讀先確認
result equivalence，再讀plan與data evidence，最後才比較performance。Ch16將處理
equivalent expressions、statistics及optimizer選擇。

## 課後接續

- 對自己的兩條queries保留schema、row counts、plan及result check。
- 補充閱讀external sorting、完整block/merge/hash joins與I/O cost formulas；這些不是本課
  selected Ch15考試推導範圍。
