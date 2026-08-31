# 資料庫管理逐章教材整合報告

日期：2026-08-27
狀態：Ch2-Ch7、Ch14-Ch19已改寫為English-only學生教材，仍待教師內容審閱；
SQLite學生套件已核准供本課發布

## 1. 完成範圍

| 章節 | 教材目錄 | 課堂定位 | 驗證狀態 |
|---:|---|---|---|
| 2 | `chapters/ch02_relational_model/` | relational model、keys、relational algebra | Pass |
| 3 | `chapters/ch03_introduction_to_sql/` | basic SQL、NULL、aggregation、subqueries、modification | Pass |
| 4 | `chapters/ch04_intermediate_sql/` | joins、views、constraints、basic transactions | Pass |
| 5 | `chapters/ch05_advanced_sql/` | window functions、recursive CTE、one audit trigger；routines作概念介紹 | Pass |
| 6 | `chapters/ch06_er_design/` | ER model、constraints、mapping | Pass |
| 7 | `chapters/ch07_normalization/` | anomalies、FDs、lossless decomposition、3NF/BCNF | Pass |
| 14 | `chapters/ch14_indexing/` | index use、B+ tree access、composite/covering index、plan evidence | Pass |
| 15 | `chapters/ch15_query_processing/` | logical/physical plan、scans、index searches與join order | Pass |
| 16 | `chapters/ch16_query_optimization/` | equivalence、basic selectivity、statistics、`ANALYZE`與plan evidence | Pass |
| 17 | `chapters/ch17_transactions/` | boundaries、ACID、schedules、small precedence graphs、isolation | Pass |
| 18 | `chapters/ch18_concurrency_control/` | S/X locks、grant/wait、wait-for graph與deadlock | Pass |
| 19 | `chapters/ch19_recovery_system/` | failure distinction、log records、WAL與simplified redo/undo | Pass |

每個目錄均有 `README.md`、`student_guide.md`、instructor-only
`coverage_and_verification.md`、至少一項可執行活動，以及獨立 verifier。Ch6與Ch14
另有已 render並檢查的原創 diagrams。

## 2. 評量對應

| 評量 | 比例 | 教材範圍 | 主要可保存證據 |
|---|---:|---|---|
| Exam 1 | 25% | Ch2-Ch4 | key/relational-algebra判斷、SQL結果、join/view/constraint分析 |
| Exam 2 | 25% | selected Ch5-Ch7 | advanced SQL、ERD/schema mapping、FD/decomposition/3NF/BCNF |
| Exam 3 | 30% | selected Ch14-Ch19，累積應用已教SQL/design | index/plan證據、transaction schedule、locks/deadlock、recovery log |
| Class Performance | 20% | 全學期已教活動 | SQL files、diagram/schema、預測、執行輸出、理由、修正紀錄 |

Student guides中的worked examples與self-check criteria是已發布練習回饋，不是未發布
考題答案。正式考試題目、答案與評分內容未加入這些目錄。

## 3. 章節銜接

- Ch2建立relations、keys與algebra；Ch3-Ch5把它們轉成SQL。
- Ch6由business rules建立ER model與schema；Ch7用FDs與normal forms檢查設計。
- Ch14建立physical access概念；Ch15-Ch16用plan與statistics解釋執行和最佳化。
- Ch17定義transaction correctness；Ch18提供concurrency-control mechanisms；Ch19
  處理failure後的atomicity與durability。
- Ch15與Ch16共同使用department/course/student workload；Ch17-Ch19共同使用帳戶與
  transaction history，使後半段可連續討論correctness、control與recovery。

## 4. SQL與資料環境

- Ch2-Ch5及多數SQL checks延續course-registration/university關係資料；Ch6映射相同
  domain；Ch7使用刻意含anomaly的設計例子。
- Ch14使用deterministic 20,000-row order workload；Ch15-Ch16使用deterministic
  query-plan workloads。
- Ch17 SQLite transaction lab使用account/transfer case；Ch18-Ch19使用DBMS-neutral
  Python teaching models，避免把SQLite-specific locking/recovery誤當一般規則。
- 正式上機DBMS定為SQLite 3；已驗證環境是Python 3.12.9所含SQLite 3.45.3。
  SQLite無法完整呈現的product-specific isolation、lock inspection、deadlock、
  backup/restore及point-in-time recovery以概念、schedule、log或教學程式處理，
  不列為server DBMS實作要求。

