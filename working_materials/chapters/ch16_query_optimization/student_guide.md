# Chapter 16: Query Optimization

Query optimizer要在保持SQL結果語意的前提下，從equivalent expressions、access paths、
join orders及physical operators中選擇estimated cost較低的plan。本章不把heuristic當成
永遠正確的口訣，也不要求手算完整cost model或dynamic-programming optimizer。

搭配檔案：`student_lab.sql`。

## 與前章的關係

Ch15已區分logical expression與physical plan，並讀過scan、index search及join。Ch16進一步
回答：哪些rewrites保持結果、optimizer以哪些catalog statistics估計rows，以及如何避免從
compact `EXPLAIN QUERY PLAN`過度推論。

## 學習目標

完成本章後，你應能：

1. 定義expression equivalence，並以所有legal instances而非單一sample判斷。
2. 正確使用selection cascade、selection pushdown、projection pushdown及inner-join reorder。
3. 用outer-join counterexample拒絕不成立的rewrite。
4. 說明tuple counts、distinct values、indexes及histograms在cost estimation的用途。
5. 計算簡單equality selectivity estimate並指出uniform/independence assumptions。
6. 比較estimated與actual cardinality，辨識skew及stale statistics風險。
7. 執行`ANALYZE`與`EXPLAIN QUERY PLAN`，讀取join order及access paths。
8. 比較equivalent SQL的results與plans，再提出有證據限制的結論。

## 1. What query optimization does

Optimizer通常進行三類工作：產生logically equivalent expressions、為operators選擇physical
algorithms/access paths，以及用statistics估計cost並選plan。Estimated lowest-cost plan不保證
是actual fastest，因statistics與assumptions可能不準；但沒有估計就無法在大量alternatives
中合理選擇。

### Worked example

對student、enrollment及course的query，optimizer可考慮：

```text
(filtered Student join Enrollment) join filtered Course
filtered Student join (Enrollment join filtered Course)
```

並為每個input選SCAN或SEARCH。只要inner joins的conditions及bag/set semantics被正確保留，
兩個logical orders可得到相同結果，但intermediate rows及physical cost可能不同。

### 你來判斷

把一條三表join改寫成另一個join order時，至少要先確認哪些conditions與output properties？

### 檢查方式

至少包含join predicates、outer versus inner join、duplicates、NULL behavior及required output
columns。只說「join有associativity」而忽略outer join不完整。

## 2. Expression equivalence

兩個relational expressions equivalent，表示對每個legal database instance都產生相同
relation；SQL通常使用multisets，所以duplicates count也必須相同。Sample data上的equal
result是必要檢查，但不能證明所有future legal instances都equivalent；形式規則與constraints
仍然需要。

### Worked example: selection cascade

```text
sigma(dept_id=42 AND credits=5)(R)
equivalent to
sigma(dept_id=42)(sigma(credits=5)(R))
```

兩個predicates都在R上時，先後順序不改變通過兩條件的tuples。這個分解讓optimizer有機會
把每個selection推到只含相關attributes的input。

### 你來操作

在lab中比較`BASE QUERY`與`PUSHDOWN QUERY`：使用雙向`EXCEPT`及row count確認current
instance結果相同，再比較兩份plan。

### 預期與回饋

兩個difference counts都是0，row counts相同；SQLite可能把subqueries flatten後產生相同
plan。不能因此聲稱所有任意SQL subqueries都可安全移除。

## 3. Selection pushdown

若predicate只引用join其中一側E1的attributes，inner join通常可改寫：

```text
sigma(theta1)(E1 join E2)
equivalent to
sigma(theta1)(E1) join E2
```

早期filter可能減少intermediate rows，但equivalence rule只保證結果，不保證rewrite一定
cheaper。若E1很大、filter沒有index，而另一側很小且join index有效，晚一點filter有時反而
cost較低。

### Worked example

本章query把`student.dept_id=42`限制在Student，把`course.credits=5`限制在Course，再與
Enrollment join。這兩個predicates只屬於各自input，因此pushdown保持inner-join語意，並讓
student/course indexes成為optimizer可考慮的access paths。

