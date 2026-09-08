# 資料庫管理逐章教材設計 Prompt

請依照下列程序，為Elmasri及Navathe的《Fundamentals of Database Systems》第 7 版設計本學期的資料庫管理
教材。一次只處理一個章節，完成該章的來源查核、教材、範例、練習與驗證後，
再進入下一章。

2026-09-08來源與範圍更正：現用書為上述Elmasri/Navathe第7版，私人來源為
`private_references/book_Fundamental of Database Systems.pdf`。教師已要求修正課綱，
並指定三次考試各30%；Class Performance為10%。以下依新版課綱執行，不再沿用
Database System Concepts的章號、舊週次或考試範圍。

第一批發布例外：教師另核准先完成週四9/10的課綱及Ch1、Ch2、Ch5入門選講，
並在相應來源/程式/畫面查核後commit/push。此批只標示所教內容的查核範圍，
不得宣稱整章或全書完整查核。現行維護來源為ch01_database_introduction、
ch02_database_architecture、ch05_relational_model各自student_guide.md，
圖解為`maintenance/course_repository/opening_figures.py`；舊notebook在
`Intro DB/under_revision/`，不作正式指定。Ch5後續補入同一份notebook。

## 一、正式教學範圍

逐章的必教主題、小節、排除內容、週次及考試範圍，以
`Intro DB/syllabus.md`的Textbook Coverage、Weekly Schedule與Assessment為準，
並核對`maintenance/COURSE_PLAN.md`。不要把主體章節誤解為全章必教。

- Ch1-Ch2：導論選講；Ch3：ER；Ch5：relational model與constraints。
- Ch6：basic SQL；Ch7：選定的complex queries、views、簡單trigger與schema changes。
- Ch8：指定的relational algebra運算；不教relational calculus，division作延伸。
- Ch9：只教9.1 ER-to-relational mapping；先完成Ch3與Ch5所需概念。
  Weak entities、multivalued attributes及ternary relationship須先教再映射。
  Ch4與9.2 EER-to-relational mapping不列必教。
- Ch14：14.1-14.4在Week 11，以已給定candidate keys教至3NF；14.5 BCNF在Week 13。
- Ch15：15.1.1的attribute closure及15.2的binary lossless-decomposition選定內容，
  安排Week 13，不要求完整proof、minimal cover或schema-synthesis algorithms。
- Ch17：索引用途、B+ tree查找、composite index及read/update成本選講。
  先補Ch16的record、block及基本file organization；不整章教授Ch16。
  SQLite index commands與EXPLAIN QUERY PLAN另標為實作補充，不能宣稱為原書範例。
- Ch20：transaction boundaries、ACID、COMMIT/ROLLBACK與簡單並行錯誤選講。
- Ch18-Ch19及Ch21-Ch22不列必教；window functions、recursive CTEs、stored routines、
  higher normal forms及DBMS內部演算法不列本版必考範圍。

教材份量與順序須符合課綱：

- Week 1先課綱與導論，Week 2關聯模型及核心algebra，Weeks 3-5 SQL。
- Weeks 7-8 ER與mapping導入；Week 10完成9.1；Weeks 11及13分次教授正規化。
- Week 14索引，Week 15交易基礎，Week 16只整合複習。
- Week 9出國，不排新內容；Week 17放假；Weeks 6、12、18考試。
- Exam 2不考尚未教的closure、BCNF或formal lossless-decomposition test；
  這些內容列Exam 3。實際題目仍需獨立命題與驗證。
- 一章一份notebook，可跨次授課；先依新書逐節對照既有教材，不能只改舊notebook檔名。
- 保留大量原創圖解、小型input tables、簡單範例、預測、輸出判讀及練習。
- 不因完整來源查核而把課綱略過的小節加入正式教學或增加學生工作量。
- 學生教材使用English-only prose及標準術語，不寫分鐘配置或內部製作分類。
  教師端coverage、verification及治理紀錄可使用繁體中文。

## 二、開始工作前必讀

開始任何章節前，先完整閱讀：

1. `資料庫管理/AGENTS.md`。
2. `資料庫管理/PROJECT.md`。
3. `資料庫管理/Intro DB/syllabus.md`。
4. 與本章相關的最新版18週教學計畫；若它與課綱或`PROJECT.md`衝突，以教師
   最新決定、`PROJECT.md`及英文課綱為準，並記錄衝突。
