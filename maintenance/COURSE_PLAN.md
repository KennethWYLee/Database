# 115-1 資料庫管理課程計畫

更新日期：2026-09-07
狀態：現行備課依據；2026-08-27客觀檢查及教師範圍/語言決策已套用，仍待教師
審閱英文學生教材後才能把全部逐章教材標示為student-ready

## 一、課程定位

- 對象：四技資訊管理系二年級必修課程學生。
- 學分：3 學分。
- 上課時間：星期四第 5-7 節，13:30-16:15。
- 任課教師官方英文姓名：WenYi Lee。
- 正式學生教材語言：English-only prose。
- 主要教科書：Silberschatz, Korth, and Sudarshan, *Database System Concepts*,
  7th Edition。
- 正式上機環境：SQLite 3。現有教材以 SQLite 3.45.3 驗證；學生可使用能執行
  課程 SQL 檔案的相容介面。
- 課程主線：relational model、SQL、E-R model、relational schema、normalization、
  indexing、query plans、transactions、concurrency control 與 recovery。
- Ch8 與 Ch9 不列入正式授課及考試範圍。

SQLite 不支援或不能完整呈現的 stored routines、server-side isolation、deadlock 與
recovery internals，以概念說明、圖解、schedule、log 或已驗證的教學程式呈現。學生
不需要為本課另行安裝 server DBMS，也不會因未使用特定產品而失去評量分數。

## 二、課程目標

完成本課後，學生應能：

1. 以 relations、schemas、keys 與核心 relational algebra 說明資料庫結構及查詢。
2. 撰寫、執行並驗證 SQL，說明結果、`NULL`、joins、aggregation、subqueries、
   views 與 constraints 的行為。
3. 根據 business rules 建立 E-R diagram，並映射為具備合理 keys 與 constraints
   的 relational schema。
4. 使用 functional dependencies、anomalies、lossless decomposition、3NF 與 BCNF
   檢查資料表設計。
5. 根據 workload 與 query-plan evidence 評估 index 與查詢執行方式。
6. 分析 transaction boundaries、concurrent schedules、locks、deadlocks、logs 及
   基本 recovery decisions。
7. 在允許使用 AI 的活動中，以資料、執行結果、圖形規則或 query plan 驗證輸出，
   並說明修正理由與仍存在的限制。

## 三、正式章節範圍

| 章節 | 課堂核心內容 | 課後延伸或概念介紹 |
|---:|---|---|
| Ch2 | relations、schemas、keys、schema diagrams；selection、projection、Cartesian product、join 與 set operations | 複雜 relational-algebra 推導、完整 rename 與 assignment 表示法 |
| Ch3 | DDL basics、basic queries、expressions、duplicates、string patterns、ordering、`NULL`、aggregation、`GROUP BY`/`HAVING`、`IN`/`EXISTS`、selected subqueries/CTEs、basic modification | `SOME`/`ALL`、`UNIQUE`、`LATERAL`、formal multiset algebra、advanced modification |
| Ch4 | explicit inner join、left outer join、`ON`/`USING`、outer join 中 `ON` 與 `WHERE` 的差異、views、constraints、basic transaction statements | right/full outer join、view update 細部規則、materialized views、deferred constraints、assertions、authorization |
| Ch5 | window ranking、recursive CTE、一個 row-level audit trigger；stored function/procedure 的用途與 interface | stored routine 實作、完整 procedural SQL、專屬 pivot、rollup/cube；conditional aggregation 作短示範 |
| Ch6 | design process、entities、attributes、relationships、cardinalities、participation、keys、design decisions、ER-to-relational mapping | extended E-R features、alternative notations |
| Ch7 | anomalies、functional dependencies、attribute closure、binary lossless decomposition、spurious tuples、3NF 與 BCNF 的基本判斷 | dependency preservation 的取捨、完整 theory、canonical cover 與分解演算法 |
| Ch14 | index 使用時機、B+ tree lookup/range 概念、複合索引欄位順序、covering index、`CREATE INDEX` 與 query-plan evidence | dense/sparse、clustering/secondary 的概念比較、B+ tree split、完整 insertion/deletion 與 cost derivation |
| Ch15-16 | scan 與 index search、logical/physical plan基本區分、plan access order、result-equivalence check、basic equality selectivity、catalog statistics、`ANALYZE` 與 `EXPLAIN QUERY PLAN` | materialization、pipelining、完整 join algorithms、selection/projection pushdown、join reorder、outer-join反例、skew細節、cost formulas、dynamic programming與optimizer internals |
| Ch17 | transaction boundaries、ACID、states、schedules、conflicts、small precedence graphs、conflict serializability、basic recoverability、isolation phenomena | 完整 serializability-testing algorithm、各類實作 protocol |
| Ch18 | S/X locks、compatibility、grant/wait、wait-for graph、deadlock detection及victim/retry注意事項 | basic/strict/rigorous 2PL、timestamp protocol、MVCC、snapshot isolation與write skew |
| Ch19 | transaction/system/storage failure基本區分、log old/new values、WAL ordering、committed/incomplete判斷及單一簡化redo/undo案例 | checkpoint、backup加後續log、ARIES、fuzzy checkpoint、force/steal、remote failover與production recovery administration |

