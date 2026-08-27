# Chapter 3: Introduction to SQL

## 本章核心問題

Ch2用relational algebra描述「要哪些tuples與attributes」。本章把這些需求寫成
可以由DBMS執行的SQL，並處理formal relation沒有完整呈現的實務問題：duplicates、
`NULL`、aggregation、subqueries及資料修改。

## 授課摘要

| 教學內容 | 完整範例與練習 | 學習證據 |
|---|---|---|
| DDL、basic queries、expressions、duplicates、patterns與ordering | course-registration SQL prediction and execution | SQL file與query results |
| `NULL`、aggregation、`GROUP BY`/`HAVING` | `COUNT(*)`/`COUNT(column)`及group filtering比較 | result table與解釋 |
| `IN`、`EXISTS`、一個correlated query與一個CTE | `NOT IN`加`NULL`反例及`NOT EXISTS`修正 | SQL verification table |
| basic `INSERT`、`UPDATE`與`DELETE` | 可回復的資料修改 | 影響rows與rollback結果 |

Subquery in `FROM`、scalar subquery及更複雜的correlated query保留範例作課後延伸，
未經另行教學與練習不列入Exam 1主要操作題。

## 與Ch2的關係

| Ch2 relational algebra | Ch3 SQL中的主要對應 |
|---|---|
| Projection `Π` | `SELECT`中的column list |
| Selection `σ` | `WHERE` predicate |
| Cartesian product `×` | `FROM`列出多個relations但沒有matching predicate |
| Rename `ρ` | `AS` aliases |
| Union `∪` | `UNION` |
| Intersection `∩` | `INTERSECT` |
| Difference `−` | `EXCEPT` |

這張表用來理解query meaning，不代表DBMS一定按照表中順序執行。實際execution
plan會在Ch15及Ch16處理。

## 學習目標

完成本章後，你應能：

1. 使用`CREATE TABLE`定義attributes、data types、primary key、foreign key、
   `NOT NULL`及簡單`CHECK` constraint。
2. 使用`SELECT`、`FROM`及`WHERE`取得指定資料，並解釋query result。
3. 正確使用`DISTINCT`、aliases、expressions、`LIKE`、`BETWEEN`及`ORDER BY`。
4. 使用`UNION`、`UNION ALL`、`INTERSECT`及`EXCEPT`，並判斷duplicates。
5. 使用`IS NULL`與`IS NOT NULL`，解釋`UNKNOWN`為何不通過`WHERE`。
6. 使用`COUNT`、`MIN`、`MAX`、`SUM`、`AVG`、`GROUP BY`及`HAVING`。
7. 使用`IN`、`EXISTS`、一個correlated subquery及一個CTE解決小型查詢需求。
8. 辨識`NOT IN`遇到`NULL`時的風險，並在適當情況使用`NOT EXISTS`。
9. 在constraint保護下執行`INSERT`、`UPDATE`及`DELETE`，並在執行前預測影響列數。

## 使用資料與執行方式

本章沿用Ch2的四個relations：

```text
department(dept_code, dept_name, building)
student(student_id, email, student_name, dept_code)
course(course_id, title, dept_code, credits)
enrollment(student_id, course_id, term, grade)
```

Primary keys及foreign keys以Ch2 schema diagram為準。執行`student_lab.sql`前，先在
新的SQLite database執行Ch2的`course_registration_setup.sql`。

每個example執行前先寫下：

- 預期result attributes。
- 預期tuple數。
- 可能出現的duplicates或`NULL`。
- query是否讀取資料、修改資料，或修改schema。

## 定義資料與基本查詢

### 1. SQL的工作範圍

SQL不只用來query。與本章直接相關的部分包括：

- **DDL**：定義或改變schema，例如`CREATE TABLE`、`ALTER TABLE`、`DROP TABLE`。
- **DML**：讀取或修改tuples，例如`SELECT`、`INSERT`、`UPDATE`、`DELETE`。
- **Integrity constraints**：拒絕不符合資料規則的修改。

