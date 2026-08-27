# Chapter 6: Database Design Using the E-R Model

## 本章核心問題

前五章大多接受既有schema。本章改問：在建立tables之前，如何從使用者需求判斷
應保存哪些entities、attributes、relationships及constraints？又如何把conceptual
E-R design轉成具有keys與foreign keys的relational schema？

## 授課摘要

| 教學內容 | 完整範例與練習 | 學習證據 |
|---|---|---|
| requirements、entities、attributes、relationships、cardinalities與keys | 從course-registration business rules建立E-R diagram | E-R diagram draft |
| participation、weak entities與design decisions | 比較兩個design choices及其business-rule evidence | annotated diagram |
| 移除conceptual redundancy與E-R-to-relational mapping | 將entities與relationships映射成具備keys及foreign keys的schema | revised diagram與relational schema |

Extended E-R features及alternative notations只作補充，不是Exam 2主要範圍。

## 與前章的關係

Ch2–Ch5使用schema表達keys、foreign keys、queries、constraints與database programs。
E-R model位於更前面的conceptual design階段：先讓domain expert與designer確認
「資料世界如何組成」，再映射到relations。Ch7會使用functional dependencies與
normal forms檢查relational design是否容易產生anomalies。

## 使用案例與檔案

本章使用原創course-registration案例：

- `course_registration_rules.md`：十二條requirements及待確認問題。
- `course_registration_er.svg`／`.png`：conceptual E-R diagram。
- `mapped_schema.sql`：映射後的SQLite schema與sample data。

![Course registration E-R diagram](course_registration_er.png)

圖中使用entity rectangle、relationship diamond與`min..max` cardinality。E-R notation
沒有唯一通用標準；使用其他軟體時必須先查清楚cardinality標在靠近哪一側。不能只
看crow's-foot或數字位置猜語意。

## 學習目標

完成本章後，你應能：

1. 區分requirements、conceptual design、logical design及physical design的產出。
2. 從business rules辨識entity sets、attributes、relationship sets及roles。
3. 分類simple、composite、single-valued、multivalued及derived attributes。
4. 由逐方向問題判斷one-to-one、one-to-many、many-to-one或many-to-many。
5. 使用minimum與maximum表示total/partial participation，避免方向顛倒。
6. 為entity及relationship選擇primary key，並辨識candidate key。
7. 判斷weak entity的owner、identifying relationship與discriminator。
8. 移除因relationship而在conceptual entity中重複的key attributes。
9. 把strong/weak entities、complex attributes及relationships映射為relations。
10. 比較attribute、entity、relationship及n-ary design choices，並用requirements
    支持選擇。

## 從需求到E-R diagram

### 1. Design phases與產出

Database design先了解使用者資料需求，再建立conceptual schema；之後才映射為DBMS
可實作的logical schema，最後決定files與indexes等physical design。

| Phase | 主要問題 | 本案例產出 |
|---|---|---|
| Requirements | 使用者需要保存哪些事實與規則？ | `course_registration_rules.md` |
| Conceptual design | Entities、attributes、relationships及constraints是什麼？ | E-R diagram |
| Logical design | 如何映射成relational schemas及constraints？ | `mapped_schema.sql`的table definitions |
| Physical design | 如何儲存及加速？ | Ch14才決定indexes，不在本章先猜 |

**Worked example**

Requirement 8說：「一門course可以有零到多個sections；每個section恰屬於一門
course。」Conceptual design建立Course、Section及identifies relationship，並標示
`Course 0..*`、`Section 1..1`。Logical design才把`course_id`帶入section relation作
foreign key。現在沒有資料量及query plan證據，因此不在conceptual diagram加入
index決策。

**你來操作**

把「grade必須是允許的代碼」放入適當phase，說明conceptual rule與logical
constraint各自如何呈現。

**檢查方式**

答案應先把grade視為registration的資料規則，再在relational schema用nullable
`CHECK`實作。若只回答「加index」，phase與問題都不相符。

### 2. Redundancy與incompleteness

Bad design常見兩種後果：

- Redundancy：同一事實存多份，修改後可能不一致。
- Incompleteness：某些合法事實無法獨立保存。

**Worked example**

若只建立`section(course_id, title, credits, term, section_no)`，每個section都重複
course title與credits。改title時可能只改一列。尚未開課的新course也沒有section
row可放，除非使用不合理的`NULL` section values。把Course與Section分開並建立
relationship，同時處理redundancy與incompleteness。

**你來判斷**

檢查`student_registration(student_id, student_name, course_id, course_title, grade)`。
指出至少兩個重複事實及一個無法單獨保存的合法事實。

**回饋重點**

必須指出「哪個事實」重複或缺失，不以「table太大」作為判斷理由。

### 3. Entity、entity set與attribute