課後延伸內容只有在教師另行講解、示範及安排練習後，才能列入正式評量。

## 四、授課方式

課堂依內容交替使用概念講解、完整範例、個人預測、SQL 或圖形操作、小組比較、
全班檢視、教師回饋及個人修正。固定答案的查詢與名詞題以個人作答及教師講解
處理；需要比較設計理由的題目才使用匿名展示與完整排序。

全學期安排五次完整的小組回答比較，預定在 Weeks 2、4、10、11、14：

1. key 與 schema 判斷。
2. SQL 修正方案比較。
3. E-R diagram 與 relational schema 比較。
4. normalization decomposition 比較。
5. AI 提出的 index 建議與 query-plan evidence 比較。

每組先提交一份有理由的回答，之後匿名展示。每位學生比較全部回答，教師依
課程技術標準指出正確、錯誤與限制，學生再提交自己的修正。比較結果用於討論，
不直接決定任何組別的成績。

## 五、18 週授課摘要

| 週次 | 日期 | 章節 | 授課摘要 | 教學與範例 | 學習證據 |
|---:|---|---|---|---|---|
| 1 | 2026-09-10 | 課綱、Ch2導入 | 先介紹課綱，再以student table概談資料庫用途與Ch2；不要求首堂完成整個Week 1閱讀段落 | 依實際授課選用tuples、attributes、domains、schema/instance與識別需求的開頭範例；未完成部分接續，正式keys分類在導入後進行 | 當堂指定範例的辨認、預測、解釋或修正 |
| 2 | 2026-09-17 | Ch2 | primary/candidate/foreign keys、schema diagrams 與核心 relational algebra | 對小型 relations 逐步執行 selection、projection、product、join 與 set operations；比較 key choices | Key map, algebra results, and individual revision |
| 3 | 2026-09-24 | Ch3 | SQL DDL basics；`SELECT`、`FROM`、`WHERE`、expressions、duplicates、patterns 與 ordering | 先預測 course-registration queries，再執行並核對 rows、columns 與 ordering | SQL file and verified query results |
| 4 | 2026-10-01 | Ch3 | `NULL`、three-valued logic、aggregation、`GROUP BY`/`HAVING`、`IN`/`EXISTS` 與 selected subqueries | 修正含 `NULL`、aggregation 或 subquery 錯誤的 SQL；檢查 AI 生成 SQL 的語意與輸出 | SQL verification table and individual revision |
| 5 | 2026-10-08 | Ch4 | explicit joins、left outer join、`ON`/`WHERE`、views、constraints 與 basic transaction statements | 比較 inner/outer join 結果；以 constraint violations 與 rollback/commit 說明資料完整性 | SQL and constraint exercise |
| 6 | 2026-10-15 | Ch2-4 | Written Exam 1；考後依公布標準分析並修正代表性錯誤 | 個人考試；以新資料修改一題錯誤解法 | Exam 1 and correction sheet |
| 7 | 2026-10-22 | Ch5 | window ranking、recursive CTE、row-level audit trigger；stored routines 作概念介紹 | 以 prerequisite graph、ranked scores 與 grade-change audit 示範各功能解決的問題 | Advanced SQL exercise and execution evidence |
| 8 | 2026-10-29 | Ch6 | entities、attributes、relationships、cardinality、participation 與 keys | 從選課案例的 business rules 建立初版 E-R diagram，逐項標示判斷依據 | E-R diagram draft |
| 9 | 2026-11-05 | Ch2-5 review | 教師參加 INFORMS；不安排實體課、考試或新內容 | 非同步概念檢核，重做一題 SQL 並檢查一項Ch2-Ch5核心判斷 | Asynchronous review record |
| 10 | 2026-11-12 | Ch6 | design decisions、redundancy、E-R model 到 relational schema 的 mapping | 檢查 AI 生成 E-R diagram 是否符合 business rules，再完成 schema、keys 與 foreign keys | Revised E-R diagram, schema, and individual revision |
| 11 | 2026-11-19 | Ch7 | anomalies、functional dependencies、attribute closure、lossless decomposition、3NF 與 BCNF | 從含重複資料的 relation 找出 anomalies，以 FD 與 sample rows 比較 decomposition | FD table, decomposition, and individual revision |
| 12 | 2026-11-26 | Ch5-7 | Written Exam 2；考後修正一題 advanced SQL、E-R mapping 或 normalization 題 | 個人考試；使用新的 business rule 或 relation instance 完成修正 | Exam 2 and correction sheet |
| 13 | 2026-12-03 | Ch14 | index 使用時機、B+ tree equality/range lookup、複合與 covering index、query-plan evidence | 對 deterministic order workload 建立 index，比較建立前後的 access path | Index design and query-plan evidence |
| 14 | 2026-12-10 | Ch15-16 | scan/index search、plan access order、result-equivalence check、basic selectivity、catalog statistics與`ANALYZE` | 比較等價query的results與plans，讀取SCAN/SEARCH及statistics，再驗證AI的index建議 | Query-plan interpretation and individual revision |
| 15 | 2026-12-17 | Ch17 | transaction boundaries、ACID、schedules、conflicts、small precedence graphs、recoverability 與 isolation phenomena | 逐步分析 transfer schedules、conflict edges、commit order、dirty read 與 phantom | Transaction and isolation analysis |
| 16 | 2026-12-24 | Ch18-19 | S/X compatibility、grant/wait、wait-for graph與deadlock；log records、WAL及單一簡化redo/undo案例；整合複習 | 判斷lock requests及cycle，依transaction status與log old/new values完成redo/undo，再連結index、plan、transaction與recovery | Concurrency and recovery analysis; review record |
| 17 | 2026-12-31 | - | 校慶補假，不排課 | 無 | None |
| 18 | 2027-01-07 | Ch14-19 | Written Exam 3 / Final Examination；累積應用已教 SQL 與 database design concepts | 個人考試 | Exam 3 |

