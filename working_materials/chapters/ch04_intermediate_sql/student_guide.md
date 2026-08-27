# Chapter 4: Intermediate SQL

## 本章核心問題

Ch3已能查詢及修改單一或多個relations。本章進一步處理四個實務問題：如何明確
寫出relations之間的連結、如何保存可重複使用的query definition、如何把多個修改
視為同一個工作單位，以及如何讓DBMS拒絕不合法的資料。

本章課堂核心集中在：

- explicit inner joins、`ON`、`USING`及`NATURAL JOIN`的風險。
- left outer join，以及outer join中`ON`與`WHERE`的差異。
- view的定義、查詢及資料變動反映方式。
- `COMMIT`、`ROLLBACK`及transaction的基本atomicity。
- `NOT NULL`、`UNIQUE`、`CHECK`、foreign keys及referential actions。

Right/full outer join、view modification細部規則、materialized views、deferred
constraints、assertions及authorization作課後延伸，不是Exam 1的主要操作題。
Index definition移到Ch14。

## 與Ch3的關係

Ch3曾用comma-separated `FROM`及`WHERE`連結relations。本章改用explicit join：

```sql
FROM student AS s
JOIN enrollment AS e ON e.student_id = s.student_id
```

對inner join而言，matching predicate常可在`ON`或`WHERE`得到相同結果；對outer
join而言，兩者可能產生不同結果。Ch3的基本constraints也會在本章擴充成一套能
實際驗證資料規則的schema設計。

## 先備知識與執行方式

你應已能使用aliases、`SELECT`、`WHERE`、`GROUP BY`、`NULL`、`INSERT`、`UPDATE`
及`DELETE`，並能指出primary key與foreign key。

本章沿用Ch2的course-registration database。先在新的SQLite database執行：

```text
working_materials/chapters/ch02_relational_model/course_registration_setup.sql
```

再執行本章的`student_lab.sql`。Right及full outer join examples需要SQLite 3.39或
更新版本；本教材已在SQLite 3.45.3驗證。每個block執行前先記錄：result attributes、
預期row數、可能出現的`NULL`，以及schema或data是否會改變。

## 學習目標

完成本章後，你應能：

1. 使用`JOIN ... ON`連結兩個以上relations，並逐一說明matching columns。
2. 比較`ON`、`USING`及`NATURAL JOIN`，辨識同名column造成的非預期matching。
3. 判讀inner與left outer join保留哪些rows及在哪裡補`NULL`。
4. 解釋outer join中把condition放在`ON`或`WHERE`為何可能改變結果。
5. 建立及查詢view，並解釋一般view與stored query result的差別。
6. 說明view modification可能不明確；細部DBMS規則作課後延伸。
7. 使用transaction boundaries把多個modifications視為一個工作單位，並用
   `ROLLBACK`恢復開始前的狀態。
8. 使用`NOT NULL`、`UNIQUE`、`CHECK`與foreign keys表達可由DBMS檢查的規則。
9. 根據business rule選擇reject、`CASCADE`或`SET NULL`，並說明可能影響。

## 1. Explicit inner join與`ON`

Inner join只保留兩邊符合join condition的row pairs。`ON`放的是relations之間的
matching rule；`WHERE`則放對joined rows的其他篩選條件。這種分工通常更容易檢查。

**Worked example**

需求：「列出每筆修課紀錄的學生、課程名稱與成績。」

```sql
SELECT s.student_id, s.student_name,
       c.course_id, c.title, e.grade
FROM student AS s
JOIN enrollment AS e ON e.student_id = s.student_id
JOIN course AS c ON c.course_id = e.course_id
ORDER BY s.student_id, c.course_id;
```

逐步判讀：

1. `student JOIN enrollment`以`student_id`找到每筆enrollment的學生。
2. 前一步結果再以`course_id`連到`course`。
3. 每筆enrollment只有一個matching student及course，因此目前輸出6 rows。
4. S101修讀FT210，即使學生與課程屬於不同department，仍是合法match；join rule
   只要求兩邊`course_id`相同。