Views、transaction control及authorization會在後續章節處理。

### 2. Data types與`CREATE TABLE`

SQL標準常見types包括`VARCHAR(n)`、`CHAR(n)`、`INTEGER`及`NUMERIC(p,d)`。不同
DBMS對長度、precision及自動轉型的實作可能不同。本課目前用SQLite，因此可執行
lab使用`TEXT`與`INTEGER`，並以constraints補上必要限制。不能把SQLite type
affinity當成所有DBMS的通則。

**Worked example**

```sql
CREATE TABLE study_group (
    group_id TEXT PRIMARY KEY,
    group_name TEXT NOT NULL,
    course_id TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity BETWEEN 2 AND 8),
    FOREIGN KEY (course_id) REFERENCES course (course_id)
);
```

逐行判讀：

1. `group_id`是primary key，因此必須unique且不能是`NULL`。
2. `group_name`與`course_id`明確不允許`NULL`。
3. `capacity`只能介於2到8；`BETWEEN`包含兩個端點。
4. `course_id`必須指向已存在的`course.course_id`。

插入`('G01', 'SQL Practice', 'DB201', 4)`可以成立。插入capacity 10或不存在的
course_id應被拒絕。

**你來判斷**

設計`study_group_member(group_id, student_id, member_role)`的constraints。答案必須
防止同一學生在同一group重複出現，並防止指向不存在的group或student。

### 3. `DROP TABLE`、`DELETE`與`ALTER TABLE`不是同一件事

- `DELETE FROM r`移除符合條件的tuples，relation schema仍存在。
- `DROP TABLE r`移除relation本身，包括schema與data。
- `ALTER TABLE`改變既有schema；可用功能與限制依DBMS而異。

**Worked example**

刪除`study_group`中的全部tuples後，仍可再`INSERT`。若`DROP TABLE study_group`，
必須重新`CREATE TABLE`後才能再存資料。這兩個操作的影響範圍不同，不能互換。

**你來判斷**

若只想移除G01但保留其他groups與table structure，應使用哪一類statement？答案要
包含一個能識別G01的predicate。

### 4. `SELECT`、`FROM`及`WHERE`

基本query形狀是：

```sql
SELECT result_expressions
FROM input_relations
WHERE predicate;
```

- `FROM`指出需要哪些input relations。
- `WHERE`只保留predicate結果為`TRUE`的rows。
- `SELECT`決定result attributes或expressions。

SQL文字順序是`SELECT`、`FROM`、`WHERE`，理解query meaning時可以先想`FROM`，
再想`WHERE`，最後想`SELECT`。這只是語意理解方式，不是physical execution order。

**Worked example**

需求：「找出IM系、但不是S101的學生ID與姓名。」

```sql
SELECT student_id, student_name
FROM student
WHERE dept_code = 'IM' AND student_id <> 'S101';
```

`FROM`取得`student`；`WHERE`留下S103；`SELECT`輸出`student_id`與
`student_name`。結果是`(S103, Kai Wu)`。

**你來判斷**

預測把`AND`改成`OR`後會有哪些students。逐列說明至少哪一個condition為`TRUE`。

### 5. Duplicates、`DISTINCT`與expressions

SQL query results預設可以包含duplicates：

```sql
SELECT dept_code
FROM student;
```

結果包含兩個IM，因為兩位students屬於IM。加入`DISTINCT`才移除重複：

```sql
SELECT DISTINCT dept_code
FROM student;
```

結果是DES、FIN、IM。`DISTINCT`作用在整個result tuple，不是只看某一個任意column。

`SELECT`也可以包含expression：

```sql
SELECT course_id, credits, credits * 18 AS semester_hours
FROM course;
```

`AS semester_hours`為result attribute命名。這個query只計算顯示值，不會修改
`course.credits`。

**你來判斷**

