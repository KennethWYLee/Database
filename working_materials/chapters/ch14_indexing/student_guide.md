# Chapter 14: Indexing

Logical design回答facts及constraints如何表示；index屬於physical design，讓DBMS在不
改變query result的前提下，用不同access path尋找資料。本章不以「每個column都加
index」為目標，而是根據query、data distribution與update workload提出可驗證的選擇。

搭配檔案：`student_lab.sql`及`bplus_tree_example.png`。

課堂核心是index使用時機、B+ tree equality/range lookup、複合索引欄位順序、
covering index，以及建立index前後的query-plan evidence。Dense/sparse、
clustering/secondary、leaf split及hashing用來建立概念，不列為完整操作要求。

## 與前章的關係

Ch7先消除不必要的redundancy。Index通常不修正update、insertion或deletion anomaly；
它加速對既有schema的特定access patterns。Ch15-Ch16會再把index放進query plan及
optimizer選擇中判讀。

## 先備知識

- primary/candidate/foreign key與Ch7的logical design；
- selection、range condition、join及`ORDER BY`；
- `CREATE TABLE`、`CREATE INDEX`及basic aggregate queries。

## 學習目標

完成本章後，你應能：

1. 區分search key與primary/candidate key。
2. 以access type、access/update cost及space比較index選擇。
3. 以概念圖解釋ordered index中的clustering/secondary及dense/sparse差異。
4. 逐步追蹤B+ tree的equality lookup與range scan。
5. 說明B+ tree為何保持balanced，以及linked leaves如何支援range query。
6. 概念比較ordered index與hash index適用的query。
7. 依lexicographic order判斷composite index可支援的leading predicates。
8. 解釋covering index及額外storage/update cost。
9. 使用`CREATE INDEX`、`DROP INDEX`與`EXPLAIN QUERY PLAN`檢查實際access path。
10. 根據workload提出index，並清楚限制證據能支持的結論。

## 1. Index與search key

Index是額外的data structure，保存search-key values與records或record locations之間的
連結。Search key是用來lookup的一個或多個attributes，不必unique，也不等於primary
key。Primary key是logical constraint；index是physical access structure。多數DBMS會
為primary key建立index，但兩個概念仍不能互換。

### Worked example

`Enrollment(student_id, course_id, grade)`的primary key是
`(student_id, course_id)`。若常查「某個grade的所有enrollments」，可以建立以grade為
search key的index；grade顯然不是candidate key，因多列可以同為A。

查`student_id='S101'`可能只回少量rows；index可先定位對應entries，不必逐列檢查整張
table。但每次insert、delete或修改indexed value時，也要維護index。

### 你來判斷

對`Course(course_id, title, dept_code)`，分別說明`course_id`作primary key及
`dept_code`作index search key代表什麼。哪一項允許duplicates？

### 檢查方式

Course ID負責uniqueness及row identity；department code index負責lookup，允許同系多門
課。若答案說「有index所以dept_code一定unique」，混淆了constraint與access path。

## 2. Index evaluation與workload

沒有一種index對所有工作都最好。至少要比較：

- access types：equality、range、prefix、ordering或join；
- access time及預期rows；
- insertion、deletion及indexed-value update成本；
- index的space overhead；
- query與update的頻率，而不只看一條query。

### Worked example

選課系統每分鐘有數百次「查一位student的所有選課」，每天批次匯入一次新選課。對
`Enrollment(student_id, course_id, grade)`建立`student_id` index有明確理由：高頻
equality lookup通常只取少量rows，而index maintenance相對低頻。

若另一個report每學期只執行一次、會讀取全體學生，專為它增加多個index可能得不償失。
這不是以「一天一次」直接判定，而是要求測量query benefit、storage與持續update cost。

### 你來操作

比較兩個workloads：(A) 95% lookup by student ID、5% inserts；(B) 5% lookup、95%
grade updates。提出是否建立grade index，並列出仍需取得的data distribution或plan證據。

### 回饋重點

答案必須同時提到matching row數、query frequency及maintenance；不能只說「index會快」。

## 3. Ordered indices: clustering, secondary, dense, sparse（概念延伸）

Ordered index把search-key values依序保存。若資料records本身也按相同search key順序存放，
它是clustering index；不同順序的index是secondary/nonclustering index。一個file無法同時
按多個互不相同的orders實體排列。

Dense index對每個search-key value有entry。Sparse index只為部分values設entry，必須在
records按相同search key排列時才能由最近的entry接續sequential scan；因此secondary
index必須dense，否則未列出的value可能散落在file任何位置。

### Worked example

資料依ID分成三個blocks：

```text
B1: 101, 105       B2: 110, 120       B3: 130, 145
```