若省略第二個`ON`，就無法正確說明course如何對應enrollment。若join condition
寫錯成`c.dept_code = s.dept_code`，會把「同系」誤當成「實際修讀」。

**你來操作**

列出每筆enrollment的學生email與course所屬department name。先寫出三條relations
之間的兩個matching conditions。

**檢查方式**

結果應有6 rows；S101/FT210必須保留，且它的course department是Finance。若row數
多於6，先檢查是否漏掉join condition；少於6則檢查是否加入了不屬於需求的條件。

## 2. `USING`與`NATURAL JOIN`

兩邊具有同名且確實表示同一件事的column時，可以用`USING(column)`指定matching
column。`NATURAL JOIN`則自動要求兩邊所有同名columns相等。自動判斷很簡短，但
schema新增或意義不同的同名column都可能悄悄改變query result。

**Worked example: `USING`**

```sql
SELECT c.course_id, c.title, d.dept_name
FROM course AS c
JOIN department AS d USING (dept_code)
ORDER BY c.course_id;
```

`USING (dept_code)`明確指定course所屬department。結果有4 rows，每門course恰好
對應一個department。

**Worked counterexample: `NATURAL JOIN`**

```sql
SELECT student_id, student_name, course_id, title
FROM student
NATURAL JOIN enrollment
NATURAL JOIN course;
```

第一個join使用共同的`student_id`。但其result與`course`同時具有`course_id`及
`dept_code`，第二個natural join會要求兩者都相等。S101屬於IM卻合法修讀FIN的
FT210，因此這筆資料被錯誤移除；結果只有5 rows。相同需求用兩個explicit
`JOIN ... ON`會得到正確的6 rows。

**你來操作**

把`USING (dept_code)` example改寫成`ON`，再比較attributes與rows。說明為何
`ON c.dept_code = d.dept_code`不會受到其他同名columns影響。

**檢查方式**

兩個queries都應得到DB201、FT210、ML230、WD120共4 rows及正確department name。
`ON`版本若使用`SELECT *`，matching column可能出現兩次；比較時應先列出需要的
attributes。

## 3. Inner與outer joins

Inner join會失去沒有match的rows。Outer join在保留側遇到沒有match的row時，仍將
它放入result，另一側attributes以`NULL`補齊。

| Join type | 保留沒有match的rows |
|---|---|
| `INNER JOIN` | 不保留 |
| `LEFT OUTER JOIN` | 保留左relation |
| `RIGHT OUTER JOIN` | 保留右relation |
| `FULL OUTER JOIN` | 兩邊都保留 |

`OUTER` keyword可省略，例如`LEFT JOIN`等同`LEFT OUTER JOIN`。

**Worked example: left outer join**

Lab暫時加入沒有學生修讀的IS250：

```sql
SELECT c.course_id, c.title, COUNT(e.student_id) AS enrollment_count
FROM course AS c
LEFT OUTER JOIN enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.title
ORDER BY c.course_id;
```

結果中的IS250仍存在，`enrollment_count`是0。這裡使用`COUNT(e.student_id)`而不是
`COUNT(*)`：outer join為IS250產生一個null-padded row，`COUNT(*)`會把它算成1，
但`COUNT(e.student_id)`不計`NULL`。

**Worked example: right與full outer join**

Lab建立兩個很小的temporary tables。已知students為S101、S105；planned records為
S101/DB201及未知的S999/AI999。

- Right join保留兩筆planned records，所以S999的known-student columns是`NULL`。
- Full join另外保留沒有planned record的S105，所以三種情況都能看到：matched、
  left-only、right-only。

Right join可以交換relations改寫成left join。有些DBMS或舊版本沒有full join，
不能在未確認dialect前假設語法可用。

**你來操作**