Entity是可與其他objects區分的real-world object；entity set收集同類entities。
Attribute描述entity的property。Entity可具體或抽象，例如Student與Course都可以是
entities。

**Worked example**

- S101是Student entity；Student是entity set。
- `student_id`、email及name是Student attributes。
- Student entity set的extension是目前實際存在的所有student entities，類似relation
  instance，不等於entity set的設計本身。

`student_id`由學校指派而非使用政府識別碼，避免把不必要的敏感identifier拿來當
database key。

**你來操作**

對Requirement 5辨識一個entity set、一個entity、三個attributes及一個可能的
candidate key。不要把一筆course row稱為entity set。

**檢查方式**

Entity example必須是某一門具體course，例如DB201；entity set是Course；course_id
可作key，title未必unique。

### 4. Complex attributes

Attribute可以有不同structure：

- Composite：可拆成有意義components，例如name拆成first/last name。
- Multivalued：同一entity可有零到多個values，例如phone numbers。
- Derived：由其他資料計算，例如completed credits。
- Single-valued/simple：每個entity一個不可再拆的值。

**Worked example**

Student的`name(first_name,last_name)`是composite。`{phone_number}`是multivalued，
因S101可同時有手機與辦公室電話。`completed_credits`是derived，應從non-failing
enrollments及course credits計算；若同時另存一份，更新grade後可能不同步。

`NULL`可能表示not applicable、missing或unknown，三種語意不完全相同。本案例grade
為`NULL`表示尚未給成績，不代表零分。

**你來判斷**

對student address提出composite components。再比較「一個multivalued phone
attribute」與「Phone entity」：什麼額外requirements會使Phone entity較適合？

**回饋重點**

若需要phone type、owner sharing或location，Phone具有自己的properties或
relationships，較適合作entity；只需多個號碼時multivalued attribute即可。

### 5. Relationship、role與degree

Relationship表示entities之間的association；relationship set收集同類associations。
Relationship本身也可有descriptive attributes。Degree是參與entity sets的數量。

**Worked example**

Student S101 registers for Section DB201/115-1/1是一個relationship instance。
`registers`是binary relationship set，grade是relationship attribute，因它描述特定
student-section pair，不只描述Student或Section。

Course prerequisite是Course與Course的recursive binary relationship。兩次出現的
Course必須標示roles：`course_id`是需要先修的course，`prereq_id`是先修course。

**你來操作**

判斷「某位instructor指導某位student完成某個project」的degree，並為三個roles
命名。再說明拆成三個不受限制的binary relationships可能失去什麼組合資訊。

**檢查方式**

原關係是ternary。答案必須保留完整instructor-student-project combination，不能只
知道各自曾與誰或哪個project相關。

### 6. Mapping cardinalities

Cardinality必須從兩個方向分開問：

1. 固定一個A entity，它最多對應幾個B entities？
2. 固定一個B entity，它最多對應幾個A entities？

**Worked example: Department–Student**

- 固定一個Department，可有多少Students？0到多個。
- 固定一個Student，可有多少major Departments？恰好1個。

因此從Department到Student是one-to-many；從Student到Department是many-to-one。
圖上Department edge標`0..*`，Student edge標`1..1`。

**你來操作**

依Requirements 8及9，分別判斷Course–Section與Student–Section的maximum
cardinality。每個relationship都要回答兩個方向。

**檢查方式**

Course–Section是one-to-many；registers是many-to-many。若只寫「一對多」卻沒有
指出哪一側是one，答案不完整。

### 7. Participation與minimum cardinality

Maximum回答「最多幾個」；minimum回答「是否必須參與」。Minimum 1表示total
participation，minimum 0表示partial participation。

**Worked example**

每個Student必須有一個major Department，所以Student在majors_in是total且`1..1`。
Department即使暫時沒有Students仍可存在，所以Department participation是partial且
`0..*`。Maximum相同不代表minimum相同。

**你來判斷**

若新政策允許新生入學後兩週內尚未決定major，應改哪一個minimum？這會如何影響
logical schema中的`student.dept_code`？

**回饋重點**

Student cardinality會由`1..1`改成`0..1`。Relational mapping若合併relationship，
foreign key需允許`NULL`；不能仍保留`NOT NULL`卻聲稱optional。

### 8. Keys for entities與relationships

Entity set可有superkeys、candidate keys及一個chosen primary key。Relationship key
取決於participating entity keys及cardinality。

**Worked example**

Student以`student_id`為primary key，email是另一candidate key。Registers是M:N，
一個relationship由Student key與Section完整key共同識別：

```text
(student_id, course_id, term, section_no)
```

Grade是descriptive attribute，不需加入key；同一registration的grade可從`NULL`改為
A，而不產生新的relationship instance。

**你來操作**

