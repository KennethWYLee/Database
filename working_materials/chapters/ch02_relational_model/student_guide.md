# Chapter 2: Introduction to the Relational Model

## 本章核心問題

資料表不只是畫出來像格子的資料。要讓不同資料表能被正確查詢與連結，我們必須
知道每一列代表什麼、哪些欄位能識別一列、不同資料表如何維持一致，以及如何用
一組可組合的運算描述查詢需求。

## 授課摘要

| 教學內容 | 完整範例與練習 | 學習證據 |
|---|---|---|
| relation、tuple、attribute、domain、schema與instance | course-registration relations的結構判斷 | schema identification sheet |
| primary/candidate/foreign keys與schema diagram | 比較candidate keys並沿foreign key連結relations | key map與判斷理由 |
| 核心relational algebra | 對小型relations執行selection、projection、product、join與set operations | 每一步的result relation |

下一章會把本章的查詢想法寫成SQL。本章先專注於資料結構與查詢邏輯，不要求
記憶SQL語法。Assignment、rename及複雜equivalence推導保留完整範例，但作課後
延伸，不列入Exam 1主要操作題。

## 先備知識

- 能閱讀一般二維資料表。
- 知道集合中相同元素只算一次。
- 能使用等於、不等於、且、或等條件。
- 能依照明確規則逐步篩選與整理資料。

## 學習目標

完成本章後，你應能：

1. 在一個資料表中指出relation、tuple、attribute、domain及relation instance。
2. 說明schema與instance的差別。
3. 根據business rules判斷superkey、candidate key、primary key及composite key。
4. 指出foreign key的referencing relation與referenced relation，並判斷資料是否
   違反參照要求。
5. 閱讀schema diagram並沿著foreign key找出資料表之間的連結。
6. 區分imperative、functional及declarative query descriptions。
7. 對小型relation instance執行selection、projection、Cartesian product、
   theta join、union、intersection及set difference。
8. 比較兩個簡單relational-algebra expressions是否表達相同查詢目的。

## 本章使用的資料

以下資料是本課自建的course-registration例子。這些表格會持續用來解釋本章的
概念。

### `department`

| dept_code | dept_name | building |
|---|---|---|
| DES | Digital Design | Hong Hall |
| FIN | Finance | Cheng Hall |
| IM | Information Management | Hong Hall |

### `student`

| student_id | email | student_name | dept_code |
|---|---|---|---|
| S101 | an.chen@example.edu | An Chen | IM |
| S102 | bea.lin@example.edu | Bea Lin | FIN |
| S103 | kai.wu@example.edu | Kai Wu | IM |
| S104 | mira.ho@example.edu | Mira Ho | DES |

### `course`

| course_id | title | dept_code | credits |
|---|---|---|---:|
| DB201 | Database Management | IM | 3 |
| FT210 | Financial Technology | FIN | 3 |
| ML230 | Machine Learning | IM | 3 |
| WD120 | Web Design | DES | 2 |

### `enrollment`

| student_id | course_id | term | grade |
|---|---|---|---|
| S101 | DB201 | 115-1 | A |
| S101 | FT210 | 115-1 | B+ |
| S102 | FT210 | 115-1 | A- |
| S103 | DB201 | 115-1 | B |
| S103 | ML230 | 115-1 | A |
| S104 | WD120 | 115-1 | A- |

資料設計採用下列business rules：

- 每位學生有唯一且不變的`student_id`。
- 每個`email`只屬於一位學生。
- 姓名可以重複。
- 每個department及course各有唯一代碼。
- 同一位學生在同一學期只能對同一課程有一筆enrollment紀錄。
- `student.dept_code`與`course.dept_code`必須對應既有department。
- `enrollment.student_id`與`enrollment.course_id`必須對應既有student與course。

## 資料表、schema與keys

### 1. Relation、tuple及attribute

在relational model中：