使用left outer join列出每位student及修課數，包括沒有修課的student。另加入一位
沒有enrollment的temporary student來測試0。

**檢查方式**

每位student只能有一個summary row。Temporary student必須保留且count為0；若是1，
檢查是否誤用`COUNT(*)`。

## 4. Outer join中的`ON`與`WHERE`

對outer join而言，`ON`先決定哪些pairs可以match，再補上保留側沒有match的rows；
`WHERE`則在outer join產生結果後過濾。把condition從`ON`移到`WHERE`不一定等價。

**Worked example**

保留所有courses，只在右側接上grade為A或A-的enrollment：

```sql
SELECT c.course_id, e.student_id, e.grade
FROM course AS c
LEFT JOIN enrollment AS e
  ON e.course_id = c.course_id
 AND e.grade IN ('A', 'A-');
```

IS250沒有match，仍以`NULL`保留。DB201、FT210、ML230、WD120各有一筆A或A-，所以
暫時資料共有5 rows。

若改成：

```sql
FROM course AS c
LEFT JOIN enrollment AS e ON e.course_id = c.course_id
WHERE e.grade IN ('A', 'A-')
```

IS250的`e.grade`是`NULL`，predicate結果為`UNKNOWN`，因此被`WHERE`移除，剩4 rows。
這個結果在此需求下已不再「保留所有courses」。

**你來判斷**

需求A是「保留全部courses，只接上及格enrollments」；需求B是「只列出至少有一筆
及格enrollment的courses」。分別指出grade condition應放在哪裡，並說明unmatched
course是否保留。

**回饋重點**

答案必須從outer join的處理順序及`NULL` predicate解釋，不能只背「condition放
`ON`比較好」。

## 5. View的定義與查詢

View是一個由query定義的virtual relation。一般view保存query definition；使用時
根據目前base tables求值，不是建立當下結果的獨立副本。它可以簡化重複查詢，
也能只暴露使用者需要的columns或rows，但authorization本身另有規則。

**Worked example**

```sql
CREATE VIEW course_enrollment_summary AS
SELECT c.course_id,
       c.title,
       COUNT(e.student_id) AS enrollment_count
FROM course AS c
LEFT JOIN enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.title;
```

之後可像query table一樣使用：

```sql
SELECT course_id, enrollment_count
FROM course_enrollment_summary
WHERE enrollment_count >= 2;
```

目前結果為DB201與FT210。Lab暫時新增S102/DB201後，view顯示DB201 count為3；rollback
後再次查詢又是2。這支持「view依目前base data重新求值」，不是固定snapshot。

CTE只在一個statement中存在；view會保留在schema中直到`DROP VIEW`。Materialized
view則可能實際儲存結果並需要refresh，但沒有統一的standard SQL建立語法，本章不
要求操作。

**你來操作**

建立`im_course(course_id, title, credits)` view，只顯示IM courses，再透過view查詢
3-credit courses。

**檢查方式**

View definition不應包含其他department；query result應為DB201及ML230。再對base
table暫時加入一門IM course，確認view可看到它，最後rollback。

## 6. View modification的限制（課後延伸）

若透過view做`INSERT`、`UPDATE`或`DELETE`，DBMS必須把修改轉回base tables。有些
views無法唯一決定應修改哪些base rows，例如join view或aggregate view。

**Worked counterexample**

`course_enrollment_summary.enrollment_count`是多筆enrollment計算出的aggregate，
以下要求沒有唯一的base-table修改方式：

```sql
UPDATE course_enrollment_summary
SET enrollment_count = 99
WHERE course_id = 'DB201';
```

SQLite會拒絕，因為SQLite views預設read-only，除非另建`INSTEAD OF` trigger。SQL
標準與其他DBMS可能允許某些只來自單一base table的simple views更新，因此不能把
SQLite限制寫成所有DBMS通則。

**你來判斷**

比較「只選student的ID與name」及「依department計算student count」兩個views。
指出哪一個較可能具有明確的base row對應，以及aggregate view為何不明確。