### 你來判斷

若Student有一億rows、`status='ACTIVE'` match 95%且無status index，而Enrollment只含十筆
目標資料，能否僅憑「selection要早做」宣稱先scan Student最佳？列出要比較的plans。

### 回饋重點

不能。需比較full Student filter scan與先從small Enrollment經join key lookup後再測status，
並使用row estimates及access paths。

## 4. Projection pushdown

早期projection可減少intermediate tuple width，但必須保留final output、join、selection、
grouping及ordering仍需要的attributes。漏掉join key會使後續operation無法執行；SQL
multiset下也要注意是否引入或消除duplicates。

### Worked example

Final output只需`student_id, course_id`，Student側仍需保留`student_id`作join key與
`dept_id`作filter；Course側需`course_id`作join key與`credits`作filter。Filter完成後可讓
intermediate output省略names等未使用columns。

### 你來操作

為`Student JOIN Enrollment JOIN Course`列出每個leaf input在filter前後最少要保留的columns。
故意移除`student_id`，說明哪個join立即失效。

### 檢查方式

Student至少先保留student ID與department ID；filter後仍需student ID。Course同理保留
course ID與credits。答案不能只列final projection。

## 5. Join reorder and Cartesian-product risk

Inner natural/equi joins在正確conditions下可利用commutativity與associativity改變order。
不同order產生的intermediate sizes可能差很多。若先join兩個沒有連接predicate的inputs，
會形成Cartesian product，通常產生大量不必要pairs。

### Worked example

先取得Department 042的100 students，再由Enrollment primary-key prefix找每位student的
5 enrollments，形成約500 rows；之後查Course並測credits。若先將10,000 students與500
courses做沒有predicate的product，會先產生5,000,000 pairs，完全忽略Enrollment提供的
relationships。

### 你來判斷

給定A-B及B-C有join predicates，但A-C沒有，列出兩個不先產生Cartesian product的join
orders，以及一個會先產生product的order。

### 檢查方式

`(A join B) join C`及`A join (B join C)`可先用有效predicate；`(A cross C) join B`先產生
product。仍需確認join type與conditions，不能只看table names。

## 6. Outer join is a semantic boundary

Outer join保留unmatched rows，NULL extension會使某些inner-join equivalences失效。把right
side filter放在`WHERE`通常會移除NULL-extended rows；把它放進`ON`則仍保留left rows，只是
右側不match。

### Worked counterexample

Lab加入Department 101，沒有任何Student：

```sql
-- Query A: filter after left join
FROM department d LEFT JOIN student s ON s.dept_id=d.dept_id
WHERE s.student_id < 3

-- Query B: filter as part of ON
FROM department d LEFT JOIN student s
  ON s.dept_id=d.dept_id AND s.student_id < 3
```

Query A移除Department 101，因`NULL < 3`是UNKNOWN；Query B保留它並輸出NULL student。
因此兩者不是equivalent。

### 你來操作

執行兩個queries及difference checks，指出只存在Query B的row。再把`LEFT JOIN`改成
`INNER JOIN`，重新判斷filter位置。

### 預期與回饋

Department 101/NULL只在ON-filter版本。Inner join版本可安全把只引用Student的condition在
`ON`與`WHERE`間移動，仍要保留相同predicate。

## 7. Catalog statistics and ANALYZE

Optimizer常使用relation tuple/page counts、tuple width、distinct-value counts、index
properties及value-distribution histograms。為每次update同步精確statistics成本太高，因此
statistics可能來自sampling、periodic `ANALYZE`或自動更新，也可能stale。

SQLite的`ANALYZE`會在本lab建立`sqlite_stat1`。其內容比完整教科書catalog簡化，且build
是否支援更細緻histograms依環境而異。不要把SQLite一個stat string當成所有DBMS共同格式。

### Worked example

```sql
ANALYZE;
SELECT tbl, idx, stat FROM sqlite_stat1 ORDER BY tbl, idx;
```

