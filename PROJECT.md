# 資料庫管理 - Project Context

本檔只記錄資料庫管理課程的事實、固定決策、權威文件、核准用語、限制與
未解問題。通用工作規則見 `AGENTS.md`；`CLAUDE.md` 是其位元一致鏡像。

- 最後更新日期：2026-08-28
- 課程狀態：115-1課綱、18週課程計畫、章節範圍、三次考試與SQLite環境已對齊；
  教師審閱前客觀檢查完成，2026-08-27的範圍與語言決策已套用至英文學生教材；
  2026-08-28完成並驗證依18週導覽的本機學生repository預覽
- Repository：本資料夾是獨立 Git repository；`main`追蹤GitHub的`origin/main`，
  目前已推送的基準commit為`2f3a307`
- 文件可見性：混合；歷屆考題、答案、評分資料及教師手冊不得直接發布

## 課程定位與對象

- 課程名稱：資料庫管理（Database Management）
- 任課教師官方英文姓名：WenYi Lee。
- 對象：四技資訊管理系二年級必修課程學生。
- 學分與時數：3 學分，每週 3 小時。
- 上課時間：星期四第 5-7 節，13:30-16:15。
- 課程主體：relational model、relational algebra、SQL、E-R model、
  relational schema、functional dependencies、normalization，以及選定的
  indexing、query processing、query optimization、transactions、concurrency
  control與recovery內容。
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

## 教科書與已驗證章節

- 現行主要教科書與投影片來源：Silberschatz, Korth, and Sudarshan,
  *Database System Concepts*, 7th Edition。
- 2026-08-27重新確認的本機私人教科書PDF標題、作者與版本均符合上述資料；該
  PDF只作教師端來源查核，不納入Git或學生套件。
- 已完整查核本課正式範圍的教科書Ch2-Ch7、Ch14-Ch19正文及對應官方
  slides；Ch8-Ch9另核對封面與章節綱要並決定不列入必修進度。不得再把
  舊課綱使用的 *Fundamentals of Database Systems, 7/e* 當成本學期現行教材。

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
- 教師於 2026-11-01 至 2026-11-07 參加 INFORMS；Week 9 的
  2026-11-05 不排實體課、考試或新進度，只安排 ch2-ch5 非同步複習。
- Week 17 的 2026-12-31 為校慶補假，不排課。
- Week 6 的 2026-10-15 辦理Exam 1；Week 12的2026-11-26辦理Exam 2。
- Week 16 的 2026-12-24 完成ch18-ch19選講與期末複習。
- Week 18 的 2027-01-07 是校定期末考週，辦理Exam 3與課程期末考。

## 評量與章節對應

| 評量 | 週次與日期 | 比例 | 範圍 |
|---|---|---:|---|
| Written Exam 1 | Week 6, 2026-10-15 | 25% | ch2-ch4 |
| Written Exam 2 | Week 12, 2026-11-26 | 25% | 選定的ch5-ch7內容 |
| Written Exam 3 / Final Examination | Week 18, 2027-01-07 | 30% | 選定的ch14-ch19內容，並累積應用SQL與database design概念 |
| Class Performance（課堂表現） | 全學期 | 20% | SQL labs、database design exercises、ER diagrams、schemas、normalization、index與query-plan activities、個人回答與修正；peer rank不直接計分 |

- 三次考試都用來確認學生本人的資料庫概念、SQL、資料庫設計、效能與交易
  處理能力。
- 同儕排序結果不用來直接計算各組正式成績。
- Exam 2只考課前已明列並實際教授的selected ch5-ch7內容。
- Exam 3只考課前已明列並實際教授的selected ch14-ch19內容；累積題只能應用
  已教過的SQL與database design概念。
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
  `working_materials/student_sqlite_package/package_files.json`；build script依
  allow-list產生自包含資料夾及ZIP，不把教師檔案或歷史來源帶入。
- 現行套件包含Ch2-Ch7、Ch14-Ch17的synthetic SQL/schema/sample data、Ch6/Ch14
  diagrams及Ch17 schedule analyzer。學生可用`run_labs.py`重建各章database。
- `working_materials/sql_labs/university_db/`的發布來源與授權尚未確認，不列入
  學生套件，也不作為115-1權威sample database。
- SQLite無法完整示範的stored routines、server-side isolation、deadlock inspection
  與recovery internals，以概念、schedule、log或已驗證教學程式處理，不宣稱為
  SQLite實際server behavior。
- `from_11001_DB/` 是歷史教材與受限制來源，不是可直接發布的學生教材。
- `working_materials/` 是目前建置區；個別 lab、schema、sample database 或
  assessment 仍須另行指定權威版本與可見性。
- `working_materials/assessments/` 內的內容在使用前必須標示 student、
  instructor、practice、historical 或 current，並檢查答案隔離。

## 權威文件與優先順序

1. 教師在目前 task 中明確核准的決定。
2. 國立臺北商業大學官方行事曆與課程行政資料。
3. 本 `PROJECT.md` 記錄的固定決策。
4. `1151_database_management_revised_syllabus.md`：英文課綱的維護來源。
5. `database_chapter_teaching_material_prompt.md`：逐章教材的範圍、必要講解、
   範例、練習、查核與交付要求。
