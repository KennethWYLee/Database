# Chapter 7: Relational Database Design and Normalization

本章使用functional dependencies檢查relational schema，重點不是背normal form的
名稱，而是回答三個設計問題：哪些facts被重複保存、分解後能不能正確重建，以及
每個nontrivial dependency的determinant是否足以識別一列。

搭配檔案：`student_lab.sql`。請先預測再執行，不要用某一組sample rows的結果代替
business rules。

課堂核心是anomalies、functional dependencies、attribute closure、binary lossless
decomposition、spurious tuples，以及3NF/BCNF的基本判斷。Dependency preservation
用來說明設計取捨；完整theory、canonical cover及分解演算法留作課後延伸。

## 與前章的關係

Ch6從requirements建立E-R model，再映射成relations。若一開始收到的是既有table、
匯入的spreadsheet，或設計中仍混合多種facts，就需要本章的方法檢查schema。Ch7不
取代requirements analysis；functional dependency必須來自穩定的business rule，
不能只從目前資料猜測。

## 先備知識

- relation schema、tuple、primary key、candidate key及foreign key；
- projection與natural join；
- `CREATE TABLE`、`INSERT`、`UPDATE`、`DELETE`及basic joins；
- Ch6的entity、relationship及relational mapping。

## 學習目標

完成本章後，你應能：

1. 說明good relational design如何降低redundancy並保存合法facts。
2. 從一個flattened relation辨識update、insertion及deletion anomalies。
3. 依business rule寫出functional dependency，並用counterexample否定錯誤FD。
4. 計算小型attribute set的closure並判斷superkey與candidate key。
5. 判斷binary decomposition是否lossless，並辨識spurious tuples。
6. 依nontrivial FDs判斷relation是否符合BCNF。
7. 依candidate keys與prime attributes判斷relation是否符合3NF。
8. 以簡單案例說明BCNF、losslessness與dependency preservation之間可能的取捨，
   不要求執行完整分解演算法。

## 1. Good relational design

一個relation應保存同一類facts，並讓合法facts能獨立存在。把Student、Department、
Course與Enrollment全部放在同一個relation會重複姓名、系名、課名與學分，也使「尚
無人選修的course」沒有合理的row可存。table欄位多不是壞設計的充分證據；問題在於
facts的dependencies及其後果。

### Worked example

先考慮：

```text
course_enrollment_record(
  student_id, student_name, dept_code, dept_name,
  course_id, course_title, credits, grade
)
```

Business rules如下：

```text
student_id -> student_name, dept_code
dept_code  -> dept_name
course_id  -> course_title, credits
(student_id, course_id) -> grade
```

`student_name`取決於student，`course_title`取決於course，`grade`才取決於一次
student-course enrollment。因此一列同時保存四類facts。S101選兩門課時，其姓名與
系別被存兩次；十位學生選DB201時，課名與學分會存十次。

### 你來判斷

`employee_project(employee_id, employee_name, project_id, project_name, hours)`中，
若employee ID決定employee name、project ID決定project name，而employee-project
pair決定hours，列出三種facts。說明為何「它有五欄」不是你的判斷依據。

### 檢查方式

答案應區分employee、project及assignment facts，並以determinants及repetition說明，
而不是用欄位數或row數判斷。

## 2. Design anomalies

Anomaly是schema讓一個正常資料操作產生額外問題：

- update anomaly：同一fact有多份，必須修改多列且可能不一致；
- insertion anomaly：某個合法fact必須等另一個fact出現才能保存；
- deletion anomaly：刪除一個fact時意外失去另一個仍需要的fact。

### Worked example

在flattened relation中，IM系名稱出現在每一位IM學生的每一次選課：

1. 若只把S101其中一列的`dept_name`改成`Information Systems`，同一
   `dept_code='IM'`會出現兩個系名，形成update anomaly。
2. 新課程AI301尚無人選修時，沒有student與grade可填；為了存course而造一個假的
   enrollment會形成insertion anomaly。
3. 若DB201只有S103選修，刪除該enrollment也會刪掉DB201的title與credits，形成
   deletion anomaly。

`student_lab.sql`用transaction展示第一個問題並`ROLLBACK`，避免故意製造的不一致
留在後續練習。

### 你來操作

執行lab中的Part A。找出每個`dept_code`有幾個distinct names，再說明若結果目前都
是1，為何仍不能證明未來不會出現update anomaly。

### 預期與回饋

正常sample data中每個code只有一個name；temporary update後IM有兩個names。FD是對
所有legal instances的規則，而不是目前instance的巧合。

## 3. Functional dependencies

對schema R，`alpha -> beta`表示：在每一個legal relation instance中，只要兩個tuples
在alpha所有attributes相同，它們在beta也必須相同。alpha稱為determinant。定義FD時
假設一般數學的equality，不使用SQL `NULL`的three-valued logic。

若`beta`是`alpha`的subset，dependency是trivial，例如
`(student_id, course_id) -> student_id`。若`K -> R`，K是superkey；若K是minimal
superkey，K是candidate key。