**回饋重點**

答案要討論修改如何映射回base relation，不能只用「第一個比較簡單」作理由。

## 7. Transaction boundaries與atomicity

Transaction是一組共同完成一項工作的query或update statements。基本控制為：

- `COMMIT`：使transaction的修改成為永久結果；commit後不能再用rollback撤銷。
- `ROLLBACK`：撤銷目前transaction內尚未commit的修改。

Transaction的atomicity表示完整工作最後是全部反映，或在失敗時全部不反映。這裡
只處理基本使用；concurrency、isolation及recovery會在Ch17–Ch19深入教授。不同
工具的autocommit預設不同，操作前必須確認。

**Worked example**

S101要把FT210換成ML230，這項工作需要兩個statements：

```sql
BEGIN;

DELETE FROM enrollment
WHERE student_id = 'S101'
  AND course_id = 'FT210'
  AND term = '115-1';

INSERT INTO enrollment (student_id, course_id, term, grade)
VALUES ('S101', 'ML230', '115-1', NULL);

COMMIT;
```

若`INSERT`失敗而前面的`DELETE`已單獨commit，學生會失去原課程卻沒換到新課。
兩個statements放在同一transaction後，application可在失敗時`ROLLBACK`。Lab使用
`SAVEPOINT`示範並刻意復原，避免改掉共同sample data。

**你來操作**

在savepoint內設計另一個合法course swap。記錄開始rows、修改後rows及rollback後
rows。

**檢查方式**

修改後應只有指定學生的兩門課發生替換；rollback後完整回到開始rows。只執行兩個
statements而沒有明確boundary及驗證，不算完成。

## 8. Single-relation integrity constraints

Integrity constraints讓DBMS在資料修改時檢查規則：

- `NOT NULL`：column不可為`NULL`。
- `UNIQUE (A1, ..., An)`：不允許兩個rows在所列columns具有相同組合。
- `CHECK (P)`：每個row的predicate不能為`FALSE`。
- `PRIMARY KEY`：識別每個row，具有uniqueness及non-null要求。

**Worked example**

```sql
CREATE TABLE waitlist_entry (
    request_id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    term TEXT NOT NULL DEFAULT '115-1',
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5),
    UNIQUE (student_id, course_id, term)
);
```

`UNIQUE`防止同一學生對同一學期同一課程重複候補；`CHECK`限制priority範圍；
`DEFAULT`只在insert未提供term時填入115-1，並不阻止明確提供其他合法term。

`CHECK (priority BETWEEN 1 AND 5)`遇到`NULL`會得到`UNKNOWN`，而check只拒絕
`FALSE`。因此若`NULL`不合法，仍必須加`NOT NULL`。Lab的
`check_without_not_null`證實只用`CHECK (value > 0)`仍接受`NULL`。

**你來判斷**

逐一判斷以下候補資料會被哪個constraint拒絕：相同student/course/term第二次
insert、priority 8、student_id為`NULL`。若同時違反多個規則，不應依賴DBMS固定
先報哪一個。

**檢查方式**

Verifier會分開執行三種failure。學生說明必須指出constraint與被破壞的資料規則。

## 9. Referential integrity與foreign-key actions

Foreign key要求referencing columns的non-null value在referenced candidate key中
存在。兩邊column數量必須相同且types相容。本例加入：

```sql
FOREIGN KEY (student_id) REFERENCES student (student_id)
    ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES course (course_id)
```

因此S999不能進入waitlist。若刪除student：

- 預設reject/no action：仍有dependent rows時拒絕刪除。
- `ON DELETE CASCADE`：一併刪除dependent rows。
- `ON DELETE SET NULL`：把foreign key改成`NULL`，前提是column允許`NULL`。

這些不是單純語法偏好。若waitlist在學生離校後不應保留，cascade可能符合規則；
若enrollment必須保存歷史，直接cascade刪除可能造成資料損失，通常應使用其他設計。

