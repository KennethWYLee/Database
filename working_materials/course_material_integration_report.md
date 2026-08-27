# 資料庫管理逐章教材整合報告

日期：2026-08-27
狀態：Ch2-Ch7、Ch14-Ch19初稿及自動驗證完成；尚未核准發布

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
| 16 | `chapters/ch16_query_optimization/` | safe rewrites、outer-join counterexample、statistics與skew | Pass |
| 17 | `chapters/ch17_transactions/` | boundaries、ACID、schedules、small precedence graphs、isolation | Pass |
| 18 | `chapters/ch18_concurrency_control/` | S/X locks、2PL、wait-for graph與deadlock | Pass |
| 19 | `chapters/ch19_recovery_system/` | failures、WAL、redo/undo、basic checkpoint與backup+log | Pass |

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
- 2026-08-27驗證ZIP SHA-256：
  `256d97bd2c93e62cb08ec898531c42739d93c1a1acb73c8efa93caa2afe2296a`。
- Manifest逐檔bytes與SHA-256檢查通過；ZIP未包含instructor、answer、solution、
  assessment、`__pycache__`或prebuilt database files。
- ZIP已解壓至乾淨臨時目錄，使用Python 3.12.9及SQLite 3.45.3重建並通過
  Ch2-Ch7、Ch14-Ch17共10組activities；Ch17 schedule analyzer亦執行通過。
- 教師於2026-08-27核准目前ZIP與student README供本課程發布使用；尚未上傳LMS
  或其他校內系統。

## 6. 仍待決定

1. Student-facing prose維持「繁體中文說明加English technical terms」，或改成
   English-only。
2. SQLite學生套件在LMS或校內系統的實際發布位置。
3. 從實際下載位置重新核對ZIP hash與manifest。
4. 三次考試藍圖、允許資源、AI規則與rubric。
5. Instructor official English name spelling。
6. 逐章student guides的課堂核心與課後延伸標示仍需教師做最後語言審閱。

## 7. Primary Next Action

依 `PROJECT.md`，下一步是決定SQLite學生套件在LMS或校內系統的固定下載位置並
上傳已核准ZIP。預期成果是可供本課學生下載的連結；完成條件是從該位置取得的
ZIP hash與manifest一致，並能依README在乾淨環境通過全部10組activities。