## 5. 驗證結果

2026-08-27由course root重新執行12個verifiers，全部exit code 0。涵蓋：

- schema、constraints、foreign keys、SQL results及reversible modifications；
- ER SVG/PNG與B+ tree SVG/PNG可解析和render；
- normalization lossless/lossy examples、query results、plans、statistics及skew；
- transaction rollback/commit、schedule graphs、recoverability；
- S/X compatibility、2PL、wait-for cycle、version visibility、write skew；
- restart redo/undo、WAL order及backup+log restore。

原有逐章教材另行通過17個Python files的syntax parse、4個JSON files的parse，以及
所有local Markdown image paths檢查。學生套件的2個維護中Python scripts亦通過
syntax check，package config與生成manifest均在build時成功parse。未執行項目包括
真實server DBMS concurrency、power-loss crash、corrupted storage、production
restore、remote failover及ARIES。

### SQLite學生套件

- 維護來源：`working_materials/student_sqlite_package/package_files.json`。
- 生成內容：18個核准chapter assets，加上README、runner及manifest，共21個files。
- 生成ZIP：`working_materials/student_sqlite_package/output/sqlite_course_package.zip`。
- 2026-08-28重建並驗證的ZIP SHA-256：
  `15f6847ad7163db552536231427010f68ef1731606726ba05bf298ce40001e05`。
- Manifest逐檔bytes與SHA-256檢查通過；ZIP未包含instructor、answer、solution、
  assessment、`__pycache__`或prebuilt database files。
- ZIP已解壓至乾淨臨時目錄，使用Python 3.12.9及SQLite 3.45.3重建並通過
  Ch2-Ch7、Ch14-Ch17共10組activities；Ch17 schedule analyzer亦執行通過。
- 教師於2026-08-27核准目前ZIP與student README供本課程使用；現行GitHub course
  repository已確認為private。未來只在另一個public repository或allow-listed release
  artifact放入核准檔案；本次未公開、上傳或push。

### 統一notebook repository

- 2026-08-28依教師最新決定，course repository不再分教師/學生或weekly/chapter
  directories；根目錄直接提供`ch02.ipynb`至`ch19.ipynb`共12份章節notebook。
- 每份notebook整合既有English chapter reading、teaching examples、SQL或Python
  demonstrations、practice及reproducibility checks；Ch6與Ch14圖片以attachment內嵌。
- Ch2新增兩張由Python標準庫產生的原創SVG：course-registration relational schema及
  selection/projection pipeline；XML parse與PNG visual QA通過，未複製教科書圖。
- SQL使用Python標準庫`sqlite3`與in-memory database；Ch17-Ch19模擬程式及JSON data
  於cell內嵌，執行時只建立會自動清除的temporary directory。
- Ch2-Ch7與Ch14-Ch17加入一致的database build順序，實際列出tables、columns、
  primary keys、unique constraints、foreign keys及`PRAGMA foreign_key_check`結果；
  Ch18-Ch19說明改用simulation的SQLite能力邊界。
- 生成結果共14個files：12份notebook、唯一Markdown檔`README.md`及`.gitignore`；
  README整合導覽、18週進度、課綱與課程政策，且`ASSET_FILES=0`，沒有lab runner、
  chapter subdirectory或外部data。
- 12份notebook全部逐cell執行通過；manifest、English-only、internal path、external
  dependency、attachment及精確檔案集合檢查均通過。

## 6. 仍待執行

1. 教師審閱English-only逐章notebook的內容、術語、閱讀順序及核心/延伸標示。
2. 建立第一批GitHub公開allow-list、獨立public repository或release artifact，並決定
   公開時機；未核准檔案維持在現行private repository。
3. 從未來實際GitHub下載位置重新核對ZIP hash與manifest。
4. 完成三次考試藍圖、允許資源、AI規則與rubric。
5. 選擇並測試課堂匿名展示及排序平台。

## 7. Primary Next Action

依 `PROJECT.md`與`pre_instructor_review_audit.md`，下一步是教師審閱生成後的
`README.md`及代表性的`ch02.ipynb`、`ch06.ipynb`、`ch15.ipynb`、`ch18.ipynb`、
`ch19.ipynb`。預期成果是明確修正或核准notebook閱讀順序與份量；完成條件是概念、
範例、預測、執行、判讀及practice的順序獲確認，再決定何時更新GitHub預覽。