Course、Student及Enrollment index statistics讓planner估計不同access paths。執行大量
insert/delete後若statistics未更新，optimizer可能仍依舊distribution估計。

### 你來操作

執行lab後，找出event-type index的stat。記錄total rows、distinct values及actual COMMON/
RARE counts；說明哪些資訊沒有直接出現在average stat中。

### 檢查方式

Total 10,000、2個types；COMMON 9,900、RARE 100。Average rows per distinct value為5,000，
無法單獨描述這個skew。

## 8. Selectivity, skew, and estimation

若沒有frequent-value或histogram資訊，equality predicate常以uniform assumption估計：

```text
estimated rows = total rows / number of distinct values
selectivity = estimated rows / total rows
```

多條件估計可能再假設conditions independent。這些是近似，不是data law。

### Worked example

Event有10,000 rows及2個distinct types，uniform estimate對任何type都是5,000 rows。Actual：

```text
COMMON: 9,900   estimation error: -4,900
RARE:     100   estimation error: +4,900
```

同一average estimate對兩個values方向相反地失準。Frequent-value counts或histogram可改善，
但SQLite lab不聲稱其build已保存這些細節。

### 你來操作

計算COMMON與RARE的actual selectivity，並說明哪一個query較可能適合secondary index lookup。
再寫出仍需看plan的理由。

### 預期與回饋

COMMON 99%，RARE 1%；RARE較可能受益於index。仍要看projection是否covering、record
placement、cache及optimizer選擇，不能只用percentage保證。

## 9. Practical plan interpretation

`EXPLAIN QUERY PLAN`顯示SQLite選擇的access order及index use；它不提供完整cost unit、
actual rows、buffer hits或其他DBMS的operator details。實務流程：

1. 保存SQL、schema、indexes、row counts及DBMS version。
2. 確認rewrites的results相同。
3. 執行`ANALYZE`並記錄statistics state。
4. 比較plan order、SCAN/SEARCH、index names與temporary work。
5. 把結論限制在目前workload及環境。

### Worked example

Lab中base及pushdown SQL回相同rows。SQLite 3.45.3會flatten subqueries，因此兩份plans可
相同；這是optimizer已辨識equivalence的可觀察結果。它不證明source SQL文字相同，也不
證明其他DBMS一定採同一plan。

### 你來操作

逐行解釋base plan：第一個access是哪張table、使用哪個index、後續join如何找rows。再
指出一項plan沒有提供的actual execution資訊。

### 回饋重點

答案依實際plan，不以預先背的join order代替。缺少資訊可列actual rows per operator、
elapsed time、buffer reads或memory。

## 課堂比較與個人學習證據

各組比較一對看似較快的SQL rewrite。共同回答必須先證明或反駁equivalence，再看statistics
與plan；不能先用style偏好選winner。教師依duplicates、NULL、outer join、row counts及
plan evidence回饋，學生修正。

個人保存：original/rewrite SQL、雙向difference check、statistics snapshot、兩份plans、
actual counts，以及一個不成立rewrite的counterexample。

## 常見錯誤

1. Sample result相同就宣稱所有instances equivalent。
2. 對outer join無條件push down right-side predicate。
3. Projection pushdown漏掉join key。
4. 把「selection early」當成永遠最低cost的定理。
5. 把estimated rows當成actual rows。
6. Statistics更新後未重新取得plan。
7. 只改寫SQL排版，卻聲稱改變algorithm。
8. 使用`EXPLAIN`但沒有確認result equivalence。

## 本章總結

Query optimization先守住equivalence，再利用statistics估計alternatives。Selection/
projection pushdown及join reorder常能降低intermediate work，但適用條件與cost evidence
不可省略。Outer join、duplicates、NULL與skew是最容易讓直覺失效的地方。Ch17將從單一
query plan轉向transaction execution及concurrent schedules。

## 課後接續

- 為一條真實query建立「equivalence -> statistics -> plan -> limits」四段紀錄。
- 完整cost formulas、dynamic programming、optimizer implementation、materialized views及
  advanced optimizations作補充，不列入本課selected Ch16操作考題。