說明`SELECT DISTINCT dept_code, student_name FROM student`為何不會把兩位IM學生
合併成一列。

### 6. 多個relations與aliases

Ch3用`FROM`列出多個relations，再由`WHERE`提供matching predicate：

```sql
SELECT s.student_name, e.course_id, e.grade
FROM student AS s, enrollment AS e
WHERE s.student_id = e.student_id;
```

`s`與`e`是table aliases。`s.student_id = e.student_id`避免把每位student與每筆
enrollment任意配對。Ch4會改用更清楚的explicit `JOIN ... ON ...`語法。

**Worked example**

本例有4個student tuples及6個enrollment tuples。省略matching predicate會產生
24個combinations；加入predicate後只有6筆真實修課紀錄。

**你來判斷**

要取得course title與department name，需要哪些relations？寫出aliases及matching
predicate，並指出兩邊的同名attribute。

### 7. String patterns、`BETWEEN`及ordering

`LIKE`使用兩個常見wildcards：

- `%`：零個以上characters。
- `_`：恰好一個character。

```sql
SELECT course_id, title
FROM course
WHERE title LIKE '%Technology%';
```

這個pattern找出title中包含`Technology`的courses。大小寫規則會受DBMS及collation
影響；需要明確的case-insensitive比較時，可在確認DBMS行為後使用`LOWER(title)`
與lowercase pattern。

`BETWEEN 1 AND 2`包含1與2。`ORDER BY`控制display order：

```sql
SELECT course_id, title, credits
FROM course
WHERE credits BETWEEN 1 AND 2
ORDER BY credits DESC, course_id ASC;
```

沒有`ORDER BY`時，不應依賴rows目前顯示的先後順序。

**你來判斷**

分別寫出pattern：title以`Data`開頭；title的第二個character是`e`。說明`%`與`_`
在兩個patterns中的角色。

### 8. Set operations

`UNION`、`INTERSECT`及`EXCEPT`要求兩邊result具有相同column數及相容types。

令DB學生為`{S101, S103}`，FinTech學生為`{S101, S102}`：

| SQL operation | Duplicate handling | Result |
|---|---|---|
| `UNION` | 移除duplicates | S101, S102, S103 |
| `UNION ALL` | 保留兩邊全部copies | S101, S101, S102, S103 |
| `INTERSECT` | 移除duplicates | S101 |
| `EXCEPT` | 左邊減右邊並移除duplicates | S103 |

SQLite支援這四個examples，但不支援`INTERSECT ALL`及`EXCEPT ALL`。不要因某個
DBMS不支援某個syntax，就把它誤寫成SQL標準不存在。

**你來判斷**

若把`EXCEPT`兩邊交換，結果為何？再解釋為何`EXCEPT`具有方向。

### 9. `NULL`與three-valued logic

`NULL`不是空字串、0或一個可直接比較的普通value。除了`IS NULL`及
`IS NOT NULL`，與`NULL`的comparison通常得到`UNKNOWN`。

```sql
WHERE grade = NULL       -- 不會得到預期的NULL rows
WHERE grade IS NULL      -- 正確測試NULL
```

`WHERE`只保留predicate為`TRUE`的rows；`FALSE`與`UNKNOWN`都不保留。

常用邏輯結果：

| Expression | Result |
|---|---|
| `TRUE AND UNKNOWN` | `UNKNOWN` |
| `FALSE AND UNKNOWN` | `FALSE` |
| `TRUE OR UNKNOWN` | `TRUE` |
| `FALSE OR UNKNOWN` | `UNKNOWN` |
| `NOT UNKNOWN` | `UNKNOWN` |

**Worked example**

暫時把S102的FT210 grade改成`NULL`：

- `COUNT(*)`計算6筆enrollments。
- `COUNT(grade)`忽略`NULL`，結果是5。
- `WHERE grade <> 'F'`也不保留該row，因為`NULL <> 'F'`是`UNKNOWN`。

