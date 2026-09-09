# 資料庫管理 - Project Context

本檔只記錄資料庫管理課程的事實、固定決策、權威文件、核准用語、限制與
未解問題。通用工作規則見 `AGENTS.md`；`CLAUDE.md` 是其位元一致鏡像。

- 最後更新日期：2026-09-09
- 2026-09-09最新考試決策：教師要求第16週（2026-12-24）期末考，第18週
  （2027-01-07）補考，並授權修改相關檔案後commit/push。此決定取代下方
  第16週整合複習、第18週正式期末考的較早紀錄。第17週12/31仍放假；
  Exam 1/2日期與30/30/30/10配分不變。核心章節保留，Weeks 13-15以原有
  範例穿插複習；Week 15限定一個轉帳例子及一張並行更新圖，並整合複習，
  不新增作業或進階交易演算法。Weeks 16-18不加新必教內容。
  補考不另增第四次配分；補考資格、範圍、計分安排待教師宣布，不自行制定。
  本次也包含上一則尚未提交的教科書區塊及11/1-8出國日期修正。
- 2026-09-09課綱修正：教師更新出國期間為2026-11-01至2026-11-08，取代較早
  11/1-7的期間。仍僅影響Week 9的11/5，保留非同步複習、不排實體課或新進度；
  11/12恢復實體授課。課綱前段新增獨立Textbook區塊，明列書名、作者、第7版
  與Pearson出版社；現用書、必教章節、考試日期及30/30/30/10配分不變。
  同步更新COURSE_PLAN；本次未另行授權commit或push。
- 2026-09-08第一批授課發布：教師同意優先完成週四9/10使用版本，包含驗證後
  commit/push。現行入口為課綱、`Intro DB/ch01.ipynb`、`ch02.ipynb`、`ch05.ipynb`；
  三份分別是正確課本Ch1、Ch2導論選講及Ch5第一堂入門，不是全章已完成。
  Ch1/2停在Chapter Summary，Ch5停在First-Meeting Summary and Practice；
  教師可提早停止接續授課。SQL/Python為提供的觀察工具，不是第一堂撰寫要求。
  舊12份notebook保留於`Intro DB/under_revision/`供檢閱，清楚標示未指定，
  舊週次/考試/章號不再作正式入口。新版維持一章一份，不另做week1 notebook。
  新增16張原創圖解；來源、範圍、驗證與發布狀態見
  `maintenance/course_repository/first_meeting_release.md`。
  因授課期限，第一批優先於後續ER範例修正；NULL主鍵缺陷仍列後續阻擋項，
  受影響舊ER教材不得因此次發布被宣稱已修復或可指定。完整教科書全章查核
  仍未完成；以下較早未授權push或尚無導論教材的狀態由本段取代。
- 2026-09-08教材對照進度：依教師「開始下一步」完成新版必教主題與現有維護
  來源的對照，見`maintenance/course_repository/textbook_material_correspondence.md`。
  本次僅建立對照與缺口紀錄，沒有改寫或重新命名notebook，也未變更課綱政策。
  需要補齊導論架構、1NF/2NF至3NF的逐步教學、1:1及三元關係mapping、
  索引所需儲存先備。另在全新記憶體SQLite重現舊ER mapped_schema.sql接受
  NULL文字主鍵的問題；已記錄但未在對照階段修改。因有實際正確性問題，
  下一步優先修正該SQL、增加缺少識別值的測試並重建受影響成品，再依對照補課。
  正確教科書完整章節來源查核仍為0章；本次沒有stage、commit或push。
- 2026-09-08最新核准：教師要求依本次討論修正課綱，並指定三次考試各30%。
  現用書為Elmasri/Navathe第7版；主體為Ch3、Ch5-Ch9、Ch14的課綱指定內容，
  Ch1-Ch2作導論，Ch15、Ch17、Ch20選講，Ch16僅補索引需要的先備概念。
  Ch9只教9.1，以Ch3及Ch5為先備；不教Ch4與9.2，不另開Ch18-Ch19、Ch21-Ch22。
  配分為Exam 1/2/3各30%，Class Performance 10%，取代較早25/25/30/20的紀錄。
  Week 7-8教ER，Week 10完成mapping；Week 11教至3NF，Week 13才教closure、
  BCNF及binary lossless decomposition；後三者列Exam 3，不列Exam 2。
  Week 14教索引，Week 15教交易基礎，Week 16只做整合複習。考試日期、出國週、
  假日、五次比較活動及AI使用政策保持不變。最新完整範圍以
  `Intro DB/syllabus.md`與`maintenance/COURSE_PLAN.md`為準。
  這是課綱修正，不是全章教材完成：現有notebooks及生成設定仍保留舊書章號，
  不能按檔名指定新書閱讀或考試，也未因本次課綱更新而自動完成來源查核。
  本次未授權commit/push。以下較早決策如有衝突，以本段及現行課綱為準。
