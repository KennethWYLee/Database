# Chapter 5: Advanced SQL

## 本章核心問題

前幾章的SQL由使用者明確送出一個statement。本章處理四種進一步需求：把可重用
邏輯放在database中、在資料改變時自動執行動作、查詢任意深度的階層，以及在不
減少detail rows的情況下做排名與移動計算。

本章課堂核心為：

- `RANK`、`DENSE_RANK`、`ROW_NUMBER`、`PARTITION BY`與明確window frame。
- Recursive CTE的base term、recursive term、fixed point及termination。
- 一個row-level audit trigger，包括event、condition、action及`OLD`/`NEW`。

Stored function與procedure只介紹用途、input/output及基本interface，不要求安裝或
撰寫stored routine。Conditional aggregation作短示範。完整SQL procedural language、
external routines、statement-level triggers、專屬`PIVOT` syntax、`ROLLUP`、`CUBE`、
JDBC、Python database API、ODBC及embedded SQL均為課後延伸。

## 與Ch4的關係

Ch4把資料規則放在declarative constraints，並用transactions控制多個修改。Ch5
加入無法只靠一般query或constraint直接處理的資料庫程式：

- Function或procedure需要被明確呼叫。
- Trigger由指定database event自動啟動。
- Recursive CTE重複使用前一輪結果直到沒有新結果。
- Window function在query result上計算，不會像`GROUP BY`一樣把多列合併成一列。

能用foreign key、`CHECK`或普通query清楚解決時，不應只為了「自動化」就改用
trigger。

## 先備知識與執行方式

你應已能使用subquery、CTE、aggregate、views、transactions及constraints。先執行
Ch2的`course_registration_setup.sql`，再執行本章`student_lab.sql`。

本課目前使用SQLite 3.45.3。SQLite支援本章的triggers、recursive CTE及window
functions，但不能使用SQL statement建立stored function或procedure。因此：

- `standard_routine_examples.sql`是source-checked reference，**未在SQLite執行**。
- Lab只執行routine body的等價query或modification，用來核對預期資料結果。
- 本課不要求另裝server DBMS；reference用來辨認routine interface，不能宣稱已在
  SQLite或其他DBMS安裝並通過。

## 學習目標

完成本章後，你應能：

1. 正確判讀ties下的`RANK`、`DENSE_RANK`及`ROW_NUMBER`。
2. 使用`PARTITION BY`及明確window frame計算running或moving aggregate。
3. 將recursive CTE拆成base term及recursive term，逐輪說明新增的rows。
4. 說明`UNION`、`UNION ALL`、cycles及termination之間的關係。
5. 以event、condition與action解釋row-level trigger，並正確判讀`OLD`與`NEW`。
6. 判斷何時constraint或一般query比trigger更清楚，並指出trigger的隱含副作用。
7. 比較function、procedure與trigger的啟動方式及輸出方式，不把reference code
   誤認為SQLite可執行語法。

## 1. Function、procedure與trigger（用途與interface）

| Mechanism | 如何啟動 | 主要結果 |
|---|---|---|
| Function | 出現在expression或由DBMS-specific call啟動 | 回傳scalar或table value |
| Procedure | 以`CALL`或DBMS-specific syntax明確呼叫 | 執行一組statements，可有output parameters |
| Trigger | 指定table發生`INSERT`、`UPDATE`或`DELETE`時自動啟動 | 執行預先定義的action |

Stored routines可讓多個applications共用同一份database-side logic，但各DBMS的
procedural syntax差異很大。Routine中逐row呼叫複雜function也可能造成效能問題；
不能因為邏輯可重用，就推論它一定比較快。

**Worked example: scalar function contract**

需求：「給一個course ID，回傳目前enrollment count。」Reference file使用
textbook-style SQL/PSM：

```sql
CREATE FUNCTION course_enrollment_count(p_course_id VARCHAR(10))
RETURNS INTEGER
BEGIN
    DECLARE result_count INTEGER;
    SELECT COUNT(*) INTO result_count
    FROM enrollment
    WHERE course_id = p_course_id;
    RETURN result_count;
END;
```

逐步判讀：

1. `p_course_id`是一個input parameter。
2. `RETURNS INTEGER`定義function result type。
3. `SELECT ... INTO`把matching enrollment count存入local variable。
4. `RETURN`送回該integer；`COUNT(*)`即使沒有match也回傳0。

若可在目標DBMS安裝，DB201與FT210應回傳2，ML230與WD120應回傳1。Lab執行等價
scalar subquery確認這些data results，但沒有把function安裝到SQLite。

**你來設計**

為`department_course_count`寫出input、return type及等價`SELECT`。先不要寫
DBMS-specific procedural syntax。

**檢查方式**