Lab會復原這項暫時修改。

**你來判斷**

對grade分別是`A`、`F`、`NULL`的三列，計算`grade <> 'F'`的truth value，再指出
哪些rows通過`WHERE`。

## Aggregation、selected subqueries與資料修改

### 10. Aggregate functions

Aggregate function把一組values轉成一個value：

- `COUNT(*)`計算rows。
- `COUNT(attribute)`計算attribute不是`NULL`的rows。
- `MIN`、`MAX`、`SUM`、`AVG`忽略`NULL` inputs。

**Worked example**

```sql
SELECT COUNT(*) AS course_count,
       MIN(credits) AS min_credits,
       MAX(credits) AS max_credits,
       SUM(credits) AS total_credits,
       AVG(credits) AS avg_credits
FROM course;
```

目前credits是3、3、3、2，因此結果為：

| course_count | min_credits | max_credits | total_credits | avg_credits |
|---:|---:|---:|---:|---:|
| 4 | 2 | 3 | 11 | 2.75 |

`AVG`不能先用`DISTINCT`去掉相同的3，因為三門不同courses各自都必須被計入。

**你來判斷**

比較`COUNT(*)`、`COUNT(grade)`及`COUNT(DISTINCT grade)`各自回答什麼問題。不要只
寫函數名稱。

### 11. `GROUP BY`

`GROUP BY`把grouping attributes相同的rows放入同一group，再對每組計算aggregate：

```sql
SELECT dept_code,
       COUNT(*) AS course_count,
       AVG(credits) AS avg_credits
FROM course
GROUP BY dept_code
ORDER BY dept_code;
```

結果為：

| dept_code | course_count | avg_credits |
|---|---:|---:|
| DES | 1 | 2.0 |
| FIN | 1 | 3.0 |
| IM | 2 | 3.0 |

依standard SQL，`SELECT`中沒有放在aggregate function裡的attributes，應出現在
`GROUP BY`。SQLite有時允許額外columns並任選一個value，但本課不採用這種不可
攜的寫法。

**你來判斷**

為何`SELECT dept_code, title, COUNT(*) FROM course GROUP BY dept_code`在一個
department有多門課時無法唯一決定`title`？提出符合standard SQL的改寫方向。

### 12. `WHERE`與`HAVING`

- `WHERE`在形成groups前篩選individual rows。
- `HAVING`在aggregation後篩選groups。

**Worked example**

```sql
SELECT dept_code, COUNT(*) AS course_count
FROM course
WHERE credits >= 3
GROUP BY dept_code
HAVING COUNT(*) >= 2;
```

先移除credits小於3的WD120，再依dept_code分組，最後只保留至少兩門課的IM。
結果是`(IM, 2)`。

**你來判斷**

若需求是「只計算3學分以上courses，並保留平均credits大於2.5的departments」，
指出哪一個condition放`WHERE`，哪一個放`HAVING`，並說明原因。

### 13. `IN` subquery

Subquery是嵌在另一個query中的`SELECT`。先讓內層query產生一組values，再由外層
測試membership：

```sql
SELECT student_id, student_name
FROM student
WHERE student_id IN (
    SELECT student_id
    FROM enrollment
    WHERE course_id = 'DB201'
);
```

內層結果是`{S101, S103}`，外層再取得An Chen與Kai Wu。

**你來判斷**

先單獨寫出「FT210學生IDs」的inner query，再把它放入outer query取得emails。
必須先驗證inner result，再驗證完整query。

### 14. `EXISTS`與correlated subquery

`EXISTS(subquery)`只問subquery是否至少回傳一列。若inner query引用outer query
目前的row，就是correlated subquery。

**Worked example**

```sql
SELECT s.student_id, s.student_name
FROM student AS s
WHERE EXISTS (
    SELECT 1
    FROM enrollment AS e
    WHERE e.student_id = s.student_id
      AND e.grade IN ('A', 'A-')
);
```