- 2026-09-08教師明確更正現用書：Ramez Elmasri、Shamkant B. Navathe，
  *Fundamentals of Database Systems*, 7th Edition，指定檔案
  `book_Fundamental of Database Systems.pdf`。此決定取代下方所有把
  *Database System Concepts* 列為現行主教材的歷史紀錄；不是本次另行換書。
  現有課綱、notebook檔名與章節標籤沿用錯誤來源，尚未對齊正確課本；不得把
  舊Ch2/Ch3查核算成本書的來源查核，也不得只換書名便沿用全部章節編號。
  日期、三次考試配分與既有教材暫予保留；章節對照及教學範圍須重新確認。
- 2026-09-08來源查核更正：教師要求重新逐章完整查核並建立可追溯紀錄。
  既有建置、執行與局部原文查核不等於整本書逐句查核完成；下方歷史完成紀錄
  不能替代本次逐節對照。最新進度見
  `maintenance/course_repository/full_source_audit.md`。本次未授權commit或push。
- 2026-09-08授課設計決策：依教師要求補齊全部12個選定章節，以大量原創圖解、
  小型輸入表及簡單例子講解；仍維持`Intro DB/`一章一份notebook及英文學生教材。
  新增51個小例子（32個可執行SQL、19個概念推演），圖共96張；Ch2既有19張保留，
  其餘每章5至10張。範例包含預測、圖解、結果判讀、可選變化及檢查依據。
  維護來源新增`maintenance/course_repository/simple_examples.py`，由既有建置器
  就近插入各章，不增加學生資料夾、套件需求或必交作業。選講與延伸邊界、週次、
  日期、出國週、三次考試及配分不變。教師於本次完成後明確授權commit/push至
  既有`origin/main`；維護來源、12章notebook與重建SQLite套件同批提交，
  同步結果以Git history及遠端為準，不包含私人來源或忽略檔案。
  完整紀錄見`maintenance/course_repository/all_chapters_teaching_review.md`；
  程式與圖形驗證不等同於教師已親自審閱或已證明學生負荷適當。
- 2026-09-07最新發布決策：教師明確要求將既有`KennethWYLee/Database`設為public，
  已透過GitHub API確認PUBLIC。此指示取代下方較早的private、另建public repository
  與尚未授權公開紀錄；既有maintenance、歷史與分支也會公開，不改寫或刪除歷史。
  課綱新增每週Textbook Chapters欄，依現行計畫標註Ch2-Ch7及Ch14-Ch19與選講範圍，
  日期、教學內容與配分不變。此更新將同步至既有main供線上閱讀。
  公開前檢查16個可達commit的檔名及常見憑證格式，未發現教科書、考題檔或憑證
  命中；Actions runs、Releases及Issues均為0。這些檢查不是所有敏感資訊的形式證明。
  本機private_references、舊私人教材及未追蹤檔案仍不納入Git；未授權未來加入考題、
  答案、學生資料或其他受限制內容。課程維護報告不等於未發布評量答案。
- 2026-09-07最新授課決策：第一次先講課綱，再概談Ch2；notebook的Week 1/Week 2
  是閱讀分段，不要求第一堂讀到End of Week 1。沿用一章一份教材，依當堂進度接續。
  正式給學生時教師可能先提供Ch2；目前保留全部12章供教師檢查，不提前下架、
  改公開權限或另建發布分支。本次內容修改不包含新的commit/push授權。
- 同次Ch2修正已完成：文字主鍵明列NOT NULL、composition projection補DISTINCT、
  跨學期複合主鍵例子及逐概念SQL示範。建置器直接嵌入既有SQL來源，不複製維護
  SQL或另加一份章末lab。完整驗證紀錄見Ch2的coverage_and_verification.md；
  不把可執行示範的Python或transaction-control語法新增為Ch2必考內容。
- 目前目錄決策：本機與GitHub統一使用`main`及相同追蹤路徑；`Intro DB/`放
  唯一維護課綱`syllabus.md`與12份生成的章節notebook。`maintenance/`集中章節
  維護來源、課程計畫、生成器、驗證與歷史紀錄。根目錄保留README、PROJECT、
  AGENTS、CLAUDE四份Markdown，不再以不同分支提供不同的現行教材目錄。
- 教師已另行授權本次整理commit/push至main；維護來源、Intro DB成品與本紀錄
  同批提交，同步結果以Git history及遠端為準。舊`course-materials`與
  `student-preview`分支保留作歷史，不再作日常教材入口，也不自動刪除。
- 課程狀態：115-1課綱、18週課程計畫、章節範圍、三次考試與SQLite環境已對齊；
  教師審閱前客觀檢查完成，2026-08-27的範圍與語言決策已套用至英文學生教材；
  2026-08-28依教師最新決定改為不區分教師與學生導覽，每個選定章節只有一份
  自包含`chXX.ipynb`，並已完成12份notebook的本機建置與逐cell執行驗證；Ch2
  加入原創Python-generated schema/algebra figures，SQL chapters加入database build
  與schema inspection guidance