IM應得到2，FIN與DES各1，不存在的department應得到0。答案必須區分「等價query
已執行」與「stored function已安裝」兩種證據。

## 2. Procedure與可觀察的contract（概念介紹）

Procedure通常執行一組database actions，可使用input及output parameters。它不必像
function一樣出現在query expression中。

**Worked example**

Reference procedure接受course ID與新credits：

```sql
CREATE PROCEDURE change_course_credits(
    IN p_course_id VARCHAR(10),
    IN p_credits INTEGER
)
BEGIN ATOMIC
    UPDATE course
    SET credits = p_credits
    WHERE course_id = p_course_id;
END;
```

預期呼叫方式是`CALL change_course_credits('DB201', 4)`，但實際syntax取決於DBMS。
Lab在savepoint內執行body中的`UPDATE`：DB201由3變4，rollback後回到3。

這個簡化contract仍有一項重要決定：若course ID不存在，`UPDATE`影響0 rows，
procedure應把它當成error、return status或允許no-op？若不先定義，caller不能可靠
判斷工作是否完成。

**你來判斷**

為「不存在的course」選擇一種明確反應，說明caller如何觀察。再說明credits 8
會由目前schema中的哪個constraint拒絕。

**回饋重點**

答案需同時包含procedure contract與schema constraint，不能把全部驗證都藏進
procedure。

## 3. Trigger的event、condition與action

Trigger是DBMS在指定event發生時自動執行的statement。設計時至少要回答：

1. Event是insert、delete還是某些columns的update？
2. 在event之前或之後執行？是per row還是per statement？
3. Condition何時為真？
4. Action會讀寫哪些tables？

Trigger syntax高度DBMS-specific。本課SQLite example使用row-level `AFTER UPDATE`
及`OLD`、`NEW`；它們代表該row修改前後的values。

**Worked example: grade audit**

```sql
CREATE TRIGGER enrollment_grade_audit
AFTER UPDATE OF grade ON enrollment
FOR EACH ROW
WHEN OLD.grade IS NOT NEW.grade
BEGIN
    INSERT INTO enrollment_audit (
        action_name, student_id, course_id, term, old_grade, new_grade
    ) VALUES (
        'GRADE_UPDATE', NEW.student_id, NEW.course_id, NEW.term,
        OLD.grade, NEW.grade
    );
END;
```

S103/DB201由B改為B+時，audit row保留old grade B及new grade B+。`IS NOT`在SQLite
能做null-safe difference test；若只寫`OLD.grade <> NEW.grade`，其中一邊為`NULL`
時condition會是`UNKNOWN`，可能漏記真正的變更。

Trigger action與造成它的update在同一transaction中。Lab rollback grade update後，
相對應audit row也消失。這是實際執行結果，不是只靠語法推測。

**你來操作**

建立enrollment delete audit trigger。Delete event只有old row，應保存`OLD.student_id`、
`OLD.course_id`、`OLD.term`及`OLD.grade`。在savepoint內delete並rollback。

**檢查方式**

Delete後、rollback前應恰好新增一筆正確audit；rollback後enrollment與audit都恢復。
若使用`NEW`讀delete row，設計不成立。

## 4. 何時不要使用trigger

Trigger是隱含執行的程式，可能讓一個看似簡單的update寫入其他tables。錯誤可能使
原statement失敗，一個trigger也可能啟動另一個trigger，形成難以追蹤的chain。

**Worked comparison**

需求：「enrollment.course_id必須存在於course。」

- Foreign key直接宣告關係、由schema工具可見，且DBMS知道如何維護。
- 自製trigger必須處理enrollment insert/update及course delete/update等多種events；
  少寫一種就可能留下錯誤資料。

因此此需求應使用foreign key。Audit history沒有單一`CHECK`或foreign key可直接
保存old/new values，trigger才有合理用途。

**你來判斷**

比較三個需求：priority只能1–5、刪除student時移除waitlist、保存grade修改歷史。
分別優先選`CHECK`、foreign-key action或trigger，並說明可見性與副作用。

**回饋重點**

不能只回答工具名稱；必須說明該mechanism如何直接表達規則，以及有哪些tables會
被自動修改。

## 5. Recursive CTE：base與recursive terms

固定寫兩次self-join只能找到固定深度。Recursive CTE可重複使用上一輪結果，適合
prerequisites、organization hierarchy、parts hierarchy及reachability。

Lab的direct prerequisites是：

```text
DB201 <- WD120
FT210 <- DB201
ML230 <- DB201
```

箭頭右側是左側course的prerequisite。因此ML230的direct prerequisite是DB201，
indirect prerequisite是WD120。

**Worked example: transitive closure**