6. `COURSE_PLAN.md`：詳細週次、授課摘要、活動、評量與備課依據。
7. `working_materials/student_sqlite_package/package_files.json`：學生SQLite套件的
   發布allow-list；個別檔案內容仍以對應chapter source為維護來源。
8. `working_materials/student_repository/repository_config.json`：學生GitHub版的18週
   入口、閱讀連結、activities及evidence清單；內容仍受課綱、課程計畫與chapter
   source控制。
9. `1151_course_analysis.md`：課程分析。
10. `1151_database_management_workplan.md`：早期草案，只保留歷史脈絡。
11. `past_syllabi/` 與 `from_11001_DB/`：歷史與來源材料，不直接控制115-1。

文件若衝突，不得混合內容。先依上述順序判斷，並在修改前指出差異。

## Repository與發布狀態

- 本資料夾已初始化獨立 Git repository；`main`追蹤
  `https://github.com/KennethWYLee/Database.git`的`origin/main`。
- 現行`KennethWYLee/Database` repository已確認為private。GitHub visibility是
  repository層級，不能在同一private repository內把個別檔案單獨設為public。
  未來應建立另一個public repository或只發布allow-listed release artifact，僅放入
  教師逐項核准的檔案；未核准內容維持在現行private repository。
- 基準commit `2f3a307`已推送，內容是經allow-list檢查的治理文件、課綱、課程
  計畫、Ch2-Ch7與Ch14-Ch19教材、驗證程式、核准的SQLite學生套件及教師審閱前
  audit。
- 2026-08-28依教師決定參考FinTech課程的週次入口，新增可重複建置的本機學生
  repository預覽。預覽只有簡短首頁、英文課綱、18週索引、每週頁面及`resources/`；
  chapter guides與SQLite labs由現有維護來源及allow-list複製，不自動發布。
- `.gitignore`維持private-by-default。歷史來源、教科書、考題、答案、評分資料、
  暫存檔、prebuilt databases及發布來源未確認的資料不在Git追蹤範圍。
- 新增檔案仍須逐項檢查版權、答案、教師手冊、個資、憑證、檔案大小及發布
  邊界；既有baseline不構成未來檔案的自動核准。

## 目前不一致與未解問題

- [x] Ch2-Ch7與Ch14-Ch19均已建立student guide、可執行活動、instructor
  source/coverage record與verifier；2026-08-27全數重新執行通過。整合結果見
  `working_materials/course_material_integration_report.md`。
- [x] `1151_database_management_revised_syllabus.md` 已改為三次考試，並對齊
  ch2-ch7與selected ch14-ch19的正式進度及評量。
- [x] `COURSE_PLAN.md` 已依新版英文課綱改為三次考試、Ch2-Ch7與selected
  Ch14-Ch19，並移除學生不需要的教學設計分類名稱與分鐘配置。
- [x] 任課教師官方英文姓名確認為`WenYi Lee`。
- [x] 正式DBMS定為SQLite 3；現有教材以SQLite 3.45.3驗證，允許相容SQLite介面。
- [x] 已建立學生SQLite操作說明、package allow-list、build script、逐檔hash
  manifest及ZIP；2026-08-27由乾淨臨時目錄執行Ch2-Ch7與Ch14-Ch17全部通過。
- [x] `package_files.json`已指定SQL labs、schema、sample data、diagrams及Ch17
  schedule files的權威發布清單；chapter source仍是內容維護來源。
- [x] 教師於2026-08-27核准目前SQLite ZIP與student README供本課程發布使用。
- [x] 已建立GitHub remote並將基準commit `b204458`推送至`origin/main`。
- [x] 已建立`working_materials/pre_instructor_review_audit.md`，記錄全課程來源、
  一致性、執行、套件與發布安全檢查。
- [x] 教師已決定Week 9複習Ch2-Ch5、English-only學生教材、縮減Ch15-Ch16與
  Ch18-Ch19課堂核心、官方英文姓名及GitHub選擇性公開方向；決定已套用。
- [x] Ch2-Ch7與Ch14-Ch19的`student_guide.md`已改寫為English-only prose。
- [x] 已建立簡化學生repository的本機預覽builder；54個檔案、35個Markdown、
  18個週次頁面、學生可見英文與本地連結檢查通過，10組SQLite activities在乾淨
  暫存複本全部通過。
- [ ] 教師完成英文學生教材的內容與語言審閱；在此之前不得把全部逐章教材標示為
  student-ready。
- [ ] 教師審閱學生repository首頁、18週索引與代表週次頁面，確認後再決定public
  repository名稱、建立時間及GitHub Release方式。
- [ ] 逐項建立GitHub公開allow-list並決定公開時機；之後另建public repository或
  allow-listed release artifact，未核准檔案不得移出現行private repository。
- [ ] 完成三次考試藍圖、題型、允許資源、AI規則與評分方式。
- [ ] 決定課堂排序使用既有平台或自建系統，並測試30人、6組、匿名展示、
  排除自己組及原始資料匯出。

## Primary next action

教師已明確要求先簡化學生使用路徑，因此下一步改為審閱生成後的學生repository首頁、
18週索引、Week 1、Week 9、Week 14及Week 17頁面，再抽查Ch15-Ch16與Ch18-Ch19
英文閱讀。預期成果是核准或修正學生導覽及高負荷週次；完成條件是學生能從首頁兩次
點擊內找到本週reading、practice或lab、evidence要求，且教師核准第一批public
allow-list與獨立repository名稱。