5. 本章對應的教科書完整章節，不得只讀章節摘要或目錄。
6. 經確認屬於Elmasri/Navathe第7版的官方配套、程式、圖表、公式及範例；尚未
   找到時明列未取得，不得假設存在。`from_11001_DB/PowerPoint Presentations/`
   屬於Database System Concepts，僅是其他參考來源，不是現用書的官方投影片。
7. `maintenance/`、`from_11001_DB/`及其他現有SQL lab、database、schema、
   題目、圖檔與歷史教材。
8. 現有的生成來源、build script、rebuild script、notebook及相關紀錄；只有在
   實際存在時才使用，不得假設檔案已存在。

歷史考題、答案、教師手冊及受限制來源只能用於教師端查核，不得直接放入學生
教材。

## 三、每個教學內容都必須有講解與範例

2026-09-08教師要求：所有選定章節以大量原創圖解及簡單例子說明理論，
小型表格可作為資料input。沿用一章一份`Intro DB/chXX.ipynb`；不另做學生
投影片入口、不增加必教章節或必交作業。範例應就近放在對應概念旁，包含
具體輸入、可核對的預測、操作或推演、圖解、結果判讀，以及可選的條件變化。
圖中的SQL空值使用`NULL`；關係、流程及事件圖必須說明線條或箭頭的含義。
沒有SQL的概念可以用紙上推演，不得偽裝為實際DBMS執行結果。

目前維護方式：章節正文及完整lab在`maintenance/chapters/`；簡單範例及其來源
定位在`maintenance/course_repository/simple_examples.py`；圖形配置在
`teaching_figures.py`。修改這些維護來源，再建置並驗證notebook；不得只改生成檔。

在撰寫教材前，先依本章正式範圍建立逐項對照表。每一列是一個實際要教的概念、
方法、SQL語法、圖形關係、演算法概念或判讀能力，至少記錄：

- 教科書章節、小節、頁碼、投影片或官方程式位置。
- 學生應能完成的可觀察行為。
- 教材中的概念講解位置。
- 教材中的完整範例位置。
- 學生練習或操作位置。
- 結果判讀、回饋或修正方式。
- 對應的課堂表現或考試範圍。

任何正式教學內容都必須同時具備下列項目：

1. 使用學生能理解的文字完整講解，不只給定義或投影片式條列。
2. 至少一個從問題到結果都完整呈現的worked example。
3. 範例中的每一步、SQL子句、關係運算、設計決策或狀態變化都有解釋。
4. 至少一個讓學生自行套用的練習或操作。
5. 明確的預期結果、判讀依據、檢查方法或教師回饋重點。
6. 適用時加入常見錯誤、反例或錯誤解法比較。
7. 適用時說明成立條件、限制及不能推廣的情況。

只出現名詞、定義、公式、SQL語法、圖表或結論，而沒有對應講解與完整範例，
一律視為尚未完成。預測、比較、討論及修正活動不能取代教師
講解、worked example或學生實際練習。

不同主題的範例至少符合下列要求：

下列只適用於課綱實際指定的內容；不得藉此恢復排除的演算法或評量要求。

- Relational model及relational algebra：提供小型relation instance，逐步顯示
  輸入、運算及結果relation。
- SQL：提供可重現的schema、sample data、SQL、預期結果表及結果解釋。
- Joins、views及constraints：同時提供正確案例與至少一個容易出錯的案例。
- E-R model：提供business rules、ER diagram、cardinality判斷及relational
  schema mapping。
- Normalization：提供原始relation、functional dependencies、anomaly、分解過程、
  lossless判斷及正規化後schema。
- Indexing：提供query與資料情境、index選擇理由，以及建立index前後可觀察的
  query-plan差異；若DBMS或資料量不足以顯示差異，必須如實說明。
- Query processing及optimization：提供SQL、至少兩個可能或實際plan，以及可由
  plan支持的比較，不得只用執行時間宣稱某方法必然較快。
- Transactions：提供transaction boundaries、ACID、COMMIT/ROLLBACK與簡單交錯
  更新範例；本版不要求formal serializability或recoverability分類。
- Concurrency control：提供交錯schedule、lock request、等待關係及deadlock或
  正常完成的判讀。