Dense index有`101,105,110,120,130,145`六個entries。每block一個entry的sparse index有
`101->B1, 110->B2, 130->B3`。找120時，dense index直接定位120；sparse index先找不大於
120的最大entry 110，再掃描B2找到120。Sparse版本較小、更新較少，但需要block內掃描。

若records實際按ID排列，對department建立sparse secondary index便不可靠：沒有entry的
department records不一定緊接在某個已知位置之後。

### 你來操作

使用上述blocks找125。分別寫出dense與sparse查找何時知道「不存在」。再回答若B2插入
最小值108，哪個sparse entry必須更新。

### 預期與回饋

Sparse查找從110進入B2，掃到下一個130或block界線後判定不存在；B2 entry由110改為108。
答案須包含entry選擇及後續scan，不只寫binary search。

## 4. B+ tree structure

B+ tree是balanced multilevel ordered index。Internal nodes保存separator keys與child
pointers；leaf nodes保存search-key entries與record references，並依key order連接到下一個
leaf。所有root-to-leaf paths長度相同。DBMS通常讓一個node接近storage page大小，因此
fanout高、tree相對矮。

![Original B+ tree example](bplus_tree_example.png)

圖中每個leaf最多3個keys。Root的40、70把搜尋範圍分成三個children；leaf arrows保存
排序後的sequential path。圖是教學簡化，不代表SQLite公開其內部page layout。

### Worked example: equality lookup

找50時：

1. Root比較50與40、70，選擇`40 <= key < 70`的middle child。
2. Middle leaf依序比較40、50、60。
3. 找到50的entry，再依record reference取得row。

不需要掃描左、右leaves。Tree的實際I/O仍受cache、page size與DBMS implementation影響。

### Worked example: range scan

找`45 <= key <= 80`時，先以45下降到middle leaf，從50開始輸出；接著沿leaf links讀取
60、70、80，遇到90停止。Ordered leaves使range不必對每個可能值重新從root搜尋。

### 你來操作

在圖上追蹤key 25、65及100的search path；再列出range `[25,75]`實際輸出的keys及停止
條件。

### 檢查方式

25走left leaf並找到30之前的位置；65走middle leaf但不存在；100走right leaf後超過最後
key。Range輸出30、40、50、60、70，讀到80時停止。

## 5. B+ tree updates（概念延伸）

Insertion先找到leaf並按序放入entry。若node超過capacity，split成兩個nodes並把新的
separator送到parent；split可能向上propagate。Deletion若造成underflow，可向sibling
redistribute或merge，必要時更新parent。無論如何，leaves仍在同一depth。

### Worked example: leaf split

在圖的middle leaf `[40,50,60]`插入65：

1. 找到middle leaf並形成暫時序列`[40,50,60,65]`。
2. 因capacity是3，split成`[40,50]`與`[60,65]`。
3. 把new right leaf的first key 60作separator加入root。
4. Root由`[40|70]`成為`[40|60|70]`，leaf links改為left -> `[40,50]` ->
   `[60,65]` -> right。

此例root仍有空間；若parent也full，還會繼續split。教材不要求背完整insert/delete
pseudocode，但必須能保持ordering、capacity、links與balanced property。

### 你來操作

假設root最多3個separator keys，接著在right leaf `[70,80,90]`插入85。畫出leaf split，
說明為何root也必須split，以及所有leaves的depth最後是否相同。

### 回饋重點

Right leaf應分為兩個ordered leaves並送出separator；root overflow後建立new root。完成後
所有leaves仍同depth。只把85擠進full leaf而不處理capacity不正確。

## 6. Ordered index and hash index（概念延伸）

Hash index以hash function把search-key value映射到bucket，適合equality lookup。不同keys
可能collision到同一bucket，仍需在bucket內比較。因bucket addresses不保存key order，
一般hash index不能有效支援range query。SQLite lab不建立hash index，因目前SQLite
環境的普通user-created indexes是B-tree family；hash只作概念比較。

### Worked example

假設`h(k)=k mod 4`：keys 10、14都到bucket 2。找14時先算bucket 2，再比較其中entries；
找`10 <= k <= 14`則不能只算一個bucket，因11、12、13分散在其他buckets。Ordered B+
tree可先找10，再沿leaves到14。

### 你來判斷

在「依exact session token查一列」與「依order date查一週」兩個需求中，各選ordered或
hash index並解釋。若還需`ORDER BY token`，選擇是否改變？

### 檢查方式

Exact equality可考慮hash；date range及ordered traversal需要ordered index。若同時需要
token order，ordered index的用途增加。這是概念比較，實際仍依DBMS支援與plan決定。

## 7. Composite index and lexicographic order

Composite index `(A,B)`先依A排序；A相同時再依B排序，類似字典先比較第一個字。它通常
有效支援`A = value`及`A = value AND B range`。只限制B時，不能假設DBMS一定能直接
使用完整ordered range；某些optimizer可能採skip-scan等技術，所以要看實際plan。

