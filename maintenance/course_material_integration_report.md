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

- 維護來源：`maintenance/student_sqlite_package/package_files.json`。
- 生成內容：18個核准chapter assets，加上README、runner及manifest，共21個files。
- 生成ZIP：`maintenance/student_sqlite_package/output/sqlite_course_package.zip`。
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

## 6. 最新修訂與後續事項

### 2026-09-05 Week 1更新

- 教師核准優先修改Week 1；同一份ch02.ipynb加入兩週範圍、第一週停止點、
  單一student relation圖、七段就地執行範例及具體練習表。
- 正式keys分類、schema diagrams、algebra與完整四表SQL setup保留在Week 2；
  Week 1僅引入識別欄位用途。兩週使用獨立資料庫，第一週的修改不會流入後續章節。
- 課綱、計畫與README週次對齊；未改考試日期、配分、原有SQL套件或其他章節範圍。
- 全部12份notebook重新建置通過；Ch2三種fresh-kernel執行與畫面檢查的詳細證據
  見Ch2 coverage record。此更新的早期階段尚未重新定位完整教科書PDF，當時使用
  官方slides與執行證據查核；後續原文查核與修正如下。

### 2026-09-05 教科書查核後的局部修正

- 已找到並私下保存第7版PDF，閱讀完整Ch2及Week 1需要的Ch1/Ch3相關段落。
- 依教師核准，區分查詢結果去重與原表資料、把course的room練習改為description，
  並新增atomic values的前後電話表格與完整查找步驟；學生程式仍是七段。
- `2026.09.05-week1-textbook-review`重建及全部12份notebook執行通過；Ch2兩支
  verifier與三組fresh-kernel執行通過，桌面及手機顯示已檢查。
- 與三處修正前相比，生成預覽僅ch02.ipynb改變，其餘13個檔案hash相同。
  未改課綱、週次、配分或SQLite ZIP，未commit/push；教師內容與份量審閱仍待完成。

### 2026-09-05 Week 1完成

- 依教師進一步要求，已直接完成Week 1，不把教師逐份審閱列為本次完成條件。
  版本為`2026.09.05-week1-complete`；沒有新增課堂主題、學生程式、週次或配分。
- 六項原有目標均有解釋、具體範例、預測、操作或判斷、結果判讀及練習。補上
  email檔案衝突、完整重複tuple比較、連續修改摘要及DB205/WD120具體練習。
  教材明確供教師講解與示範，保留輸出讓學生課後複習，不改為純自學課程。
- 嚴格原始JSON檢查發現缺少cell ID，已修正維護中的生成器；12份notebook的
  原始schema驗證與全數程式執行通過。其他11章只補格式欄位，教學內容未變。
- Ch2兩支verifier與三組fresh-kernel執行通過，桌面及手機的範例、練習、停止點
  已檢查。連續兩次重建的14個預覽檔案與manifest雜湊完全一致。
- Week 1編寫、來源查核、執行與本機顯示檢查完成，沒有尚待教師處理的客觀
  阻擋項目。未宣稱教師親自審閱或實際學生測試；未commit/push。

### 後續事項

1. 其餘週次的內容審閱與教學份量確認仍屬後續全課程工作，不阻擋Week 1完成。
2. 建立第一批GitHub公開allow-list、獨立public repository或release artifact，並決定
   公開時機；未核准檔案維持在現行private repository。
3. 從未來實際GitHub下載位置重新核對ZIP hash與manifest。
4. 完成三次考試藍圖、允許資源、AI規則與rubric。
5. 選擇並測試課堂匿名展示及排序平台。

## 7. Primary Next Action

2026-09-07更新：教師改採本機與GitHub相同的main目錄。`Intro DB/`提供單一課綱
與12份章節notebook，維護來源集中到`maintenance/`；Week 1的修正或理由措辭
已統一，移動後驗證通過。主要後續動作僅在另獲授權後將同一main的來源與成品
一併commit/push，核對遠端目錄與連結。詳見`structure_migration_review.md`；
本次不更新舊預覽分支。下段保留2026-09-05的歷史同步紀錄。

教師要求直接完成Week 1的新指示取代先請教師審閱的原建議；編寫與驗證已完成。
教師隨後另行授權commit/push，`course-materials`已更新至`5391b52`。發布時發現
GitHub不顯示SVG attachment，已從維護中的SVG產生PNG內嵌圖片，並確認Week 1
圖解在線上正常顯示。版本為`2026.09.05-week1-github-png`；前述未發布紀錄是
編寫階段的歷史狀態。`main`來源與本紀錄同批提交，實際同步以Git遠端為準。
本次不自動擴寫Week 2，不把其餘週次的待辦轉作Week 1完成的前置條件。