- Recovery：提供failure scenario、log records及復原步驟，說明哪些操作需要
  undo、redo或rollback；只使用本章實際教授的機制。

## 四、設計前的來源查核

撰寫教材前，必須完整閱讀本章正式範圍及理解必要的相鄰段落，逐段及逐句查核：

- 定義與技術名詞。
- 主要主張。
- 公式、符號及relational-algebra notation。
- 圖、表、schema diagram、E-R diagram及圖說。
- SQL、transaction schedule、log與其他程式或表示法。
- 程式輸出、query result及query plan。
- 範例、假設、限制、注意事項。
- 本章內部及與前後章的關係。

查核時必須區分：

1. 教科書明確陳述的內容。
2. 教科書範例或實驗呈現的結果。
3. 作者提出的限制、條件或例外。
4. 可以從公式、SQL、schema、schedule或log直接推出的結果。
5. 為本課學生所做的教學改寫。
6. 尚未由來源或執行結果支持的推論。

對核心主張保留章、節、頁碼、圖表、公式、投影片或官方程式位置。不得捏造
引用、頁碼、SQL輸出、query plan、執行時間或教科書未提出的結論。

## 五、資料庫範例與程式查核

逐行檢查本章使用的SQL、setup script、transaction及其他程式，確認：

- SQL與正文解釋一致。
- 使用的DBMS、版本、dialect及extension已記錄。
- schema、keys、constraints及sample data明確且可重建。
- 每個query result可由目前資料重現。
- `NULL`、duplicate rows、empty result及constraint violation等情況已正確處理。
- transaction boundary、commit及rollback沒有混淆。
- query plan及performance解讀沒有超出證據。
- 沒有把SQLite、PostgreSQL、MySQL或其他DBMS的特定行為錯寫成通用SQL規則。
- 教科書程式與本地改寫之間的差異有明確理由。
- 所有學生需要的資料來源、路徑及執行順序都已說明。

可合理執行的內容必須在乾淨環境中依序執行。若某段因DBMS、版本、權限、時間、
資料量、網路或其他限制無法執行，必須標示為未執行並說明原因，不得從其他結果
推定它已通過。

## 六、本章教材設計

完成來源查核及逐項對照表後，才開始設計教材。本章教材應讓學生即使沒有教師
投影片，也能閱讀、重現範例並完成主要練習。內容量必須配合第一節所列的週次
與授課摘要；課堂未完成部分可由學生課後接續閱讀，但不得把超出正式範圍的內容
變成未明示的必做作業。

每章原則上包含：

1. 一份完整的學生主教材。
2. 一份適合本章的可執行SQL lab、notebook或可重現操作文件。
3. 必要的schema、sample data、diagram、query、transaction schedule或log資料。
4. 必要的環境設定、DBMS差異、資料來源、故障排除及延伸內容。
5. 與學生教材分開保存的教師驗證紀錄及答案。

學生主教材至少包含：

- 本章核心問題。
- 與前章的關係。
- 先備知識。
- 可觀察及可檢查的學習目標。
- 完整概念說明。
- 每個正式教學內容對應的worked example。
- 適用的公式、符號、schema、diagram、schedule、log及query-plan解釋。
- 可執行的SQL或操作步驟與預期結果。
- 執行或揭示答案前的結果預測。
- 執行結果的判讀。
- 方法、設計或SQL解法比較。
- 常見錯誤、反例及失敗情境。
- 分段理解問題。
- 課堂討論問題及學生回答時應使用的判斷依據。
- 個人應保存的學習證據。
- 課後接續內容。
- 本章總結及與下一章的連結。

教材應以自己的文字及自行建立的教學例子重新說明，不得大量複製教科書正文、
投影片、圖表、解答或其他受著作權保護的內容。必要引用應保持簡短並標示來源。

## 七、教學、範例、練習與評量對齊

完成初稿後，重新檢查逐項對照表：

- 每個學習目標至少對應一段實際教學。
- 每段實際教學至少對應一個完整範例。
- 每個完整範例後至少有一個學生可完成的練習或判讀活動。
- 每個練習都有預期結果、判斷標準或教師回饋重點。
- 每個列入考試的能力都已在考前教過、示範過並讓學生練習過。
- 每個列入Class Performance的產出都有明確要求及可保存的個人證據。
- Peer ranking可支援討論，但rank本身不直接決定成績。
- 未列入正式範圍的內容不得出現在必考或必做要求中。