### Worked example

常見query：

```sql
SELECT ordered_at, amount
FROM ch14_order_line
WHERE customer_id = 'C0042'
  AND ordered_at BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY ordered_at;
```

`(customer_id, ordered_at)`把同一customer的rows放在連續key range內，且其內再按date
排序。反過來的`(ordered_at, customer_id)`主要先按date排列，不符合這個query的leading
equality pattern。

### 你來操作

對index `(dept_code, salary)`判斷下列predicates，並說明可用的leading部分：

```text
A. dept_code = 'IM'
B. dept_code = 'IM' AND salary BETWEEN 50000 AND 70000
C. salary = 60000
D. dept_code < 'IM' AND salary = 60000
```

### 預期與回饋

A使用first component；B使用department equality後的salary range；C缺少leading
department；D在first component已是range，不能推定second component能形成單一連續
range。實際DBMS可能另選plan，但不能從index名稱直接宣稱四者都同樣有效。

## 8. Covering index

若index包含query需要輸出的所有columns，DBMS可能只讀index而不回table取row，這稱為
covering index。多放columns會增加index size、降低fanout並增加write cost，因此covering
不是免費的。

### Worked example

`(customer_id, ordered_at)`可找出目標entries，但query還要`amount`時可能需要回table。
新增`(customer_id, ordered_at, amount)`後，SQLite 3.45.3在本lab顯示`USING COVERING
INDEX`。這個觀察只支持lab的query及環境，不代表所有DBMS使用相同術語或選擇。

### 你來判斷

若report還要輸出`status`，現有covering index是否仍cover？提出一個新index後，再說明
為什麼不應在知道report頻率與update workload前立即建立。

### 檢查方式

現有index不含status；加入status可cover該projection，但會加大每個entry並提高維護成本。

## 9. SQL and query-plan lab

`student_lab.sql`建立20,000列可重現資料，依序觀察：

1. 無secondary index時的table scan；
2. 建立`(customer_id, ordered_at)`後的index search；
3. 建立包含amount的index後的covering search；
4. 缺少leading customer predicate及低-selectivity status predicate時的plan。

主要語法：

```sql
CREATE INDEX idx_name ON table_name (column1, column2);
DROP INDEX idx_name;
EXPLAIN QUERY PLAN SELECT ...;
```

DBMS自行選access path；`CREATE INDEX`不保證每一條query都使用它。Plan中主要找：

- `SCAN`或`SEARCH`；
- index name；
- covered predicates，例如`customer_id=?`與date bounds；
- `COVERING INDEX`；
- 額外sort或temporary structure訊息。

### 你來操作

完整執行lab，為三個階段保留plan文字。回答：哪個predicate讓planner定位到連續index
range？哪一版不需另取amount？status query為何即使有index也未必值得使用？

### 預期與回饋

在已驗證SQLite 3.45.3環境，第一階段為table scan；composite index階段以customer及date
bounds進行search；covering階段出現covering index。Status中`COMPLETE`佔大多數，取得
大量rows時index benefit可能小，仍需實際statistics及plan。

若你的版本出現不同plan，先記錄SQLite version、完整DDL、row counts及`ANALYZE`狀態，
不要把不同輸出直接當作錯誤。

## 課堂比較與個人學習證據

各組為同一組三條queries提出最多兩個indexes。共同回答必須列出query-to-index理由、
不被支援的query及write/storage cost。回答鎖定後比較plan；教師依predicates、selectivity、
ordering、covering及maintenance回饋，學生再修改。

個人保存：初始proposal、三份plan、revised proposal，以及一句明確限制「目前證據不能
支持什麼」。同儕排名不用來直接計算正式成績。

## 常見錯誤

1. 把search key誤認為一定unique。
2. 認為index會改變query結果或修復normalization問題。
3. 每個column都加index，沒有計算writes及space。
4. 認為composite index的column order不重要。
5. 只看一次elapsed time，不看plan、rows及cache狀態。
6. 看到`CREATE INDEX`成功就宣稱query已使用index。
7. 把textbook B+ tree抽象圖當成特定DBMS公開的physical page格式。

## 本章總結

Index選擇從workload開始，以search key、ordered/hash properties、composite ordering與
covering需求形成假設，再由實際plan驗證。B+ tree以balanced high-fanout structure支援
equality與range access，同時付出space及update maintenance。Ch15將把table scan、index
scan與join operator放入完整query processing流程。

## 課後接續

- 為自己的一張table列出top three queries及update pattern，再提出不超過兩個indexes。
- 補充閱讀complete B+ tree insertion/deletion pseudocode、B-tree、LSM、bitmap、spatial
  及temporal indices；這些不是本課selected Ch14考試操作範圍。