```sql
WITH RECURSIVE all_prereq(course_id, prereq_id) AS (
    SELECT course_id, prereq_id
    FROM course_prerequisite

    UNION

    SELECT ap.course_id, cp.prereq_id
    FROM all_prereq AS ap
    JOIN course_prerequisite AS cp
      ON cp.course_id = ap.prereq_id
)
SELECT course_id, prereq_id
FROM all_prereq;
```

- Base term加入所有direct pairs。
- Recursive term把目前的`prereq_id`當成下一個`course_id`，再找到上一層。
- 第一次新增FT210/WD120及ML230/WD120。
- 下一輪沒有新pair；`UNION`移除已存在duplicates，fixed point成立並停止。

完整result為5 pairs：DB201/WD120、FT210/DB201、FT210/WD120、ML230/DB201、
ML230/WD120。

**你來操作**

只查FT210的direct及indirect prerequisites，並加入depth：DB201應為1，WD120為2。

**檢查方式**

先單獨執行base term確認第一層，再執行完整query。若direction顛倒，可能得到「哪些
courses依賴FT210」，那是另一個問題。

## 6. Termination、`UNION`與cycles

Recursive query必須能停止。`UNION`會去除重複的完整result rows；對只含
`(course_id, prereq_id)`的closure，它可避免同一pair無限重新加入。`UNION ALL`
保留duplicates，通常較省deduplication成本，但若graph有cycle且沒有cycle guard，
可能不斷產生rows。

**Worked counterexample**

Depth query的row包含`depth`。即使使用`UNION`，每次走完cycle產生的depth不同，
完整row仍不重複，所以不能只靠deduplication停止。可採用的策略包括：

- Data constraint或application rule禁止cycle。
- 在recursive state保存visited path，拒絕已出現node。
- 在需求允許時設定明確maximum depth，但這只限制結果，不證明graph無cycle。

本章lab的depth example使用已知acyclic sample及`UNION ALL`，不能推廣成任意graph
都安全。

**你來操作**

在savepoint內加入WD120依賴ML230形成cycle。不要直接執行未設上限的`UNION ALL`
depth query；先預測closure query會多出哪些pairs，再rollback。

**回饋重點**

答案必須以recursive row的完整columns判斷是否重複，不能只說`UNION`永遠安全。

## 7. Ranking functions與ties

Window function使用`OVER(...)`在相關rows上計算，但保留每個input row。Lab先取每位
student的best score：S101=92、S102=92、S103=84、S104=84。

**Worked example**

```sql
WITH best_score AS (
    SELECT student_id, MAX(score) AS best_score
    FROM sql_practice_score
    GROUP BY student_id
)
SELECT student_id,
       best_score,
       RANK() OVER (ORDER BY best_score DESC) AS score_rank,
       DENSE_RANK() OVER (ORDER BY best_score DESC) AS dense_score_rank,
       ROW_NUMBER() OVER (
           ORDER BY best_score DESC, student_id
       ) AS display_row
FROM best_score;
```

| student | score | `RANK` | `DENSE_RANK` | `ROW_NUMBER` |
|---|---:|---:|---:|---:|
| S101 | 92 | 1 | 1 | 1 |
| S102 | 92 | 1 | 1 | 2 |
| S103 | 84 | 3 | 2 | 3 |
| S104 | 84 | 3 | 2 | 4 |

`RANK`在ties後留gap；`DENSE_RANK`不留gap；`ROW_NUMBER`每row都不同。為使
`ROW_NUMBER`可重現，example加入`student_id`作tie-breaker。Window內的`ORDER BY`
定義計算順序；final display仍應有outer `ORDER BY`。

**你來判斷**

若S103提高到92，預測四位student的三種numbering。說明下一個`RANK`為何是4，並
指出三位92的deterministic display order由哪個column決定。

**檢查方式**

先把best-score relation寫出來，再計算ties。不能以目前未明列的physical row order
決定`ROW_NUMBER`。

## 8. `PARTITION BY`與window frame

`PARTITION BY`將window calculation分組，但不把detail rows合併。`ORDER BY`定義
partition內順序；frame定義current row計算時包含哪些rows。

**Worked example: running average**

```sql
SELECT student_id,
       attempt_no,
       score,
       ROUND(
           AVG(score) OVER (
               PARTITION BY student_id
               ORDER BY attempt_no
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ),
           1
       ) AS running_average
FROM sql_practice_score;
```

S101 attempt 1的average是78；attempt 2包含78與92，所以是85。S104依序是70及77。
每位student重新開始，總result仍有6 rows。若改用`GROUP BY student_id`，每位學生只
剩一個summary row，已不是running result。

**你來操作**

把frame改成`ROWS BETWEEN 1 PRECEDING AND CURRENT ROW`，計算最多兩次attempt的
moving average。再加入第三次attempt來區分running與two-row moving window。

**檢查方式**