### Worked example: rule and counterexample

Business rule「每個student ID只代表一位student」支持：

```text
student_id -> student_name, dept_code
```

但目前資料碰巧每位student只選一門課，不能支持：

```text
student_id -> course_id
```

只要未來出現兩列 `(S101, DB201)`與`(S101, FT210)`，left side相同、right side不同，
這一對tuples就是counterexample。因此第二個FD不是合法business constraint。

### 你來操作

判斷`course_title -> course_id`是否成立。請提出一條business rule支持它，或建立兩門
同名、不同ID的課程作為counterexample。只回答「sample data沒有重複」不算完成。

### 檢查方式

若制度沒有保證title unique，應拒絕此FD；不同course IDs可以共享通識課名。SQL的
`UNIQUE(course_title)`只有在制度真的要求unique時才合理。

## 4. Attribute closure and candidate keys

Attribute closure `alpha+`是在給定FDs下可由alpha決定的所有attributes。計算小型
closure時，先放入alpha，再反覆套用left side已全部在closure中的FD，直到不能增加
attribute。這裡只使用closure作key與lossless判斷，不要求推導完整`F+`。

### Worked example

令R為本章的八欄flattened relation，從`{student_id, course_id}`開始：

1. 初始：`{student_id, course_id}`。
2. `student_id -> student_name, dept_code`，加入`student_name, dept_code`。
3. `dept_code -> dept_name`，加入`dept_name`。
4. `course_id -> course_title, credits`，加入`course_title, credits`。
5. `(student_id, course_id) -> grade`，加入`grade`。

Closure包含R全部attributes，所以pair是superkey。移除`student_id`後無法決定student
與grade；移除`course_id`後無法決定course與grade，因此它是candidate key。

### 你來操作

對下列FDs計算`{employee_id, project_id}+`，再分別移除一個attribute測試minimality：

```text
employee_id -> employee_name
project_id -> project_name
(employee_id, project_id) -> hours
```

### 預期與回饋

Pair的closure應包含五個attributes；任何單一ID都缺少另一個entity fact及hours，
所以pair是candidate key。若只說「看起來unique」，尚未證明它能決定所有attributes。

## 5. Lossless decomposition

把R分成R1與R2後，我們希望對每個legal instance都能由projections的natural join精確
重建R。若join產生原本不存在的spurious tuples，decomposition是lossy。

只考慮FD constraints的binary decomposition時，若共同attributes
`R1 intersection R2`能決定R1或R2的全部attributes，分解是lossless：

```text
(R1 intersection R2) -> R1
or
(R1 intersection R2) -> R2
```

這不是說「有相同欄位就一定lossless」；共同欄位必須是其中一側的superkey。

### Worked example: lossless steps

第一次把flattened relation分成：

```text
Department(dept_code, dept_name)
Remaining(student_id, student_name, dept_code,
          course_id, course_title, credits, grade)
```

共同attribute是`dept_code`，且`dept_code -> dept_name`，所以它決定Department全部
attributes；此binary step是lossless。後續依`student_id`、`course_id`與pair分解，可得：

```text
Department(dept_code, dept_name)
Student(student_id, student_name, dept_code)
Course(course_id, course_title, credits)
Enrollment(student_id, course_id, grade)
```

每一步的共同attribute都是被移出relation的一側之key。Lab最後用兩個`EXCEPT`檢查
normalized join與原始rows雙向都沒有差異。

### Worked example: lossy join

原始employee rows為：

```text
(E1, Kim, Taipei, 60000)
(E2, Kim, Tainan, 62000)
```

錯誤分成`EmployeeIdentity(employee_id, name)`及
`EmployeeDetails(name, city, salary)`。共同attribute只有name，但name不是任何一側的
key。Natural join會把兩位Kim交叉配對，產生4列，其中2列是spurious tuples。

### 你來操作

執行lab的Part C與D，記錄lossless reconstruction的兩個difference counts，以及
Kim join的row count。圈出兩列spurious tuples並指出錯誤的employee-city pair。

### 預期與回饋

兩個difference counts都應為0；Kim join應有4列。只比較row count不永遠足以證明
relations相等，因此lossless case使用雙向`EXCEPT`。

## 6. Boyce-Codd normal form (BCNF)

Relation schema R在BCNF，表示對`F+`中每個`alpha -> beta`，至少有一項成立：

1. dependency是trivial；或
2. alpha是R的superkey。

實作判斷時先列出由business rules支持的FDs，再測試每個nontrivial determinant的
closure。看到一個left side不是superkey的FD，就已找到BCNF violation。

### Worked example

Flattened relation中的`dept_code -> dept_name`是nontrivial，但`dept_code+`只有department
facts，不能決定student、course及grade，因此relation不在BCNF。

分解後：

- Department的nontrivial FD是`dept_code -> dept_name`，left side是key。
- Student的nontrivial FD是`student_id -> student_name, dept_code`，left side是key。
- Course的nontrivial FD是`course_id -> course_title, credits`，left side是key。
- Enrollment的nontrivial FD是pair`-> grade`，left side是key。