如果每位Student最多有一位advisor，但一位Instructor可指導多位Students，判斷
advisor relationship的minimal key來自哪一側。

**檢查方式**

Student是many side且每位student最多一個advisor，因此Student primary key已能唯一
識別advisor relationship。若把兩側keys都當primary key，會錯誤允許一位student有
多位advisors。

### 9. Weak entity

Weak entity缺少可獨立形成primary key的attributes，需依賴identifying entity。
Owner primary key加上weak entity discriminator才能識別weak entity；weak entity對
identifying relationship必須total participation，且每個weak entity對應一個owner。

**Worked example**

Section只在特定Course內由`(term, section_no)`辨識。另一門Course可重用相同term與
section number，因此Section完整key是：

```text
(course_id, term, section_no)
```

Diagram以double rectangle表示Section、double diamond表示identifies。`course_id`
不重複列為Section conceptual attribute；它在logical mapping時由owner帶入。

**你來判斷**

若學校改用全球唯一`section_uuid`，Section是否必然不再適合作weak entity？分別從
key sufficiency與existence dependency回答。

**回饋重點**

Globally unique ID使它能技術上成為strong entity，但Section仍在概念上依賴Course
才有意義。選擇需由enterprise semantics支持，不只看是否能增加surrogate key。

## 從E-R diagram到relations

### 10. 移除conceptual redundant attributes

若relationship已表達association，不應同時在entity中重複對方primary key。這是
conceptual model的規則；映射到relations後，foreign-key column可能重新出現。

**Worked counterexample**

若Student entity同時有`dept_code` attribute及majors_in relationship，兩處可能指向
不同Department。Diagram只保留relationship。因每位Student恰好一個Department，
logical mapping把`dept_code NOT NULL`放入student relation，這是relationship的實作，
不是把conceptual duplication加回來。

**你來操作**

檢查Section與Course的identifying relationship。說明為何conceptual Section box不列
`course_id`，但section relation必須有`course_id`。

**檢查方式**

答案需提到owner key同時成為weak entity primary key的一部分及foreign key。

### 11. Mapping entities與complex attributes

Strong entity通常映射為同名relation，entity primary key成為relation primary key。
Composite attribute展開為component columns；multivalued attribute建立separate
relation；derived attribute通常不存成獨立column。

**Worked example: Student**

```text
student(student_id PK, email UNIQUE, first_name, last_name, dept_code FK)
student_phone(student_id FK, phone_number,
              PK(student_id, phone_number))
```

Name展開為兩欄。每個phone value是一row，因此S101有兩個phone rows。Derived
completed credits由query計算，不在student relation保存。

**你來操作**

設計Instructor的composite address與multivalued certification mapping。列出每個
relation的primary key及foreign key。

**檢查方式**

Address components留在Instructor relation；certification另成relation且key至少包含
instructor key與certification value。

### 12. Mapping weak entity

Weak entity relation包含自己的attributes、owner primary key，並建立foreign key指向
owner。Primary key是owner key加discriminator。

**Worked example**

```text
section(course_id FK, term, section_no, room, capacity,
        PK(course_id, term, section_no))
```

`course_id`同時是identifying Course的foreign key及Section primary key的一部分。
Mapped SQL允許DB201在115-1有section 1與2；不允許不存在的Course擁有Section。

**你來操作**

把Course底下的Assignment設計為weak entity，discriminator是assignment_no。列出
relation及key；再指出deadline應放在哪裡。

**檢查方式**

Key包含Course/Section owner的完整key及assignment_no；deadline描述Assignment，
不是identifying relationship。

### 13. Mapping one-to-many與total participation

對A到B的many-to-one relationship，若A是many side且total participation，通常可把
B key作foreign key併入A relation，省去只有keys、沒有descriptive attributes的獨立
relationship relation。

**Worked example**

Every Student has exactly one major Department，因此：

```text
student(..., dept_code NOT NULL FK -> department.dept_code)
```

Every Course也恰由一個Department offered，所以course同樣包含non-null
`dept_code`。Department可有0 courses，不需要在Department放course key list。

**你來判斷**

若Student可有多個majors，是否還能在student放單一`dept_code`？提出新的relationship
relation與primary key。

**檢查方式**

應改為`student_major(student_id, dept_code, PK(student_id,dept_code))`及兩個foreign
keys；student中的單一dept_code無法表示M:N。

### 14. Mapping many-to-many relationship

M:N relationship建立separate relation，包含兩側keys與relationship attributes。
Participating keys通常共同形成primary key。

**Worked example: registers**

```text
enrollment(
  student_id FK,
  course_id, term, section_no FK -> section,
  grade,
  PK(student_id, course_id, term, section_no)
)
```

Grade留在enrollment，因S101在不同sections可以有不同grade。Mapped SQL以composite
foreign key防止enrollment指向不存在的Section。

**你來操作**