- 2026-09-05依教師核准重整Ch2的Week 1：同一份notebook內新增七段就地執行範例、
  tuple/attribute/value圖、具體練習與End of Week 1停止點；完整keys分類與四表操作
  自Week 2開始。編寫完成時尚未commit/push；後續同步紀錄見Repository與發布狀態。
- 同日取得教科書後，依教師核准修正三處Week 1內容：查詢去重不改動原表、
  course練習改用description，以及補上atomic values的前後電話表格與查找步驟。
  學生程式仍為七段，未增加SQL語法要求、章節、週次或配分。
- 同日依教師「先把Week 1完成」的最新指示，完成現有範圍的講解、具體範例、
  練習及客觀檢查，不再把教師逐份審閱列為Week 1編寫完成的前置條件。
  版本`2026.09.05-week1-complete`已完成來源查核、執行與本機畫面驗證；
  不宣稱教師已親自審閱或學生已實際使用；後續已授權GitHub同步。
- Repository：本資料夾是獨立 Git repository；`main`追蹤GitHub的`origin/main`，
  最新commit以Git history為準
- 文件可見性：混合；歷屆考題、答案、評分資料及教師手冊不得直接發布

## 課程定位與對象

- 課程名稱：資料庫管理（Database Management）
- 任課教師官方英文姓名：WenYi Lee。
- 對象：四技資訊管理系二年級必修課程學生。
- 學分與時數：3 學分，每週 3 小時。
- 上課時間：星期四第 5-7 節，13:30-16:15。
- 課程主體：relational model、relational algebra、SQL、ER model、
  ER-to-relational mapping、functional dependencies、normalization，以及選定的
  indexing、query-plan interpretation及transaction basics；不要求DBMS內部
  query optimization、concurrency-control或recovery演算法。
- 課程可在教師允許時訓練學生檢查 AI 產生的 SQL、ER diagram、schema、
  query plan與transaction判斷；這是教師加入的應用，不宣稱為教科書原有章節。

## 用語與學生可見內容

- 所有正式學生教材使用English-only prose；technical terms使用教科書與資料庫領域
  的標準英文用語。教師端治理、查核與備課文件可使用繁體中文。
- 學生可見文件直接描述概念講解、完整範例、個人練習、小組比較、教師回饋
  與個人修正，不使用學生無法從課程內容理解的教學設計分類名稱。
- 課程計畫與逐章教材不寫分鐘配置；需要控制份量時，以授課摘要、課堂核心
  內容及課後延伸內容區分。
- 不把課堂流程、評量方式或 AI 使用方式另取未經教師核准的名稱。
- Week 1只介紹識別欄位的用途，以同名學生說明；superkey、candidate/primary/
  composite/foreign key的正式分類留在Week 2。課綱、課程計畫與首頁對齊此決定。
- Week 1使用獨立的synthetic student table，Python/SQL為已提供的觀察工具，
  不要求掌握語法。七段示範依概念、可檢查預測、程式與實際輸出、具體判讀排列；
  練習直接寫在同一notebook，只在教師指定時繳交，未新增配分或作業平台。
- 2026-09-07修正Week 1練習要求：可提供預測的修正，或解釋預測為何正確，
  不要求預測正確的學生另找一個錯誤。課綱入口改稱syllabus，不建立week1.ipynb；
  這是檔案與導覽調整，不改動既有Week 1授課範圍、日期、章節或評量。

## 現用教科書與查核狀態

- 現行主要教科書：Ramez Elmasri、Shamkant B. Navathe，
  *Fundamentals of Database Systems*, 7th Edition，Pearson；依教師本次明確確認。
- 正確私人複本：`private_references/book_Fundamental of Database Systems.pdf`。
  來源為教師原始書庫中的同名檔案；原檔保留。PDF共1273頁，封面、書名頁與
  版權頁已查驗；這份PDF列出的ISBN為978-0-13-397077-7，不能把舊課綱另一
  裝訂/地區版本的ISBN直接當作此PDF的ISBN。原檔與複本SHA-256相同：
  `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`。