在目前列出的FDs下，四個relations都符合BCNF。這個結論依賴business rules；若日後新增
例如`course_title -> credits`的制度規則，就必須重新檢查。

### 你來操作

檢查`EmployeeProject(employee_id, employee_name, project_id, project_name, hours)`的
每個nontrivial FD。指出第一個BCNF violation，再提出一組relations，使每個determinant
在自己的relation中成為key。

### 檢查方式

`employee_id -> employee_name`與`project_id -> project_name`都違反BCNF。合理分解為
Employee、Project及Assignment；只把name刪掉而不說明facts保存位置不是完整設計。

## 7. Third normal form (3NF)

3NF對每個`alpha -> beta`允許三種情況：dependency trivial、alpha是superkey，或
`beta - alpha`中的每個attribute都包含在某個candidate key中。出現在至少一個
candidate key的attribute稱為prime attribute。BCNF必定是3NF，反向不一定成立。

### Worked example: 3NF but not BCNF

假設：

```text
TeachingAssignment(student_id, course_id, instructor_id)
```

Business rules：每位student在每門course恰有一位instructor；每位instructor在這個
制度中只教一門course。因此：

```text
(student_id, course_id) -> instructor_id
instructor_id -> course_id
```

Candidate keys是`(student_id, course_id)`與`(student_id, instructor_id)`，所以三個
attributes都是prime。`instructor_id -> course_id`中，instructor ID不是superkey，
故違反BCNF；但right side的course ID是prime，故符合3NF第三項。這個判斷只在上述
「一位instructor只教一門course」rule成立時有效。

### 你來操作

若制度改為instructor可教多門course：

1. 哪個FD不再成立？
2. Candidate keys會如何改變？
3. 原本「3NF but not BCNF」的結論是否還能沿用？

### 預期與回饋

`instructor_id -> course_id`不再成立，只剩student-course pair作candidate key；在剩餘
FD下relation符合BCNF。Normal form是schema與constraints的性質，不能脫離rules沿用。

## 8. BCNF, losslessness, and dependency preservation

理想設計希望同時得到BCNF、lossless decomposition及dependency preservation。
Dependency preserving表示每個原FD能只檢查個別decomposed relations，不必join；但並非
所有schema都能同時滿足三者。3NF允許某些determinant不是superkey、right side為prime
的dependencies，以保留dependency preservation。

### Worked example

對TeachingAssignment依`instructor_id -> course_id`分成：

```text
InstructorCourse(instructor_id, course_id)
StudentInstructor(student_id, instructor_id)
```

共同attribute `instructor_id`是InstructorCourse的key，因此分解lossless且兩表BCNF。
但原FD `(student_id, course_id) -> instructor_id`的三個attributes沒有同時出現在任一表；
只靠個別table的key/unique constraints不能直接檢查它。這說明normalization不是看到
BCNF就停止思考constraints。

教科書在SQL難以有效表達arbitrary FDs的前提下仍偏好BCNF；實際設計則必須記錄未能由
database constraints直接enforce的rule及其檢查位置。

### 課堂比較

兩組分別主張保留3NF single relation或採用BCNF decomposition。每組必須用四個相同
依據回答：repetition、losslessness、能否由個別relations檢查FD，以及SQL實作成本。

### 個人學習證據

提交一頁內容，包含：

1. 原relation與business rules；
2. FDs與candidate key closure；
3. 至少一個anomaly；
4. decomposition與lossless理由；
5. 每個relation的BCNF/3NF判斷；
6. 根據回饋修正前後的一項差異。

同儕意見可協助比較，但個人證據必須保留自己的原始判斷及修正。

## 常見錯誤

1. 從少量sample rows猜FD，沒有business rule。
2. 把「目前沒有duplicates」誤寫成candidate key證明。
3. 只列normalized tables，沒有說明原FDs、anomalies及lossless理由。
4. 認為兩表有共同欄位就一定lossless。
5. 把3NF簡化成「沒有transitive dependency」，卻未找candidate keys與prime attributes。
6. 認為BCNF一定preserves every dependency。
7. 以join execution成功宣稱所有future legal instances都lossless；sample execution只能
   找反例或支援特定instance，形式判斷仍需FD criterion。

## 本章總結

Normalization把business rules轉成可檢查的FDs，再以closure、lossless criterion、
3NF與BCNF評估schema。好的答案必須同時處理資料語意與分解後的約束，不能只把一張
大表拆成多張小表。Ch14將轉向physical design：在logical schema合理後，再以queries、
data distribution與query plan決定index，而不是用index修補設計異常。

## 課後接續

- 用另一個真實表格重做「rules -> FDs -> anomalies -> decomposition -> lossless」流程。
- 補充閱讀attribute closure與dependency preservation；不要求完整Armstrong axioms、
  canonical cover或decomposition algorithm作為本課Exam 2操作題。
- 在正式assessment前，以教師公告的selected Ch7範圍為準。