第三次moving average只能使用attempt 2與3；running average會使用1、2、3。必須
明列`ROWS` frame，避免依賴DBMS的default frame。

## 9. Conditional aggregation與cross-tab（短示範）

Cross-tab將一個category的values轉成result columns。SQL Server及Oracle等DBMS有
各自的`PIVOT` syntax；本課用basic SQL的conditional aggregation建立固定兩欄。

**Worked example**

```sql
SELECT student_id,
       MAX(CASE WHEN attempt_no = 1 THEN score END) AS attempt_1,
       MAX(CASE WHEN attempt_no = 2 THEN score END) AS attempt_2
FROM sql_practice_score
GROUP BY student_id
ORDER BY student_id;
```

S101得到78與92；只有一次attempt的S102與S103在`attempt_2`是`NULL`。每個student與
attempt number由primary key保證最多一row，因此`MAX`只負責把該value聚合到一格，
不是在多筆衝突資料中任意選最高分。

**你來操作**

加入`best_score`欄，並說明它應使用全部attempts，不能只取目前顯示的兩欄。再新增
attempt 3，觀察固定cross-tab不會自動多一個column。

**檢查方式**

Best score應分別為92、92、84、84。若category數量動態變化，固定SQL不能自動建立
新columns，需要application或DBMS-specific dynamic pivot；本章不要求。

## 補充定位

- `ROLLUP(a, b)`產生`(a,b)`、`(a)`及grand total等prefix groupings。
- `CUBE(a, b)`產生所列attributes的所有subsets，結果可能快速增加。
- Rollup/cube產生的`NULL`表示某層aggregation，不一定是base data中的unknown；支援
  的DBMS可用`GROUPING()`區分。
- 專屬pivot、rollup及cube syntax未在SQLite執行，不列入Exam 2主要操作題。

## 課堂活動與Class Performance

每組比較三份AI產生的database logic：一份用trigger重做foreign key、一份recursive
CTE沒有termination說明、一份把ties全部用`ROW_NUMBER`當成rank。各組提交修正版
與理由；個人排序時使用：

1. Mechanism是否符合需求，且副作用可觀察。
2. Recursive query是否能說明base、每輪新增rows及停止條件。
3. Ranking是否正確處理ties及deterministic order。
4. Window partition、order及frame是否完整。
5. 是否把未執行的DBMS-specific code誤寫成已驗證。

Peer rank不直接計分。個人保存routine contract、trigger before/after evidence、
recursive iterations、ranking prediction及教師回饋後修正版。

## 常見錯誤

| 錯誤 | 影響 | 修正方式 |
|---|---|---|
| 把reference routine當成SQLite已執行 | 驗證聲明不實 | 分開記錄logic result與routine installation |
| Function與procedure都只寫成「一段程式」 | Caller contract不清楚 | 明列input、return/output及啟動方式 |
| Trigger condition用`<>`比較nullable values | `NULL`變更可能漏記 | 使用目標DBMS的null-safe comparison |
| 用trigger重做declarative constraint | Events容易漏寫且規則較難發現 | 優先使用PK/FK/UNIQUE/CHECK |
| Recursive term連接方向錯誤 | 回答反向reachability問題 | 逐輪列出input及new rows |
| `UNION ALL`遇cycle無guard | 不停止或超過recursion limit | Deduplicate適合的state或明確cycle detection |
| 把`ROW_NUMBER`當成tie-aware rank | 同分被強迫排成不同名次 | 依需求使用`RANK`或`DENSE_RANK` |
| Window `ORDER BY`當成final display order | Output順序不保證 | 另加outer `ORDER BY` |
| 省略frame卻假設running rows | DBMS default可能不同 | 明列`ROWS BETWEEN ...` |

## 本章總結與下一章

- Function回傳value，procedure由caller明確啟動工作，trigger由database event自動
  執行；三者不可只依syntax長短選擇。
- Trigger適合audit等需要old/new transition values的工作，但declarative constraint
  能直接表達時應優先使用constraint。
- Recursive CTE由base與recursive terms反覆求值到fixed point；cycles與完整row的
  duplicate定義會影響termination。
- Ranking functions對ties的處理不同；window partition及frame決定每列計算使用的
  rows。
- Conditional aggregation能建立固定categories的cross-tab，但不會自動因新category
  產生新columns。

Ch6將回到database design：先從business rules辨識entities、attributes、relationships
及cardinalities，再映射成relations。Ch5的程式不能補救一個沒有正確表達business
rules的schema。

## 課後接續內容

1. 完成lab P1–P9並保存prediction與output。
2. 為audit trigger畫出原statement、trigger condition、trigger action及rollback後
   state的順序。
3. 手算FT210 recursive query的每輪new rows，再與SQL output比較。
4. 用同一組scores解釋三種ranking及一個window frame，不只貼執行結果。