映射Course與Course的prerequisite relationship，使用role names避免兩個foreign keys
同名，並加入禁止direct self-prerequisite的constraint。

**檢查方式**

Relation應有`course_id`及`prereq_id`，兩者都reference Course，pair為primary key。
`CHECK(course_id <> prereq_id)`只阻止直接self-loop，不能阻止長cycle。

### 15. Design choices必須由requirements支持

Entity、attribute或relationship並非只看名詞決定。選擇取決於該object是否有自己的
properties、是否需多個values、是否與其他objects建立relationships，以及需要保留
哪種combination。

**Worked comparison: registration**

目前Registration只有grade，可簡潔建模為Student與Section的relationship。若未來每筆
registration有獨立registration ID、payment、approval status及多次appeal records，
Registration成為entity可能更清楚，並分別與Student及Section建立relationships。

**Worked comparison: binary與ternary**

Mother與Father可拆成兩個binary relationships，因不知道father時仍能保存mother。
但Instructor–Student–Project guidance的三者組合若拆成未受限制的pairs，無法知道
哪位instructor帶哪位student做哪個project。

**你來判斷**

針對「每次學生候補都有request time、priority changes及通知紀錄」，比較把Waitlist
當relationship或entity。列出你的決定所需的requirements證據。

**回饋重點**

回答需評估identity、attributes及後續relationships，不以「entity比較專業」作理由。

## Mapped schema驗證

執行`mapped_schema.sql`後，至少檢查：

1. S101可有兩個phone rows，但同一phone pair不能重複。
2. 不存在的Department不能被Student或Course引用。
3. DB201可有同term的section 1與2，但相同complete key不能重複。
4. Enrollment必須同時reference既有Student與完整Section key。
5. Grade可為`NULL`，但不接受未列出的Z。
6. Derived completed credits為S101=6、S102=3、S103=3；S103的ML230尚未給grade，
   不計入completed credits。

這些checks只證明目前SQL mapping與sample requirements相符，不證明所有未來政策都
已涵蓋。例如`CHECK(course_id <> prereq_id)`不能檢查多步prerequisite cycle。

## 課堂活動與Class Performance

各組收到一份AI產生的E-R design，其中混有redundant foreign-key attributes、反向
cardinality、把multivalued assignment marks當成單一relationship attribute，以及
無法保存尚未開課Course的設計。各組提交：

1. 修正後diagram或清楚的textual equivalent。
2. 每項修正對應的business rule。
3. 映射後relations、primary keys及foreign keys。
4. 至少一筆會讓錯誤設計失敗、但正確設計可表示的sample data。

匿名展示後，個人依requirements coverage、cardinality、key correctness、redundancy、
mapping及可驗證sample data排序。Peer rank不直接計分；個人修正版才是證據。

## 常見錯誤

| 錯誤 | 影響 | 檢查方式 |
|---|---|---|
| 從table直接照抄foreign keys進conceptual entity | Relationship重複且可能矛盾 | 先以relationship表達association |
| 只說one-to-many不說方向 | Cardinality可能完全顛倒 | 固定每側entity各問一次 |
| 把maximum 1當成total participation | Optional entity被誤設為必須參與 | 分開判斷minimum與maximum |
| M:N relationship只把一側key放進另一table | 無法表示多個associations | 建立relationship relation與composite key |
| Multivalued attribute放一個逗號字串 | 難以constraint、query及更新單一value | 映射為separate relation |
| Derived attribute與base facts一起儲存 | 更新後可能不一致 | 由query計算或設計明確維護機制 |
| Weak entity只用discriminator當key | 不同owners的values衝突 | Owner key加discriminator |
| 用surrogate key取代所有business constraints | Duplicate business facts仍可能存在 | 保留必要candidate/unique constraints |

## 本章總結與下一章

- Requirements先於diagram；conceptual、logical及physical design回答不同問題。
- E-R model用entities、attributes、relationships及cardinalities描述enterprise。
- Complex attributes、relationship attributes與weak entities都有對應mapping rules。
- Conceptual diagram不重複relationship所代表的foreign-key attribute；logical schema
  依cardinality把foreign key合併或建立separate relation。
- Design choice必須由可保存的事實、constraints及未來需求支持。

Ch7會檢查mapped relations中的functional dependencies、update anomalies及lossless
decomposition，進一步判斷relational design是否為3NF或BCNF。

## 課後接續內容

1. 完成兩週practice並保存business-rule-to-diagram-to-schema mapping。
2. 以一組valid及invalid data驗證每個key與cardinality decision。
3. 選一個可能改變的政策，例如multiple majors，說明conceptual及logical schema需
   修改的地方。
4. 不需學習extended E-R及alternative notation的完整符號；只需知道不同工具的
   notation可能不同，轉讀前要先確認legend。