若任一正式教學內容在「講解、範例、練習、回饋」中有空缺，必須先補齊，不能
進入下一章。

## 八、完成初稿後的逐句檢查

逐句檢查所有學生可見內容，包括正文、標題、表格、圖說、公式說明、題目、提示、
SQL註解及執行輸出。每一句至少檢查：

1. 是否正確。
2. 是否受到來源或執行證據支持。
3. 是否使用教科書及資料庫領域的標準術語。
4. 主詞、動詞及技術關係是否精確。
5. 是否把單一範例、單一DBMS或單一資料集結果過度推廣。
6. 是否遺漏成立條件、限制或例外。
7. 是否與SQL、schema、diagram、schedule、log、query plan及其他段落一致。
8. 是否符合二年級資訊管理學生的先備能力。
9. 是否能由自行閱讀的學生理解及重現。
10. 是否與本章學習目標、範例、練習及評量相符。
11. 是否不必要地重複或增加學習負擔。

## 九、程式與成品驗證

完成逐句檢查後：

- 從乾淨、已記錄版本的環境重建sample database。
- 依順序執行所有學生需要執行的SQL、script、notebook或操作。
- 核對query results、constraint behavior、transaction results、query plans及正文。
- 測試主要錯誤、邊界、`NULL`、duplicates、empty results及資料問題。
- 檢查所有內部連結、圖片、資料及script路徑。
- 檢查Markdown、notebook與SQL lab的閱讀及執行順序。
- 確認學生教材沒有答案、教師批改內容、歷史考題答案或未發布考題。
- 確認生成來源與生成後成品一致，不得只修改生成檔。
- 若教材包含diagram或其他版面成品，實際render並檢查文字、箭頭、cardinality、
  table及公式是否清楚且沒有重疊。

## 十、修正與完成條件

發現問題後，修正維護來源，重新生成受影響教材，再重新執行受影響的檢查。
不得只修改生成後的notebook、Markdown或講義而留下build script或來源不一致。

重複「檢查、修正、重新生成、重新驗證」，直到下列條件全部成立：

- 所有正式教學內容均出現在逐項對照表。
- 每個正式教學內容都有講解、完整範例、學生練習及回饋方式。
- 核心技術主張均已查核來源。
- 所有可合理執行的SQL及程式均已通過。
- 未執行內容已清楚標示並說明原因。
- 正文、公式、SQL、schema、diagram、schedule、log、query plan及輸出沒有已知矛盾。
- 學習目標、教材、範例、活動、Class Performance及考試範圍互相對應。
- 學生能在沒有投影片講解的情況下閱讀、重現範例並完成練習。
- 課堂討論建立在所有學生都能完成的共同內容上。
- 沒有已知的答案洩漏、版權、個資或發布問題。
- `AGENTS.md`及`PROJECT.md`要求的適用檢查均已完成。
- 沒有尚未處理的阻擋性錯誤。

「完成」只表示上述檢查在目前版本沒有發現阻擋性問題，不代表教材永遠不需
修改，也不要求為了篇幅而無限制增加內容。

## 十一、逐章交付與自動繼續

完成一章後，先建立該章的交付紀錄，不要把尚未完成的下一章內容混入本章。
每章紀錄至少包含：

1. 本章建立或修改的檔案。
2. 本章實際教授及略過的小節。
3. 主要教學設計及每個教學內容的範例配置。
4. 查核過的教科書、投影片、程式與既有教材範圍。
5. 實際執行的SQL或程式及結果。
6. 未執行或無法驗證的項目。
7. 發現並修正的主要問題。
8. 仍存在的限制。
9. 本章是否符合進入下一章的條件。

完成紀錄後，若沒有阻擋性問題，立即自行開始下一章，不等待額外指示。若存在
阻擋性問題，應先嘗試利用現有來源、環境及可重現測試解決；只有確實無法繼續時
才停止並具體說明所需資訊或決定。

依序完成Ch2、Ch3、Ch4、Ch5、Ch6、Ch7、Ch14、Ch15、Ch16、Ch17、Ch18、
Ch19後，提供全課整合報告，確認章節銜接、術語、sample database、SQL dialect、
Class Performance與三次考試範圍一致。
