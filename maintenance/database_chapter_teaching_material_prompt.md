# 資料庫管理逐章教材設計 Prompt

請依照下列程序，為Elmasri及Navathe的《Fundamentals of Database Systems》第 7 版設計本學期的資料庫管理
教材。一次只處理一個章節，完成該章的來源查核、教材、範例、練習與驗證後，
再進入下一章。

2026-09-08來源與範圍更正：現用書為上述Elmasri/Navathe第7版，私人來源為
`private_references/book_Fundamental of Database Systems.pdf`。教師已要求修正課綱，
並指定三次考試各30%；Class Performance為10%。以下依新版課綱執行，不再沿用
Database System Concepts的章號、舊週次或考試範圍。

2026-09-10最新指示：今天只教Ch1/Ch2，後續按Ch3-Ch9、Ch14-Ch19順序。
教師授權重排課綱與同步文件後commit/push。先前Ch5/Ch8在前兩週的安排已撤換，
既有教材保留至Week 4/8使用；Ch20不另排教學。不得把歷史紀錄當作現行範圍。

## 一、正式教學範圍

以`Intro DB/syllabus.md`及`maintenance/COURSE_PLAN.md`的Detailed Coverage為準。
範圍是Ch1/Ch2導論、Ch3-Ch9、Ch14-Ch19；列出章節不代表所有小節或習題均必教。

- Ch3 ER必教；3.1-3.7核心加3.9簡單三元例子。
- Ch4 EER必教4.1-4.7，包含全部核心種類、限制、design choices、definitions、
  UML及abstraction/knowledge representation/ontology入門；不新增ontology專案。
- Ch5教5.1-5.3；Ch6教6.1-6.4；Ch7選7.1-7.4含一個簡單trigger。
- Ch8選8.1-8.3 algebra及8.5組合；division、calculus不列必教。
- Ch9教9.1-9.2；七個ER步驟、8A-8D成立條件、shared subclasses與categories，
  比較相同/不同來源key；區分圖上限制與SQLite實際強制限制。
- Ch14選14.1-14.5，含1NF至3NF及BCNF簡單比較，使用給定candidate keys。
- Ch15選15.1-15.3：短attribute closure、lossless/dependency preservation，
  用給定minimal cover/key追蹤Algorithm 15.4。minimal cover要定義，
  但不要求推導；不加入general chase、證明、完整BCNF演算法或4NF/5NF。
- Ch16選16.1-16.8：records、blocks、buffering、blocking factor、
  heap/sorted files、static hashing及collision；不只列為索引背景。
- Ch17選17.1-17.4與17.7：ordered/dense/sparse indexes、B+ tree、composite keys，
  讀寫代價與physical design；不教完整split/merge實作。
- Ch18選18.1、18.3-18.4、18.7：SQL到algebra、selection方法、
  nested-loop/indexed nested-loop、sort/hash join概念、materialization/pipelining。
- Ch19選19.1-19.3：query trees、合法pushdown、兩種plan、catalog、
  equality selectivity與估計限制；不做完整成本推導或optimizer實作。
- Ch20-Ch22不排正式章節；Ch5的簡短rollback例子不代表另教整章交易。

週次與評量：
- Week 1 Ch1/Ch2；Week 2 Ch3；Week 3 Ch4的4.1-4.4；
  Week 4 Ch4的4.5-4.7與Ch5；Week 5 Ch6。
- Weeks 7/8 Ch7/Ch8；Week 10 Ch9；Week 11 Ch14/Ch15；
  Weeks 13/14/15 Ch16、Ch17、Ch18/Ch19。
- Weeks 6/12/16三次考試各30%，範圍依序Ch1-6、Ch7-9與Ch14-15、
  Ch16-19加累積已教SQL/design；Class Performance 10%。
- 11/1-8出國，Week 9只複習Ch1-8；Week 17放假；Week 18補考。
  Weeks 16-18不排新內容，補考不加第四次配分。
- 五次小組比較Weeks 2、4、10、13、14；AI活動仍4、10、14，
  題材依現行plan，不能在SQL教授前要求學生獨立寫SQL。
- Weeks 11/15份量緊，使用共同小例子及給定資料；不足時回報，不擅自增加
  考試週進度、作業或考未教內容。
- 一章一份notebook；大量原創圖、input tables、簡例、預測、實際輸出、
  判讀及練習。英文學生教材不寫分鐘配置或內部製作分類。
- 本次改課綱/銜接，不等於全章或全書逐句查核完成；查核範圍須獨立記錄。

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
- E-R model：Ch3提供business rules、ER diagram及cardinality判斷；relational
  schema mapping保留至Ch9，不在Ch3提前要求SQL或轉表。
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

依現行課綱順序完成Ch1-Ch2導論、Ch3-Ch9、Ch14-Ch19的指定範圍。
只處理本次教師授權的批次；一章一份notebook，Ch9不拆分。
完成全課後提供整合報告，確認章節銜接、術語、sample database、SQL dialect、
Class Performance與三次考試範圍一致。不得沿用舊書章號或擅自排入Ch20。