- 本書尚未完成任何一章的完整來源查核。已確認檔案身分不等於已閱讀全書。
  `from_11001_DB/PowerPoint Presentations/`為另一本文獻的投影片，不能再稱為
  本書對應的官方教材。[Pearson教師頁面](https://www.pearson.com/en-us/subject-catalog/p/Elmasri-Fundamentals-of-Database-Systems-7th-Edition/P200000003546?view=educator)
  已確認列有PowerPoint配套，但實際投影片檔案尚未取得或查核。

### 先前使用錯誤主教材的紀錄

以下保留 *Database System Concepts*, 7th Edition 的閱讀及執行紀錄，僅供
追溯；不代表本課現用書、章節對照或學生可用狀態。一般SQL執行結果不因用書
更正就自動失效，但教材與本書的來源一致性必須重新查核。

- 2026-08-27當時確認的本機私人PDF標題、作者與版本為上述另一本文獻；該
  PDF只作教師端來源查核，不納入Git或學生套件。
- 2026-09-05依教師提供的目錄找到並複製教科書至
  `private_references/Database System Concepts 7th.pdf`；原檔為
  `C:/Users/User/Documents/GoogleDrive/無筆記論文&書pdf/book_Database System Concepts 7th.pdf`，
  保留不動。封面、版權頁與metadata確認為上述第7版，PDF共1519頁、11,403,145 bytes；
  複製前後SHA-256一致：`6759169c44277578465d0aeebd50be0e70e832076a7e7a7a45b4e98ce4151d8c`。
  `private_references/`已受現行`.gitignore`排除。複製步驟只確認書籍身分與複本一致性。
- 同日後續已完整閱讀Ch2文字、練習與附註（印刷pp.37-64、PDF pp.62-89），
  視覺檢查pp.40、42的相關圖表，並讀取Ch1 pp.1、5-8、11-14與Ch3 pp.72-73，
  重新核對新版Week 1。
  正式原文範圍、三處修正與驗證見Ch2 coverage record；不宣稱同時重審其餘章節。
- 過去紀錄曾聲稱完整查核Ch2-Ch7、Ch14-Ch19，但不足以支持目前版本已完成
  全部逐句來源查核；本次依逐章紀錄重新確認，不延用這項整體完成宣稱。
  Ch8-Ch9僅曾核對另一本文獻的章節綱要並決定不列入當時的必修進度。
  舊稿曾排除 *Fundamentals of Database Systems, 7/e* 作為現用書；這項排除
  已由教師本次明確確認撤銷，不得再沿用。

以下表格是既有教材在 *Database System Concepts* 中的編號與範圍，尚未對應
至現用 *Fundamentals of Database Systems*；不得據此直接指定新書閱讀或考試章節。

| 章節 | 教科書章名 | 本課處理方式 |
|---:|---|---|
| 2 | Intro to Relational Model | 正式授課：relations、schemas、keys、schema diagrams，以及selection、projection、Cartesian product、join與set operations；assignment、rename及複雜equivalence推導作課後延伸 |
| 3 | Introduction to SQL | 正式授課：DDL basics、basic queries、aliases、expressions、duplicates/`DISTINCT`、string patterns、ordering、set operations、NULL、aggregation、`GROUP BY`/`HAVING`、`IN`/`EXISTS`、一個correlated query與一個CTE、basic database modification；subquery in `FROM`、scalar與複雜correlated subqueries、`SOME`/`ALL`、`UNIQUE`、`LATERAL`、formal multiset algebra及advanced modification作課後延伸 |
| 4 | Intermediate SQL | 正式授課：explicit inner join、left outer join、`ON`/`USING`、outer join中`ON`與`WHERE`的差異、view定義與查詢、basic transactions，以及`NOT NULL`/`UNIQUE`/`CHECK`/foreign-key constraints；right/full outer join、view更新細部規則、materialized views、deferred constraints、assertions與authorization作課後延伸 |
| 5 | Advanced SQL | 選講：ranking/window functions、recursive CTE的base/recursive term與termination，以及一個row-level audit trigger與`OLD`/`NEW`；stored function/procedure只教用途與基本interface，pivot以conditional aggregation短示範；完整procedural SQL、專屬pivot、rollup/cube、JDBC、Python database API、ODBC與embedded SQL不列入主要教學 |
| 6 | Database Design Using the E-R Model | 正式授課：design process、entities、attributes、relationships、complex attributes、cardinalities、keys、redundant attributes、ER-to-relational mapping、design issues；extended E-R與alternative notations作補充 |
| 7 | Normalization | 選講：good relational design、update/insertion/deletion anomalies、functional dependencies與counterexamples、足以判斷key的attribute closure、binary lossless decomposition與spurious tuples，以及3NF/BCNF的基本判斷；dependency preservation只說明取捨，不完整教授functional-dependency theory與分解演算法 |
| 8 | Complex Data Types | 不列入必修進度；可作補充閱讀 |
| 9 | Application Development | 不列入必修進度；可作補充閱讀 |
| 14 | Indexing | 選講：index使用時機、B+ tree equality/range lookup概念、composite index欄位順序、covering index、`CREATE INDEX`/`DROP INDEX`及`EXPLAIN QUERY PLAN`證據；dense/sparse、clustering/secondary與split作概念延伸，不教完整insertion/deletion及cost derivation |
| 15 | Query Processing | 選講：logical/physical plan、file/index scans、join order、nested與indexed nested-loop概念及query-plan證據；parsing/translation只作銜接，materialization/pipelining、merge/hash細節、完整演算法與成本推導作課後延伸 |
| 16 | Query Optimization | 選講：result equivalence作為performance comparison前提、catalog row/distinct statistics、basic equality selectivity、`ANALYZE`及實務判讀`EXPLAIN QUERY PLAN`；selection/projection pushdown、join reorder、outer-join反例、skew細節、cost formula、dynamic programming與optimizer algorithms作課後延伸 |
| 17 | Transactions | 選講：SQL transaction boundaries、transaction concept與states、ACID、concurrent schedules、operation conflicts、small precedence graphs、conflict serializability、basic recoverability及isolation phenomena；不教完整serializability-testing algorithm與各類實作protocol |
| 18 | Concurrency Control | 選講：S/X locks與compatibility、grant/wait、wait-for graph、deadlock detection及victim/retry注意事項；basic/strict/rigorous 2PL、timestamp protocol、MVCC、snapshot isolation與write skew作課後延伸 |
| 19 | Recovery System | 選講：transaction/system/storage failure的基本區分、log old/new values、WAL ordering、committed/incomplete判斷及單一簡化redo/undo案例；checkpoint、backup加post-backup log、ARIES、fuzzy checkpoint、force/steal、remote failover及production administration作課後延伸 |

- ch14-ch19以就業實用性為取捨依據列入正式進度與Exam 3，但只教授上述選定
  內容，不要求完整涵蓋各章理論與演算法。

## 115-1 固定日期與進度範圍

- 115-1 自 2026-09-07 開始上課；本課 Week 1 為 2026-09-10。
- 教師於 2026-11-01 至 2026-11-08 出國參加 INFORMS；Week 9 的
  2026-11-05 不排實體課、考試或新進度，只複習已教的Ch1-Ch2、Ch5-Ch8選定內容。
- Week 17 的 2026-12-31 為校慶補假，不排課。
- Week 6 的 2026-10-15 辦理Exam 1；Week 12的2026-11-26辦理Exam 2。
- Weeks 13-15的既有範例併入複習；Week 16的2026-12-24辦理Exam 3與課程期末考。
- Week 18的2027-01-07在校定期末考週，保留補考，不另排正式期末考或新進度。

## 評量與章節對應

| 評量 | 週次與日期 | 比例 | 範圍 |
|---|---|---:|---|
| Written Exam 1 | Week 6, 2026-10-15 | 30% | Ch1-Ch2、Ch5-Ch8的已教選定內容：導論、關聯模型、核心algebra及SQL |
| Written Exam 2 | Week 12, 2026-11-26 | 30% | Ch3、9.1、14.1-14.4選定內容；不含Ch4、9.2、BCNF、closure及formal lossless-decomposition test |
| Written Exam 3 / Final Examination | Week 16, 2026-12-24 | 30% | 14.5、Ch15、Ch17、Ch20選定內容；Ch16僅作索引背景，並累積應用已教SQL與database design |
| Class Performance（課堂表現） | 全學期 | 10% | 指定SQL labs、database design exercises、ER diagrams、schemas、normalization、index與query-plan activities、個人回答與修正；peer rank不直接計分 |

- 三次考試都用來確認學生本人的資料庫概念、SQL、資料庫設計、效能與交易
  處理能力。
- 同儕排序結果不用來直接計算各組正式成績。
- Week 18補考不另增配分；資格、範圍及計分安排待教師另行宣布。
- Exam 2只考Weeks 7-11已教的ER、9.1 mapping、FD與至3NF的內容；candidate keys
  由題目提供，不要求尚未教授的closure或binary lossless-decomposition判定。
- Exam 3才包含Week 13的closure、BCNF與binary lossless decomposition，以及
  索引、transaction basics；累積題只能應用已教過的SQL與database design概念。
- 各次考試是否允許使用或審查 AI 產生的材料，必須在正式考試規則中明示。

## 課堂活動決策

- 全學期規劃5次小組共同回答與個人完整比較，安排於Weeks 2、4、10、11、14。
- 各組先提交一份共同回答與理由；回答鎖定後匿名展示。每位學生排列全部
  回答，系統保存原始排序並彙整平均名次與名次分布，教師最後依技術標準
  回饋，學生再修正。
- 排序時預設匿名並隨機顯示初始順序；彙整結果應能比較納入與排除自己組
  後的差異。
- 單純回憶、固定查詢結果與單一正解題不強制使用排序，以保留 SQL 上機時間。
- 適合的活動包括 SQL 解法比較、ERD/schema 設計、normalization
  decomposition 比較、AI 產出修正與 database application risk 檢查。

## 技術環境與材料狀態

- 正式上機DBMS定為SQLite 3；現有驗證版本為SQLite 3.45.3。學生不必安裝
  server DBMS，能執行課程SQL files的相容SQLite介面皆可使用。
- 學生SQLite套件的維護來源為
  `maintenance/student_sqlite_package/package_files.json`；build script依
  allow-list產生自包含資料夾及ZIP，不把教師檔案或歷史來源帶入。
- 現行SQLite ZIP包含Ch2-Ch7、Ch14-Ch17的synthetic SQL/schema/sample data、
  Ch6/Ch14 diagrams及Ch17 schedule analyzer，仍可用`run_labs.py`重建各章database。
  統一notebook repository則把SQL、Python、data及圖片直接內嵌在對應`chXX.ipynb`，
  不要求另用ZIP、runner或外部asset。
- `maintenance/sql_labs/university_db/`的發布來源與授權尚未確認，不列入
  學生套件，也不作為115-1權威sample database。
- SQLite無法完整示範的stored routines、server-side isolation、deadlock inspection
  與recovery internals，以概念、schedule、log或已驗證教學程式處理，不宣稱為
  SQLite實際server behavior。
- `from_11001_DB/` 是歷史教材與受限制來源，不是可直接發布的學生教材。
- `maintenance/` 是目前建置區；個別 lab、schema、sample database 或
  assessment 仍須另行指定權威版本與可見性。
- `maintenance/assessments/` 內的內容在使用前必須標示 student、
  instructor、practice、historical 或 current，並檢查答案隔離。

## 權威文件與優先順序

1. 教師在目前 task 中明確核准的決定。
2. 國立臺北商業大學官方行事曆與課程行政資料。
3. 本 `PROJECT.md` 記錄的固定決策。
4. `Intro DB/syllabus.md`：英文課綱的維護來源。
5. `maintenance/database_chapter_teaching_material_prompt.md`：逐章教材的範圍、必要講解、
   範例、練習、查核與交付要求。
6. `maintenance/COURSE_PLAN.md`：詳細週次、授課摘要、活動、評量與備課依據。
7. `maintenance/student_sqlite_package/package_files.json`：學生SQLite套件的
   發布allow-list；個別檔案內容仍以對應chapter source為維護來源。
8. `maintenance/course_repository/repository_config.json`：統一notebook
   repository的18週對應、chapter source、SQL、Python、data及image整合清單；內容
   仍受課綱、課程計畫與chapter source控制。
9. `maintenance/archive/1151_course_analysis.md`：本機封存課程分析，不加入Git。
10. `maintenance/archive/1151_database_management_workplan.md`：本機早期草案，
    只保留歷史脈絡，不加入Git。
11. `past_syllabi/` 與 `from_11001_DB/`：歷史與來源材料，不直接控制115-1。

文件若衝突，不得混合內容。先依上述順序判斷，並在修改前指出差異。

## Repository與發布狀態

- 現行結構以2026-09-07決策為準：README作導覽；PROJECT記錄課程事實；AGENTS
  與CLAUDE保留根目錄自動讀取用途並維持byte-identical。課綱直接維護在
  `Intro DB/syllabus.md`，不另外複製或生成第二份課綱。章節來源在
  `maintenance/chapters/`，builder只更新`Intro DB/chXX.ipynb`，不覆寫課綱或README。
  notebook生成檔與維護來源都納入同一main的明確allow-list，課程資料夾共13個檔案。
- `maintenance/archive/COURSES.md`保存已過期的repository狀態；舊首頁來源也已
  封存，不再控制首頁。私人PDF、舊來源、未核准SQL資料、考題、暫存輸出維持忽略。
  下列2026-08-31與2026-09-05分支紀錄是歷史，不代表本次仍需發布雙分支。
- 本資料夾已初始化獨立 Git repository；`main`追蹤
  `https://github.com/KennethWYLee/Database.git`的`origin/main`。
- 現行`KennethWYLee/Database` repository已確認為private。GitHub visibility是
  repository層級，不能在同一private repository內把個別檔案單獨設為public。
  未來應建立另一個public repository或只發布allow-listed release artifact，僅放入
  教師逐項核准的檔案；未核准內容維持在現行private repository。
- `main`已推送，內容是經allow-list檢查的治理文件、課綱、課程
  計畫、Ch2-Ch7與Ch14-Ch19教材、驗證程式、核准的SQLite學生套件、教師審閱前
  audit及第一版學生repository builder。
- 2026-08-31依教師最新決定，發布用course repository不區分教師與學生目錄，也不
  建立weekly或chapter subdirectories。預覽根目錄只有整合導覽、18週進度、課綱與
  課程政策的`README.md`及12份`chXX.ipynb`；每份notebook整合reading、teaching examples、
  executable SQL/Python、practice、outputs及checks，同一份可供一週或兩週使用。
- Ch6與Ch14圖片使用notebook attachments；SQL、JSON及Python examples均內嵌於
  notebook並於執行時使用in-memory database或自動清除的temporary directory，
  因此目前沒有`assets/`、lab runner或外部data dependency。
- Ch2另以`notebook_figures.py`產生原創course-registration relational schema及
  selection/projection pipeline SVG，不複製教科書圖；SVG直接作為notebook
  attachment的維護來源。2026-09-05改為在build時轉成PNG attachment，以符合
  GitHub預覽的顯示方式。Ch2-Ch7與Ch14-Ch17均引導建立SQLite connection、執行DDL、載入
  synthetic data、檢查tables/columns/keys/foreign keys及執行chapter queries。
- 2026-08-31已推送`main` commit `63555f2`與`course-materials` commit `7bd6481`，
  後者保存14個統一course files，根目錄唯一Markdown為README。它是derived review
  copy，修改仍須在`main`的maintained source完成後重新生成。
- 2026-09-05教師另行授權commit/push；`course-materials`已推送`aa06046`的Week 1
  完成稿及`5391b52`的GitHub圖片相容性修正，遠端14個檔案與建置結果比對。
  最新build為`2026.09.05-week1-github-png`。GitHub實際預覽曾無法顯示SVG，改為
  PNG後已確認Week 1表格圖正常顯示；三張圖仍內嵌於同一ch02.ipynb。
  轉圖使用build-only的`resvg-py==0.5.0`，保留箭頭與虛線，不增加學生安裝需求。
  `main`維護來源與本紀錄同批提交；完整commit與同步狀態以Git history及遠端為準。
  repository維持private，未上傳教科書PDF、QA暫存資料或私人舊教材。
- Private GitHub既有`student-preview` branch是前一版chapter-directory預覽，已不
  代表教師最新決定；在教師另行授權commit/push或刪除前保留，不視為維護來源或
  current course release。
- `.gitignore`維持private-by-default。歷史來源、教科書、考題、答案、評分資料、
  暫存檔、prebuilt databases及發布來源未確認的資料不在Git追蹤範圍。
- 新增檔案仍須逐項檢查版權、答案、教師手冊、個資、憑證、檔案大小及發布
  邊界；既有baseline不構成未來檔案的自動核准。

## 目前不一致與未解問題

- [x] Ch2-Ch7與Ch14-Ch19均已建立student guide、可執行活動、instructor
  source/coverage record與verifier；2026-08-27全數重新執行通過。整合結果見
  `maintenance/course_material_integration_report.md`。
- [x] `Intro DB/syllabus.md` 已改為三次考試，並對齊
  ch2-ch7與selected ch14-ch19的正式進度及評量。
- [x] `maintenance/COURSE_PLAN.md` 已依新版英文課綱改為三次考試、Ch2-Ch7與selected
  Ch14-Ch19，並移除學生不需要的教學設計分類名稱與分鐘配置。
- [x] 任課教師官方英文姓名確認為`WenYi Lee`。
- [x] 正式DBMS定為SQLite 3；現有教材以SQLite 3.45.3驗證，允許相容SQLite介面。
- [x] 已建立學生SQLite操作說明、package allow-list、build script、逐檔hash
  manifest及ZIP；2026-08-27由乾淨臨時目錄執行Ch2-Ch7與Ch14-Ch17全部通過。
- [x] `package_files.json`已指定SQL labs、schema、sample data、diagrams及Ch17
  schedule files的權威發布清單；chapter source仍是內容維護來源。
- [x] 教師於2026-08-27核准目前SQLite ZIP與student README供本課程發布使用。
- [x] 已建立GitHub remote，`main`已追蹤`origin/main`。
- [x] 已建立`maintenance/pre_instructor_review_audit.md`，記錄全課程來源、
  一致性、執行、套件與發布安全檢查。
- [x] 教師已決定Week 9複習Ch2-Ch5、English-only學生教材、縮減Ch15-Ch16與
  Ch18-Ch19課堂核心、官方英文姓名及GitHub選擇性公開方向；決定已套用。
- [x] Ch2-Ch7與Ch14-Ch19的`student_guide.md`已改寫為English-only prose。
- [x] 2026-08-31曾將course repository改為12份根目錄`chXX.ipynb`；當時生成14個檔案，包含
  12份notebook、唯一Markdown檔`README.md`與`.gitignore`，沒有額外asset。README
  內含導覽、18週進度、課綱與課程政策。全部notebook
  已逐cell執行，English-only、internal path、external dependency、attachment、
  manifest及預期檔案集合檢查通過。
- [x] Ch2兩張Python-generated SVG已完成XML parse與PNG render visual QA；修正arrow
  label重疊後未見裁切。10份SQL notebooks均實際輸出table、column、primary key、
  unique constraint、foreign key及foreign-key check，Ch18-Ch19明列simulation boundary。
- [x] SQLite ZIP的`run_labs.py`仍支援原有`materials/`package，2026-08-28重建ZIP後
  10組activities通過；統一notebook repository不再依賴runner或ZIP。
- [ ] 教師完成英文學生教材的內容與語言審閱；在此之前不得把全部逐章教材標示為
  student-ready。這是全課程的人工審閱紀錄，不阻擋已委託完成的Week 1編寫與驗證。
- [x] Week 1七段範例輸出與預期一致；Week 1、Week 2與完整Ch2均已用fresh Jupyter
  kernel執行，前後週資料互不依賴；新增圖與Week 1的HTML顯示已檢查。
- [x] 已重新定位教科書PDF並複製至本課私人參考資料夾，確認版本、檔案雜湊與Git排除。
- [x] 已依重新定位的教科書及全部29頁官方Ch2投影片核對Week 1，並修正三處
  說明與範例。Ch2 coverage record區分早期未找到PDF的紀錄與本次原文查核；
  原文查核不代表教師已核准教學份量或其餘章節已重新審閱。
- [x] Week 1六項目標均已有解釋、具體範例、預測、結果判讀及可檢查的練習。
  補齊不同檔案email衝突、重複值與完整重複tuple比較、連續修改摘要，以及具體的
  DB205新增與WD120更新練習；七段學生程式與Week 2界線不變。
- [x] 修正notebook生成器缺少cell ID的格式問題；12份原始JSON通過nbformat schema
  檢查。其餘11章只新增格式欄位，內容未變；重建14個預覽檔案及manifest的hash一致。
- [ ] 教師審閱course repository的`README.md`與代表`chXX.ipynb`，確認後再決定
  public repository名稱、建立時間及GitHub Release方式。
- [ ] 逐項建立GitHub公開allow-list並決定公開時機；之後另建public repository或
  allow-listed release artifact，未核准檔案不得移出現行private repository。
- [ ] 完成三次考試藍圖、題型、允許資源、AI規則與評分方式。
- [ ] 決定課堂排序使用既有平台或自建系統，並測試30人、6組、匿名展示、
  排除自己組及原始資料匯出。

## Primary next action

本次課綱及配分已修正，下一步仍為依正確課本建立逐節與現有教材的對照，
但範圍現在以核准的英文課綱為準，不再等待教師重新選章。完成條件是每個必教
主題均能定位至原書或已標示的實作補充來源，並列出可沿用、需修正及缺少的
教材；接著才逐章重編、完整來源查核與驗證。不能用既有生成器的舊章號或歷史
週次對照宣稱新課綱教材已完成。下方保留較早建議作追溯。

2026-09-08教師確認現用書為Elmasri/Navathe第7版，因此主要下一步改為重新建立
現有教學主題與正確課本章、節的對照，指出教材缺口及需要教師判斷的範圍差異。
此新證據取代「繼續另一本文獻Ch4」的舊建議。預期成果是可核對原書位置的
對照表；完成條件為每個既有主要教學主題均有經閱讀確認的位置或明確缺口，
不把兩本書相同章號視為相同內容，不自行增刪章節或變更評量政策。
接著依確認後的範圍逐章完整查核。即時狀態以
`maintenance/course_repository/full_source_audit.md`為準。以下段落保留歷史脈絡。

教師於2026-09-05進一步要求直接完成Week 1，因此原先「先由教師審閱Week 1」
的下一步已由這項新指示取代。Week 1的編寫、來源查核、程式與顯示驗證已完成，
目前沒有需要轉交教師處理的Week 1客觀檢查或內容阻擋問題。

2026-09-07目錄遷移已完成並同步至`ba20cda`，不再延續雙分支同步。
之後教師核准Ch2修正並澄清首堂先課綱、再概談Ch2，因此本次優先完成這些內容及
受影響驗證，而非延續已完成的目錄遷移。新增客觀問題均已修正；具體證據見
`maintenance/chapters/ch02_relational_model/instructor/coverage_and_verification.md`。

2026-09-07教師新增以大量圖片講解的要求，取代先選定首堂停止位置的下一步。
Ch2目前有19張內嵌圖片，其他11章各有2至3張，共45張。新增圖由Python維護，
使用既有教材例子呈現資料表前後差異、關聯、運算步驟及交易圖，不複製教科書圖。
每張圖放在對應段落，保持一章一份notebook，不增加學生外部檔案、作業或考試範圍。
詳細來源、驗證及限制見`maintenance/course_repository/visual_teaching_review.md`。

主要下一步是教師用Ch2的圖確認投影講解是否清楚。理由是本機圖像與執行檢查
不能替代實際教室的觀看距離；預期成果是確認字級及圖解順序，完成條件是能在
實際投影下辨讀欄位、數值與箭頭，沒有需要放大重畫的圖。教師已於2026-09-07
授權將本次Ch2修正、全章圖解及驗證紀錄commit並push至既有origin/main，供線上
審閱；實際同步狀態以Git紀錄為準。未來只提供Ch2給學生及公開allow-list維持
獨立操作，不先下架任何章節，也不變更repository可見性。