- **relation**對應一個資料表。
- **tuple**對應資料表中的一列。
- **attribute**對應資料表中的一欄。
- **relation instance**是某一時間點實際存在的全部tuples。

以`student`為例，`student`是relation，`student_id`是attribute，而
`(S101, an.chen@example.edu, An Chen, IM)`是一個tuple。目前表中的四列合在
一起，構成現在的relation instance。

**Worked example**

問題：`course` relation目前有幾個attributes及幾個tuples？

判讀步驟：

1. 先看column headers：`course_id`、`title`、`dept_code`、`credits`，所以有
   4個attributes。
2. 再計算實際資料列：DB201、FT210、ML230、WD120，所以目前instance有4個
   tuples。
3. 若明天新增一門課，tuple數量會改變，但attributes不一定改變。

**你來判斷**

在`enrollment`中指出relation名稱、全部attributes，以及代表「S103修讀ML230」
的tuple。你的答案必須清楚區分attribute名稱與attribute value。

### 2. Domain、atomic value、tuple順序與duplicates

每個attribute都有允許值的集合，稱為**domain**。例如，依本例的規則，
`course.credits`只能是1到6的整數。Domain不只是目前已出現的值，而是允許出現
的值。

當一個值在目前資料使用方式中被視為不可再分割的單位，它就是atomic value。
Atomicity取決於資料如何使用。例如：

- 若系統只需要顯示完整電話號碼，單一電話字串可被當成一個值。
- 若同一欄存放`0912..., 0933...`兩個電話，系統無法把每支電話當成獨立值，
  這不適合本章的relation結構。
- 比較清楚的設計是建立`student_phone(student_id, phone_number)`，每支電話一列。

Formal relational model把relation視為tuple的set，因此tuple沒有固定順序，也不
包含完全相同的duplicate tuples。實際SQL table可能允許duplicates；這項差異會
在Ch3配合`DISTINCT`再次處理。

`NULL`用來表示目前沒有一般attribute value可填入，例如未知或不存在。本章只先
辨識這個情況；`NULL`對比較與查詢的完整影響放在Ch3。

**Worked example**

問題：把`student`的四列上下交換，relation是否改變？

答案：沒有。只要tuples與attribute values相同，顯示順序不改變formal relation。
如果使用者要求按照姓名排序，那是查詢結果的顯示要求，不是relation本身具有順序。

**你來判斷**

有人在`course`新增一列與DB201完全相同的資料。分別說明formal relational model
與一般未設限制的SQL table會如何看待這件事。答案應提到set與duplicates。

### 3. Schema與instance

**Relation schema**描述relation的邏輯結構，包括名稱、attributes、domains及已
定義的constraints。**Relation instance**則是某個時間點實際儲存的tuples。

本例的schema可以寫成：

```text
student(student_id, email, student_name, dept_code)
```

**Worked example**

情境A：新增學生S105，但仍使用原來四個attributes。

- 改變：instance。
- 不必改變：schema。

情境B：新增`admission_year` attribute。

- 改變：schema。
- 所有既有tuples如何取得新attribute value，也必須另行決定。

**你來判斷**

將S102的`dept_code`從FIN改為IM，是schema change還是instance change？寫出判斷
理由，不要只寫答案。

### 4. Superkey、candidate key與primary key

Key是schema與business rules的property，不能只看目前資料剛好沒有重複就決定。

- **superkey**：一組能保證唯一識別tuple的attributes，可以含有多餘attribute。
- **candidate key**：最小的superkey；移除其中任何attribute後就不能再保證唯一。
- **primary key**：設計者從candidate keys中選出的主要識別方式。
- **composite key**：由兩個以上attributes共同組成的key。

**Worked example 1：`student`**

依business rules，`{student_id}`與`{email}`都能唯一識別學生，而且不能再刪除任何
attribute，因此兩者都是candidate keys。`{student_id, student_name}`也能唯一識別
學生，但`student_name`是多餘的，所以它是superkey而不是candidate key。本例選擇
`student_id`作primary key。