**Worked example**

Lab暫時新增S105及其waitlist entry，再刪除S105。因waitlist foreign key明確指定
`ON DELETE CASCADE`，S105的waitlist count變成0；最後rollback，base data不變。
相對地，現有department被course或student引用時，未指定cascade的刪除會被拒絕。

**你來操作**

設計`course_feedback`：rating只能1–5；每筆feedback必須對應一筆已存在的
`enrollment(student_id, course_id, term)`；每筆enrollment最多一筆feedback。

**檢查方式**

可使用三欄composite foreign key指向`enrollment`的composite primary key，並以同一
三欄作primary key或unique constraint。測試至少一筆valid row、rating 6及不存在的
enrollment。是否允許`NULL` comment應另行決定，不能由rating constraint代替。

## 課堂整合活動與Class Performance

各組收到一段AI產生的SQL，內容同時包含`NATURAL JOIN`、left join後的`WHERE`
filter、可疑view update及未說明的cascade。各組提交修正版與逐項理由；匿名展示後，
每位學生依下列證據排列所有回答：

1. Join conditions是否對應schema中的真實關係。
2. Unmatched rows是否符合需求，且能由sample rows證明。
3. View modification是否能映射回base tables。
4. Transaction boundary是否涵蓋完整工作。
5. Constraint及foreign-key action是否符合business rule。

Peer rank不直接計分。每位學生保存自己的初始預測、lab輸出、排序理由及教師回饋後
的個人修正版，作為Class Performance evidence。

## 常見錯誤

| 錯誤 | 可觀察影響 | 修正方式 |
|---|---|---|
| 依同名columns直接使用`NATURAL JOIN` | Schema改變或無關同名column使rows消失 | 列出matching rule，優先使用`ON`或明確`USING` |
| 把left join右側filter放`WHERE` | Null-padded rows被移除，結果接近inner join | 先確認需求是限制match還是過濾final rows |
| Outer join後用`COUNT(*)`計算matches | 沒有match也被算成1 | Count右側non-null key |
| 把view當成固定資料副本 | Base data改變後的預測錯誤 | 區分view definition與materialized result |
| 假設所有views可更新 | DBMS拒絕或base modification不明確 | 查DBMS規則並分析base-row mapping |
| 依賴工具預設autocommit | Partial changes可能已永久寫入 | 明確控制transaction並驗證boundary |
| 只有`CHECK`卻以為已排除`NULL` | `UNKNOWN`通過check | 需要時另加`NOT NULL` |
| 未分析就使用`CASCADE` | 刪除範圍超過使用者意圖 | 依資料生命週期選referential action |

## 本章總結與下一章

- Explicit joins把matching rule寫在`ON`或`USING`；`NATURAL JOIN`會使用所有同名
  columns，可能因schema或語意而改變結果。
- Outer joins保留沒有match的rows並補`NULL`；`ON`與`WHERE`的condition位置會影響
  是否保留這些rows。
- View通常保存query definition並依目前base data求值；view modification是否可行
  取決於base-row mapping及DBMS。
- Transaction用`COMMIT`或`ROLLBACK`決定一組修改是否留下。
- Constraints將可檢查的資料規則放進schema；`NULL`及referential actions都必須
  明確設計。

Ch5會在這些基礎上加入functions/procedures、triggers、recursive queries與advanced
aggregation。Triggers可處理普通declarative constraints或view update不足以直接表達
的動作，但也需要清楚測試隱含的資料修改。

## 課後接續內容

1. 完成P1–P7並保留predictions與actual results。
2. 將一個comma join改寫為explicit join，證明result相同。
3. 找一個left join因`WHERE`而遺失unmatched rows的例子，附上修正前後output。
4. 閱讀materialized view、deferred constraints及assertions的概念定位；不需背誦
   DBMS-specific syntax，也不列入Exam 1主要操作題。