對每位student，inner query檢查是否至少有一筆A或A-的enrollment。`SELECT 1`只
表示我們關心row是否存在，不需要inner query輸出實際attributes。

**你來判斷**

把需求改成「沒有任何enrollment的students」，應使用`EXISTS`還是`NOT EXISTS`？
寫出inner matching predicate。

### 15. `NOT IN`遇到`NULL`的風險

如果`NOT IN`的subquery result含有`NULL`，不相等比較可能變成`UNKNOWN`，導致
outer query沒有任何row通過。

**Worked example**

Blocked IDs為`{S104, NULL}`。以下query回傳0 rows，不是S101、S102、S103：

```sql
SELECT student_id
FROM student
WHERE student_id NOT IN ('S104', NULL);
```

可改用明確matching condition的`NOT EXISTS`：

```sql
SELECT s.student_id
FROM student AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM blocked AS b
    WHERE b.student_id = s.student_id
);
```

這時S104有match而被排除；`NULL`不會與其他student_id相等，結果是S101、S102、
S103。

**你來判斷**

不能只背「永遠不要用`NOT IN`」。說明在什麼資料保證下`NOT IN`不會遇到這個
`NULL`問題，以及你如何從schema或query確認這個保證。

### 16. Subquery in `FROM`與CTE（CTE為課堂核心；`FROM`作延伸）

Query result仍是relation，所以可以放在`FROM`：

```sql
SELECT course_id, enrollment_count
FROM (
    SELECT course_id, COUNT(*) AS enrollment_count
    FROM enrollment
    GROUP BY course_id
) AS counts
WHERE enrollment_count >= 2;
```

Inner query先得到各course的enrollment count，outer query留下count至少2的DB201及
FT210。

相同中間結果也能用`WITH`定義CTE：

```sql
WITH counts AS (
    SELECT course_id, COUNT(*) AS enrollment_count
    FROM enrollment
    GROUP BY course_id
)
SELECT course_id, enrollment_count
FROM counts
WHERE enrollment_count >= 2;
```

CTE只在目前statement中可使用。DBMS不一定把它實際儲存成temporary table。

**你來判斷**

先建立每個department的course count，再找出count最高值。可以使用subquery in
`FROM`或CTE，但每一層必須明確列出result attributes。

### 17. Scalar subquery（課後延伸）

Scalar subquery用在需要單一value的位置，因此必須回傳一列一欄。`COUNT(*)`沒有
`GROUP BY`時保證得到一個value：

```sql
SELECT c.course_id,
       c.title,
       (
           SELECT COUNT(*)
           FROM enrollment AS e
           WHERE e.course_id = c.course_id
       ) AS enrollment_count
FROM course AS c;
```

結果是DB201與FT210各2人，ML230與WD120各1人。若scalar subquery實際回傳多列，
standard SQL應產生error；不同DBMS的非標準處理不能當成可攜行為。

**你來判斷**

如何修改inner query，使每個course顯示所有grades，卻不再保證單一value？說明這
為何不適合scalar position，不必執行錯誤query。

### 18. `INSERT`、`UPDATE`及`DELETE`

資料修改前先回答三個問題：

1. 哪一個relation會改變？
2. 哪些rows會受影響？
3. 是否可能違反primary key、foreign key、`NOT NULL`或`CHECK` constraint？

**Worked example**

```sql
INSERT INTO student (student_id, email, student_name, dept_code)
VALUES ('S105', 'noah.lee@example.edu', 'Noah Lee', 'IM');

UPDATE student
SET dept_code = 'FIN'
WHERE student_id = 'S105';

DELETE FROM student
WHERE student_id = 'S105';
```

1. `INSERT`新增一列，且IM必須先存在。
2. `UPDATE`只修改S105；漏掉`WHERE`會修改所有students。
3. `DELETE`只刪除S105；若其他relation已有foreign key指向S105，刪除可能被拒絕。