目前四位學生的姓名剛好不同，仍不能據此宣稱`{student_name}`是candidate key，
因為business rules允許同名學生。

**Worked example 2：`enrollment`**

`student_id`不能單獨識別tuple，因為S101修了兩門課。`course_id`也不行，因為
DB201有兩位學生。依本例規則，`{student_id, course_id, term}`共同識別一筆修課
紀錄，因此它是composite primary key。

**你來判斷**

比較下列三個`student` primary-key提案：

1. `student_name`
2. `email`
3. `student_id`

先判斷哪些是candidate keys，再從穩定性、長度、是否可能變更及是否具有業務意義
說明你會選哪一個作primary key。這是一個需要理由的設計問題，不以班級投票結果
決定技術正確性。

### 5. Foreign key與參照要求

**Foreign key**位於referencing relation，它的值必須對應referenced relation的
primary key。這項限制避免資料指向不存在的對象。

**Worked example**

`student.dept_code`是foreign key，referencing relation是`student`，referenced
relation是`department`。

- 新增`(S105, ..., LAW)`會失敗，因為`department`沒有dept_code `LAW`。
- 若先新增LAW department，再新增S105，參照要求可以成立。
- 若仍有學生的dept_code是IM，直接刪除IM department會破壞參照要求；DBMS應依
  constraint設定拒絕或執行明確的相關動作，不能默默留下無對應資料。

Foreign key的attributes不必在referencing relation中唯一。例如多位學生可以同屬
IM；被參照的`department.dept_code`才是department的primary key。

**你來判斷**

指出`enrollment`的兩組foreign keys。對每一組寫出referencing attributes、
referenced relation與referenced primary key。

### 6. Schema diagram

Schema diagram顯示relations、attributes、primary keys及foreign-key方向。它描述
資料結構，不等同於Ch6使用business entities與relationships建模的E-R diagram。

本章例子的簡化schema diagram如下：

```text
department
  PK dept_code
     dept_name [candidate key]
     building
       ^
       | student.dept_code, course.dept_code

student                              course
  PK student_id                        PK course_id
  CK email                             FK dept_code -> department.dept_code
     student_name                         title
  FK dept_code -> department.dept_code    credits
       ^                                  ^
       |                                  |
       +---------- enrollment ------------+
                    PK/FK student_id -> student.student_id
                    PK/FK course_id  -> course.course_id
                    PK    term
                          grade
```

**Worked example**

問題：如何從`enrollment`中的S101、DB201找到學生姓名與開課系所名稱？

1. 沿`enrollment.student_id`到`student.student_id`，取得An Chen。
2. 沿`enrollment.course_id`到`course.course_id`，取得DB201的`dept_code` IM。
3. 沿`course.dept_code`到`department.dept_code`，取得Information Management。

**本段應保存的學習證據**

提交一張個人schema/key判斷表，至少包含：

- 四個relations的primary key。
- 所有foreign keys及箭頭方向。
- `student`的candidate keys與一個不是candidate key的superkey。
- 一項可能違反參照要求的資料修改及理由。

## Relational query languages與relational algebra

### 7. Query描述方式

Query language讓使用者向database要求資料。教科書區分三種描述方式：

- **imperative**：指定一系列會更新state的操作。
- **functional**：把計算寫成functions的組合；functions本身不更新program state。
- **declarative**：描述想得到的資料，不指定取得資料的實際步驟。

本章的relational algebra依第7版教科書分類為functional query language。SQL混合
多種特性，但查詢通常以declarative方式表達。資料庫系統如何選擇執行方式，會在
Ch15與Ch16再學習。

**Worked example**

需求：「找出所有IM學生的姓名。」

- Declarative description：我要dept_code為IM的學生姓名。
- Relational-algebra expression：
  `Π_student_name(σ_dept_code='IM'(student))`