## 六、評量

| 評量 | 日期 | 比例 | 正式範圍 |
|---|---|---:|---|
| Written Exam 1 | 2026-10-15 | 25% | Ch2-Ch4；以課堂核心內容為限 |
| Written Exam 2 | 2026-11-26 | 25% | Ch5-Ch7；以課堂核心內容為限 |
| Written Exam 3 / Final Examination | 2027-01-07 | 30% | Ch14-Ch19；累積題只應用已教 SQL 與 database design concepts |
| Class Performance | 全學期 | 20% | SQL labs、database design、E-R diagrams、schemas、normalization、query plans、個人回答與修正 |

Class Performance 依完成情形、技術正確性、可驗證證據、理由說明及教師回饋後的
修正評定。小組回答的平均排序不直接計分。只有指定為繳交項目的證據才納入評量，
避免學生為每一個課堂練習製作不必要的額外文件。

三次考試的內部命題比例用來控制教學與評量負荷：

| 考試 | 內容比例 |
|---|---|
| Exam 1 | Ch2 約 35%；Ch3 約 40%；Ch4 約 25% |
| Exam 2 | Ch5 約 25%；Ch6 約 45%；Ch7 約 30% |
| Exam 3 | Ch14 約 20%；Ch15-16 約 20%；Ch17 約 25%；Ch18-19 約 25%；累積應用約 10% |

Exam 3 只要求學生判讀課堂已練習的 index、plan、schedule、lock、deadlock 與 log
案例，不要求完整 B+ tree algorithms、optimizer cost derivations、MVCC algorithms
或 production recovery administration。

## 七、AI 使用與驗證

AI 只在教師指定的活動中使用。正式安排三次：

| 週次 | 任務 | 學生必須提供的驗證 |
|---:|---|---|
| 4 | 檢查 AI 生成 SQL | schema/sample data、實際 query result、錯誤說明與修正版 |
| 10 | 檢查 AI 生成 E-R diagram | business-rule evidence、cardinality、keys、mapping 與修正版 |
| 14 | 檢查 AI 的 index 建議 | workload、index definition、before/after query plan、限制與結論 |

學生必須能說明提交內容，不能把 AI 回答本身當成證據。AI 工具不得用於三次
個人 written examinations；其他活動若允許使用，會在題目中明列。

## 八、行事曆與範圍備註

- 115-1 於 2026-09-07 開始上課，本課 Week 1 為 2026-09-10。
- 教師於 2026-11-01 至 2026-11-07 參加 INFORMS；Week 9 不排實體課、考試
  或新進度。
- Week 17 的 2026-12-31 為校慶補假。
- Week 18 的 2027-01-07 位於校定期末考試週，辦理 Written Exam 3。

官方行事曆來源：

- 國立臺北商業大學教務處行事曆：`https://acad.ntub.edu.tw/p/404-1004-37975.php?Lang=zh-tw`
- 115 學年度行事曆 PDF：`https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf`

## 九、仍待執行的工作

1. 現行GitHub course repository維持private；尚待教師建立第一批公開allow-list、
   決定公開時機，並另建public repository或allow-listed release artifact。
2. 將三次考試的實際題型、allowed resources、版本、答案與評分規準分開保存。
3. 決定課堂匿名展示與完整排序使用的系統，並先測試 30 人、6 組及資料匯出。
4. 由教師審閱English-only逐章教材、課堂核心/延伸標示及學生可見性後再發布。