Lab把示範包在savepoint中並復原資料。Transaction的完整概念在Ch4與Ch17教授。

**你來判斷**

在執行`UPDATE course SET credits = 4`前，預測會修改幾列。再補上一個只修改DB201
的predicate，並說明如何用`SELECT`先確認target rows。

## 補充閱讀，不列入本章主要考點

下列內容存在於教科書Ch3，但在本課只作定位，不要求學生掌握完整syntax：

- `SOME`／`ALL` set comparisons。
- `UNIQUE`／`NOT UNIQUE` subquery tests；多數DBMS未廣泛實作。
- `LATERAL` subqueries。
- Scalar query without `FROM`與DBMS-specific dummy relation。
- `INTERSECT ALL`及`EXCEPT ALL`；SQLite不支援。
- `INSERT ... SELECT`、scalar subquery update及複雜`CASE` update。
- Multiset relational algebra的形式定義。

這些內容不得在未另行教學與練習前直接列入Exam 1。

## 課堂活動與Class Performance

每位學生提交：

1. `student_lab.sql`的預測與實際結果表。
2. 一個`NULL`造成錯誤判斷的例子及修正。
3. 一個aggregation query，並標示`WHERE`、group formation、`HAVING`及`SELECT`
   各階段的作用。
4. 一個subquery，包含inner result與outer result的分開驗證。
5. 一個在savepoint中完成且已復原的資料修改例子。

課堂比較題：各組修正一段同時混淆`WHERE`、`HAVING`與`NULL`的SQL。匿名展示後，
依下列標準排序：result是否符合需求、`NULL`處理是否正確、grouping是否合法、
是否能用sample data驗證。Peer rank本身不直接計分；個人修正版才是學習證據。

## 常見錯誤

| 錯誤 | 影響 | 檢查方式 |
|---|---|---|
| 以為`SELECT`會自動移除duplicates | Result多出copies | 明確判斷是否需要`DISTINCT` |
| 漏掉multi-table matching predicate | 產生Cartesian product | 先寫出每對relations的連結attributes |
| 沒有`ORDER BY`卻依賴顯示順序 | 不同執行可能順序不同 | 只有需要display order時才明列排序 |
| 使用`= NULL`或`<> NULL` | Predicate成為`UNKNOWN` | 使用`IS NULL`或`IS NOT NULL` |
| 把row filter放在`HAVING` | 過晚才篩選或語意錯誤 | 問condition針對row還是group |
| `SELECT`非aggregate column未列入`GROUP BY` | 非standard或結果不確定 | 每個output column逐一分類 |
| `NOT IN` subquery可能含`NULL` | 可能得到0 rows | 證明subquery column為`NOT NULL`或使用`NOT EXISTS` |
| Scalar subquery回傳多列 | Runtime error或非標準結果 | 先單獨執行inner query |
| `UPDATE`或`DELETE`漏掉`WHERE` | 修改全部rows | 先用相同predicate執行`SELECT`及計數 |
| 把SQLite行為當成SQL標準 | 換DBMS後失敗 | 記錄DBMS與版本並查官方文件 |

## 本章總結

- DDL定義schema與constraints；DML查詢或修改tuples。
- `SELECT/FROM/WHERE`分別決定output、inputs及row predicates。
- SQL預設保留duplicates；需要set result時明確使用`DISTINCT`或set operation。
- `NULL`引入`UNKNOWN`；`WHERE`只保留`TRUE`。
- Aggregation先處理rows，再形成groups，最後由`HAVING`篩選groups。
- Subquery應先獨立驗證inner result，再判讀outer query。
- `NOT IN`對`NULL`敏感；`NOT EXISTS`能用matching logic清楚表達absence。
- 每次資料修改都應先確認target rows與constraints，並在可復原環境測試。

下一章將把多relation queries改寫成explicit join expressions，並進一步處理views、
transactions及integrity constraints。