- DBMS實際逐頁讀取、使用index或採用其他plan，不由這句需求直接指定。

**你來判斷**

有人說：「先從第一列開始，逐列檢查dept_code，符合IM就把姓名加入結果。」這段話
比較接近哪一種描述？再說明它與只描述所需結果有何不同。

### 8. Relational algebra的輸入、輸出與composition

Relational-algebra operation接收一個或兩個relations，輸出仍是relation。因此一個
operation的結果可以成為下一個operation的輸入。這項性質讓簡單operations能組合
成較完整的expression。

| Operation | Symbol | 主要問題 |
|---|---|---|
| Selection | `σ` | 保留哪些tuples？ |
| Projection | `Π` | 保留哪些attributes？ |
| Cartesian product | `×` | 兩邊所有tuple combinations是什麼？ |
| Theta join | `⋈_θ` | 哪些跨relation combinations符合連結條件？ |
| Union | `∪` | 在左邊、右邊或兩邊的tuples有哪些？ |
| Intersection | `∩` | 同時在兩邊的tuples有哪些？ |
| Set difference | `−` | 在左邊但不在右邊的tuples有哪些？ |
| Assignment | `←` | 如何把中間結果暫時命名？ |
| Rename | `ρ` | 如何替relation或attributes改名以避免混淆？ |

Selection、projection及rename是unary operations；product、join及三個set operations
是binary operations。

### 9. Selection

Selection保留滿足predicate的tuples，attributes不變：

```text
σ_dept_code='IM'(student)
```

**Worked example**

逐列檢查`student.dept_code`，S101與S103符合IM，因此結果為：

| student_id | email | student_name | dept_code |
|---|---|---|---|
| S101 | an.chen@example.edu | An Chen | IM |
| S103 | kai.wu@example.edu | Kai Wu | IM |

Selection可以使用`=`, `≠`, `<`, `≤`, `>`, `≥`，也可以用`∧`, `∨`, `¬`組合條件。

**你來判斷**

先預測`σ_dept_code='IM' ∧ student_id≠'S101'(student)`的結果，再說明每個被排除
tuple不符合哪一項predicate。

### 10. Projection

Projection保留指定attributes，其他attributes被移除。因formal relation是set，
projection造成的duplicate tuples會被消除：

```text
Π_dept_code(student)
```

**Worked example**

原始四個dept_code values是IM、FIN、IM、DES。Projection後IM只保留一次：

| dept_code |
|---|
| DES |
| FIN |
| IM |

結果顯示順序不影響relation。本表排序只是方便閱讀。

**你來判斷**

預測`Π_building(department)`。答案必須處理Hong Hall重複出現的情況。

### 11. Composition

要找IM學生的姓名，可以先selection，再把結果交給projection：

```text
Π_student_name(σ_dept_code='IM'(student))
```

**Worked example**

1. 內層selection留下S101與S103的完整tuples。
2. 外層projection只保留`student_name`。
3. 結果是`{An Chen, Kai Wu}`。

**你來判斷**

寫出「找出3學分課程的course_id與title」的expression，並清楚標示哪一個
operation先執行。

### 12. Cartesian product

`r × s`把r的每個tuple與s的每個tuple配對。若r有m個tuples、s有n個tuples，
結果有`m × n`個tuples。

**Worked example**

取`{S101, S102}`與`{DB201, FT210}`作Cartesian product：

| student_id | course_id |
|---|---|
| S101 | DB201 |
| S101 | FT210 |
| S102 | DB201 |
| S102 | FT210 |

這四個combinations不代表四筆真實修課紀錄。Cartesian product只列出所有可能
配對，還沒有使用連結條件。

**你來判斷**

若完整`student`有4個tuples、完整`course`有4個tuples，`student × course`有幾個
tuples？再說明為何不能把全部結果直接解讀成修課事實。

### 13. Theta join

Theta join將Cartesian product與selection合併：

```text
r ⋈_θ s = σ_θ(r × s)
```

**Worked example**

找出每位學生實際修讀的課程：

```text
student ⋈_student.student_id=enrollment.student_id enrollment
```

連結條件只保留兩邊`student_id`相等的combinations。再project姓名與course_id：

```text
Π_student_name,course_id(
  student ⋈_student.student_id=enrollment.student_id enrollment
)
```

結果為：

| student_name | course_id |
|---|---|
| An Chen | DB201 |
| An Chen | FT210 |
| Bea Lin | FT210 |
| Kai Wu | DB201 |
| Kai Wu | ML230 |
| Mira Ho | WD120 |

**常見錯誤**

省略join predicate會得到`student × enrollment`的24個combinations，其中多數不是
真實修課關係。寫join時必須能指出兩邊用來連結的attributes及理由。

**你來判斷**

寫出「找出course title及其department name」所需的兩個relations與join
predicate。先不用寫完整expression，但必須說明為何這兩個attributes能連結。

### 14. Union、intersection及set difference

三個set operations要求兩個輸入relations compatible：attribute數量相同，而且
對應位置的domains相容。

定義兩個只有`student_id`的relations：

```text
A = DB201的學生 = {S101, S103}
B = FT210的學生 = {S101, S102}
```

**Worked example**

| Expression | 問題 | 結果 |
|---|---|---|
| `A ∪ B` | 修DB201或FT210或兩者 | `{S101, S102, S103}` |
| `A ∩ B` | 同時修DB201與FT210 | `{S101}` |
| `A − B` | 修DB201但沒有修FT210 | `{S103}` |
| `B − A` | 修FT210但沒有修DB201 | `{S102}` |

Set difference有方向，`A − B`通常不等於`B − A`。`student ∪ course`沒有意義，
因為兩個relations的arity及attribute domains不相容。

**你來判斷**

令C為修ML230的學生集合。預測`A ∪ C`、`A ∩ C`與`C − A`。每個答案都要先寫
出C的內容。

### 15. Assignment（課後延伸）

Assignment把中間結果指定給temporary relation variable，讓長expression較容易
閱讀。它不增加relational algebra能表達的查詢種類。

**Worked example**

```text
db_students ← Π_student_id(σ_course_id='DB201'(enrollment))
fintech_students ← Π_student_id(σ_course_id='FT210'(enrollment))
db_students ∩ fintech_students
```

前兩行建立暫時名稱，最後一行得到`{S101}`。這些temporary variables不是對永久
database relations的修改。

**你來判斷**

使用兩個temporary relation variables重寫「修DB201或ML230的學生」。變數名稱
應能反映內容，不要只寫`A`與`B`。

### 16. Rename（課後延伸）

當同一個relation在expression中出現兩次，需要不同名稱來區分attributes：

```text
ρ_s1(student)
ρ_s2(student)
```

**Worked example**

找出同系但不是同一人的student pairs：

```text
Π_s1.student_name,s2.student_name(
  σ_s1.dept_code=s2.dept_code ∧ s1.student_id<s2.student_id(
    ρ_s1(student) × ρ_s2(student)
  )
)
```

結果是`(An Chen, Kai Wu)`。條件`s1.student_id < s2.student_id`同時移除自己和自己
配對，以及`(Kai Wu, An Chen)`這種反向重複pair。

**你來判斷**

若只保留`s1.dept_code=s2.dept_code`，結果還會包含哪兩類不需要的pairs？

### 17. Equivalent queries（簡單比較；形式推導作課後延伸）

兩個expressions寫法不同，但若對每個合法database instance都產生相同結果，才稱
為equivalent。只在目前四列資料上剛好相同，不足以證明equivalence。

**Worked example**

以下兩個expressions都找出IM學生的修課紀錄：

```text
Q1 = σ_student.dept_code='IM'(
       student ⋈_student.student_id=enrollment.student_id enrollment
     )

Q2 = (σ_dept_code='IM'(student))
     ⋈_student.student_id=enrollment.student_id enrollment
```

Q1先join再filter，Q2先filter student再join。在此predicate只使用`student`的
attribute，而且join不會改變該attribute value，因此兩者結果相同。Ch16會進一步
討論DBMS如何利用equivalent expressions尋找較合適的execution plan。

**你來判斷**

有人把Q2的predicate改為`course_id='DB201'`，卻仍放在`student`的selection中。
說明這個expression為何無法成立，並指出predicate應套用在哪一個relation。

## SQLite操作與結果預測

本章附有：

- `course_registration_setup.sql`：建立本章schema與sample data。
- `student_lab.sql`：重現本章的relations與relational-algebra results。

SQL只是用來驗證結果。Ch2不要求你背SQL語法。每次執行前先記錄：

| Example | 我預測的attributes | 我預測的tuple數 | 實際結果 | 差異原因 |
|---|---|---:|---|---|
| Selection | | | | |
| Projection | | | | |
| Cartesian product | | | | |
| Join | | | | |
| Union | | | | |
| Intersection | | | | |
| Set difference | | | | |

Lab中的`ORDER BY`只讓畫面輸出固定；它不表示formal relation本身有tuple順序。
Projection對應的SQL使用`DISTINCT`，因為formal relational algebra會移除duplicates，
而SQL預設不一定如此。

## 課堂討論與個人修正

各組比較三個`student` primary-key提案：`student_name`、`email`、`student_id`。
回答必須使用下列判斷依據：

- 是否依business rules保證unique。
- 是否minimal。
- 是否可能改變。
- 是否過長或包含不必要attributes。
- 是否會讓其他relations的foreign keys難以使用。

匿名展示各組理由後，每位學生完整排列所有回答。排序結果不直接計分；你必須
保存自己的初始判斷、排序理由，以及教師回饋後的個人修正版，作為Class
Performance的一部分。

## 常見錯誤總表

| 錯誤 | 為什麼不正確 | 檢查方式 |
|---|---|---|
| 把目前沒有重複的attribute直接當key | Key要由business rules保證 | 想像加入同名或相同值的新tuple |
| 把所有superkeys都叫candidate keys | Candidate key必須minimal | 逐一移除attribute檢查unique是否仍成立 |
| 把foreign key畫反 | Arrow應從referencing attributes指向referenced key | 問「哪一邊的值依賴另一邊先存在？」 |
| 把schema diagram當E-R diagram | 兩者目的與notation不同 | 確認圖中是relations/attributes還是entities/relationships |
| 把selection與projection混淆 | Selection選tuples；projection選attributes | 問自己正在減少rows還是columns |
| 忘記projection會移除duplicates | Formal relation是set | 列出投影前values再去重 |
| 把Cartesian product當成真實關係 | Product產生所有可能pairs | 檢查是否有join predicate |
| 忽略set-operation compatibility | 不相容的tuples不能直接比較 | 先檢查arity與對應domains |
| 以一份sample data證明equivalence | Equivalence要求所有合法instances結果相同 | 用business rules推理或找counterexample |

## 本章總結

- Relation由attributes與tuples構成；instance是特定時間點的內容。
- Schema描述較穩定的邏輯結構與constraints。
- Candidate key是minimal superkey；primary key是被選定的candidate key。
- Foreign key讓referencing relation指向referenced relation的key。
- Schema diagram呈現relations、attributes與key constraints。
- Relational algebra以relation為輸入與輸出，所以operations可以composition。
- Selection選tuples，projection選attributes，join保留符合跨relation predicate的
  combinations。
- Union、intersection及set difference需要compatible relations。
- Assignment讓中間結果易讀，rename讓同一relation的不同用途能被區分。
- Equivalent expressions連接到後續的SQL及query optimization。

下一章將把selection、projection、set operations及資料修改轉成可執行SQL，並處理
formal relation與SQL table在duplicates及`NULL`上的重要差異。
