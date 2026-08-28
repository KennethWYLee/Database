# 資料庫管理教師審閱前完整檢查

檢查日期：2026-08-27
檢查基準：`main` branch，`b204458 feat: establish database course materials`
遠端基準：檢查開始時`origin/main`與`b204458`一致
結論：教材與SQLite套件已達可供教師有效審閱的狀態；尚未核准為全套student-ready，
也尚未發布。

## 1. 整體結論

- Ch2-Ch7及Ch14-Ch19均有學生教材、可檢查的活動、教師端coverage record及驗證
  程式。所有12個chapter verifier在目前環境重新執行通過。
- 課綱、課程計畫與章節教材在三次考試、評量比例、主要教科書、SQLite環境、出國
  週、補假與期末考日期上相符。
- 所有合理可執行的學生SQL、Python模擬、SQLite activities及圖片來源均已檢查。
  SQLite學生ZIP從新暫存目錄解壓後，10組packaged activities全部通過，兩次建置的
  ZIP位元組一致。
- 未發現答案、教師檔案、未發布考題、評分資料、個資、憑證、快取、預建database
  或未核准來源進入學生套件。學生可見Markdown未發現內部製作分類名稱或分鐘配置。
- 12份學生指南均具備core question、teaching summary、prerequisites、learning
  objectives、examples、prediction、checking、common errors、individual evidence、
  chapter summary及after-class continuation；學生可見文字檔的CJK字元數為0。
- 教師已於同日決定Week 9複習Ch2-Ch5、English-only學生教材、縮減Ch15-Ch16與
  Ch18-Ch19課堂核心、官方英文姓名`WenYi Lee`，以及未來在GitHub選擇性公開。
  決定已套用；全部逐章教材仍待教師內容與語言審閱後才能發布。

## 2. 檢查來源與邊界

### 2.1 課程與行政來源

- 已完整閱讀工作區及課程治理文件、`PROJECT.md`、`README.md`、`COURSE_PLAN.md`、
  `1151_database_management_revised_syllabus.md`、章節教材設計prompt、working
  materials說明、整合報告、全部選定章節檔案及SQLite學生套件maintained source。
- 已核對國立臺北商業大學115學年度行事曆。115-1於2026-09-07開始上課，日間學制
  期中考週為2026-11-02至11-06，2026-12-31為校慶補假，期末考週為2027-01-04
  至01-08；本課星期四日期及2027-01-07的Exam 3均落在正確位置。
- 教師2026-11-01至11-07參加INFORMS是本課既定決定；Week 9不安排實體課、考試
  或新進度。

### 2.2 教科書與官方投影片

- 本機私人PDF的書名、作者與版本已確認為Silberschatz, Korth, and Sudarshan,
  *Database System Concepts*, 7th Edition。該PDF只用於教師端來源查核，未加入Git
  或學生套件。
- 已讀取並查核正式範圍的完整教科書章節。印刷頁碼範圍為：Ch2 37-58、Ch3
  65-114、Ch4 125-174、Ch5 183-232、Ch6 241-294、Ch7 303-352、Ch14
  623-678、Ch15 689-735、Ch16 743-788、Ch17 799-829、Ch18 835-896、
  Ch19 907-950。
- 已讀取12份本地官方投影片。PDF頁數為：Ch2 29、Ch3 62、Ch4 58、Ch5 47、
  Ch6 83、Ch7 93、Ch14 81、Ch15 59、Ch16 85、Ch17 40、Ch18 90、Ch19
  101。各章coverage record原先把內部slide編號誤當PDF頁碼的地方已修正。
- Ch5本地投影片在recursive query後結束，沒有完整涵蓋ranking/window functions；
  目前該部分以教科書Ch5為權威來源。這是來源組合的限制，不是未查核內容。
- 自動字串比對對連字號、單複數及章節用語差異較敏感；未以自動比對結果代替章節
  閱讀。沒有發現教材把不屬於該章的主題誤稱為教科書正式內容。

### 2.3 維護來源與生成物

- 章節中的`.md`、`.sql`、`.py`、`.json`、`.svg`及教師端verification files是
  maintained source；PNG及SQLite學生ZIP是generated artifacts。
- `working_materials/student_sqlite_package/package_files.json`是學生套件唯一
  allow-list；`build_package.py`依該清單建立資料夾、manifest及ZIP。
- 本次只修改maintained source後重新產生受影響的PNG與ZIP。未修改私人歷史教材、
  考題、答案、被`.gitignore`排除的來源，也未建立remote、commit、push或改寫歷史。

## 3. 課綱、計畫與教材一致性

### 3.1 已一致

| 項目 | 結果 |
|---|---|
| 課程與對象 | 四技資訊管理系二年級必修、3學分、星期四第5-7節一致 |
| 教科書與軟體 | *Database System Concepts*第7版及SQLite 3一致；驗證版本SQLite 3.45.3 |
| 正式章節 | Ch2-Ch7及selected Ch14-Ch19一致；Ch8-Ch9不列入正式進度 |
| Exam 1 | 2026-10-15，Ch2-Ch4，25% |
| Exam 2 | 2026-11-26，selected Ch5-Ch7，25% |
| Exam 3 | 2027-01-07，selected Ch14-Ch19及已教過的累積應用，30% |
| Class Performance | 20%；SQL labs、設計、E-R、normalization、plans、個人回答與修正 |
| Week 9 | 2026-11-05不安排實體課、考試或新進度 |
| Week 17 | 2026-12-31校慶補假，不排課 |
| 學生環境 | 不要求server DBMS；SQLite無法呈現的行為以概念、schedule、log或模擬處理 |

### 3.2 教師決定及套用結果

1. Week 9統一為Ch2-Ch5非同步複習；課綱、`COURSE_PLAN.md`與`PROJECT.md`已一致。
2. 所有正式學生教材採English-only prose；12份`student_guide.md`已完成英文改寫，
   並保留標準database terminology、SQL、公式、檔名、預測、判讀及學習證據。
3. Ch15-Ch16核心縮減為plan access、result equivalence、basic selectivity、statistics、
   `ANALYZE`及plan evidence；完整rewrites、join algorithms、skew細節與optimizer
   internals改為延伸。
4. Ch18-Ch19核心縮減為S/X compatibility、grant/wait、wait-for graph、deadlock、
   log records、WAL及單一簡化redo/undo；2PL變體、MVCC、checkpoint與backup細節
   改為延伸。
5. 任課教師官方英文姓名為`WenYi Lee`；現行GitHub course repository為private。
   未來選擇性公開需使用另一個public repository或allow-listed release artifact；
   本次沒有公開、上傳或push。

## 4. 逐章結果

下表的「通過」表示目前版本沒有發現阻擋教師審閱的客觀錯誤，不代表教師已核准
教學範圍、難度或語言。

| 章節 | 已通過及本次修正 | 待教師審閱或決定 |
|---|---|---|
| Ch2 Relational Model | 概念、keys、schema、algebra範例、預測、操作、判讀、錯誤、練習、證據與前後連結均存在；SQL/algebra verifier通過；coverage source scope已更正 | 練習的學生版自我檢核提示較少；是否增加提示屬教學選擇 |
| Ch3 Introduction to SQL | DDL、queries、NULL、aggregation、subqueries、DML與錯誤案例通過；英文改寫完成；verifier通過 | 同Ch2，學生自我檢核密度及英文技術表述待教師審閱 |
| Ch4 Intermediate SQL | joins、outer-join反例、views、constraints、transaction statements通過；移除學生版本機內部路徑並完成英文改寫；verifier通過 | 無新增客觀缺陷；仍需教師英文內容審閱 |
| Ch5 Advanced SQL | ranking、recursive CTE、audit trigger與stored-routine用途均有對應範例及活動；verifier通過 | 單週同時涵蓋多種SQL能力可能偏重；本地投影片不含ranking/window，來源以教科書補足 |
| Ch6 E-R Design | concepts、business rules、mapping及反例通過；補上先備知識；SVG/PNG與schema驗證通過 | 兩週安排合理但仍需確認學生需交付的圖形工具與格式 |
| Ch7 Normalization | anomalies、FD、closure、lossless decomposition、3NF/BCNF通過；補上明確核心問題；verifier通過 | 一週內完成closure、lossless與3NF/BCNF判斷的負荷需教師確認 |
| Ch14 Indexing | index use、B+ tree lookup/range、column order、covering index及plan evidence通過；核心與延伸範圍及來源定位已修正；PNG重建並視覺檢查 | 不教授完整B+ tree insertion/deletion的既定範圍是否符合Exam 3深度需確認 |
| Ch15 Query Processing | 英文教材保留processing stages、SCAN/SEARCH、join access與plan evidence；materialization、pipelining及完整join algorithms明列延伸 | 與Ch16共一週，仍需教師確認英文範例與實際課堂節奏 |
| Ch16 Query Optimization | 英文教材核心已縮減為equivalence、basic selectivity、statistics、`ANALYZE`與plan evidence；rewrites、outer-join反例與skew細節改為延伸；補上`EXCEPT`無法普遍驗證duplicate multiplicity的限制 | Ch15-Ch16合計由604行降為514行；仍需教師最終審閱 |
| Ch17 Transactions | ACID、states、schedules、conflicts、precedence graph、recoverability及isolation phenomena通過；verifier及schedule analyzer通過 | server-side isolation未在實際server DBMS執行；只能視為概念與模擬證據 |
| Ch18 Concurrency Control | 英文教材核心已縮減為S/X compatibility、grant/wait、wait-for graph與deadlock；2PL變體、MVCC及snapshot isolation改為延伸 | 模型不是實際DBMS行為；需教師確認延伸內容是否保留在發布版 |
| Ch19 Recovery | 英文教材核心已縮減為failure distinction、log old/new、WAL及單一redo/undo案例；checkpoint與backup細節改為延伸 | Ch18-Ch19合計由850行降為515行；未執行真實crash/restore，仍需教師最終審閱 |

## 5. 程式、圖片與套件驗證

### 5.1 環境

| 工具 | 版本 |
|---|---|
| Python | 3.12.9 |
| Python `sqlite3` linked SQLite | 3.45.3 |
| pypdf | 6.9.1 |
| Poppler `pdftotext` | 25.02.0 |
| Git | 2.54.0.windows.1 |

### 5.2 實際執行

- 逐一執行`python working_materials/chapters/<chapter>/instructor/verify_chXX.py`，
  `<chapter>`涵蓋Ch2-Ch7及Ch14-Ch19。12個verifier全部通過。
- 驗證內容包括relation/schema/key/algebra、SQL與NULL、joins/views/constraints/
  transactions、advanced SQL、E-R mapping、normalization、index/query plans、query
  processing/optimization、transaction schedules、locks/deadlocks/MVCC teaching model、
  WAL及recovery simulation。
- 對全部21個Python檔執行compile check，全部通過；7個JSON檔可解析；4個SVG檔
  可由XML parser讀取。
- 重新產生並檢視Ch6 E-R及Ch14 B+ tree PNG。文字、關係、cardinality、節點與連線
  可辨識，未見裁切或重疊。Ch14 PNG連續兩次產生相同內容。
- 執行`python working_materials/student_sqlite_package/build_package.py --verify`，
  並再次獨立建置作reproducibility比較。每次都從新暫存目錄解壓，21個allow-listed
  files及Ch2-Ch7、Ch14-Ch17共10組activities全部通過。
- packaged SQL已實際涵蓋foreign keys、constraint violations、NULL、transactions、
  query plans及預期錯誤。Ch17 schedule analyzer亦通過。

### 5.3 套件完整性

- 原始audit版本ZIP SHA-256：`52f8749d9a7b2a72c16c83488c930e52c1a85b68430144da390692ea7730e577`
- 2026-08-28為同時支援學生版`chapters/`與原套件`materials/`更新runner後，重建
  ZIP SHA-256：`15f6847ad7163db552536231427010f68ef1731606726ba05bf298ce40001e05`；
  manifest及10組packaged activities重新驗證通過。
- manifest逐檔hash與解壓檔案相符；兩次完整建置的ZIP hash相同。
- ZIP共21個檔案；blocked entry count為0。
- 未包含`instructor`、answer/solution、assessment、`__pycache__`、`.pyc`、預建`.db`、
  私人教材或未在`package_files.json`核准的來源。

### 5.4 未執行項目

- 未使用PostgreSQL、MySQL、SQL Server或其他server DBMS執行stored routines、
  isolation level、deadlock inspection、MVCC、snapshot isolation或crash recovery。
  目前證據只支持教材中的概念、SQLite行為、schedule/log分析及Python teaching model。
- 未測試實際GitHub公開下載流程或30人6組匿名排序平台；公開allow-list及平台尚未建立。
- 未審閱或建立三次考試的正式題目、答案、允許資源、AI規則與rubric，因這些屬教師
  評量政策決定。

## 6. 學生版安全、格式與發布檢查

| 檢查 | 結果 |
|---|---|
| UTF-8與replacement character | 通過；未發現解碼錯誤或U+FFFD |
| Markdown fences與本地連結 | 通過；未發現不平衡code fence或broken local link |
| 英文限定 | 課綱、12份學生指南及解壓套件共32個學生可見文字檔，CJK字元數為0 |
| 標題、表格、閱讀順序 | 12/12指南具備指定的教學結構；55個Markdown未發現阻擋性結構錯誤 |
| 分鐘或時間配置 | 未發現課堂分鐘配置 |
| 內部製作分類名稱 | 學生可見檔案未發現 |
| 教師備註、答案、考題、評分與個資 | 學生教材及ZIP未發現 |
| 憑證或secret pattern | 未發現 |
| 本機內部路徑 | Ch4一處已改成學生套件相對操作方式；複查未再發現 |
| Python危險執行模式 | 未發現`eval`、`exec`或`shell=True`；package runner使用list arguments |
| 教科書、改寫、執行與推論 | coverage record已區分來源範圍、教學改寫、執行證據與限制 |

## 7. 已修改檔案與理由

### 7.1 治理及報告

- `.gitignore`：只allow-list本報告，不改變其他private-by-default規則。
- `README.md`、`PROJECT.md`、`COURSE_PLAN.md`、`working_materials/README.md`及
  `course_material_integration_report.md`：更新實際repository狀態、audit入口、學生
  套件hash、審閱狀態及一致的主要下一步。
- 本報告：集中保存檢查版本、證據、限制、修正與教師待決事項。

### 7.2 章節教材及驗證紀錄

- Ch2-Ch7及Ch14-Ch19全部學生教材：改寫為English-only prose，保留技術範圍、
  teaching examples、prediction、interpretation、practice及individual evidence。
- Ch15-Ch16與Ch18-Ch19學生教材：依教師決定縮減課堂核心並把移出內容明列延伸。
- Ch4學生教材：移除指向repository內部工作區的本機路徑，改為學生套件操作方式。
- Ch2-Ch7及Ch14-Ch19全部coverage record：更正來源頁數、失效slide locators、核心
  與延伸範圍，以及過期的套件/介面狀態。這些修改只校正證據與既有決定，未擴張
  正式授課範圍。
- Ch14 `bplus_tree_example.png`及SQLite學生ZIP：由維護來源重新產生。

## 8. 仍存在的限制與風險

1. English-only學生教材已完成系統化改寫，但尚未由教師逐份核准技術表述與語氣。
2. Ch15-Ch16及Ch18-Ch19已大幅縮減，實際課堂負荷仍需第一次授課觀察。
3. Ch2-Ch3的學生版自我檢核提示少於後續章節；增加提示時必須避免答案洩漏。
4. Ch17-Ch19只完成SQLite可執行部分與teaching models，沒有真實server DBMS或crash
   recovery證據。
5. 三次考試藍圖、允許資源、AI規則、rubric及版本尚未建立。
6. 課堂排序平台、GitHub公開allow-list、獨立公開位置及實際下載後的ZIP複驗尚未完成。

## 9. 教師優先閱讀位置

1. Ch15-Ch16及Ch18-Ch19英文學生教材：確認縮減後的核心、延伸與Exam 3深度。
2. Ch2、Ch3及Ch17英文學生教材：抽查SQL、transaction及assessment-related術語。
3. `COURSE_PLAN.md`第六至第八節：確認每週範圍、三次考試coverage及Class
   Performance規則。
4. `1151_database_management_revised_syllabus.md`的Weekly Schedule、Assessment
   and Grading及Schedule Notes：確認可對學生公布的英文表述。
5. `PROJECT.md`的Repository與發布狀態：建立第一批GitHub公開allow-list及獨立公開位置。

## 10. 主要下一步

主要下一步是教師優先審閱縮減後的Ch15-Ch16與Ch18-Ch19英文學生教材，再抽查
Ch2、Ch3及Ch17。這些檔案直接影響Exam 3與英文技術表述，應先於GitHub公開。

預期成果是教師留下具體修正或明確核准。完成條件是核心/延伸界線、英文術語、
examples及evidence instructions均獲確認，並建立第一批GitHub公開allow-list及獨立
公開位置。

## 11. Git與發布狀態

- 本次未commit、未push、未建立remote、未改寫歷史。
- 工作樹保留本次客觀修正、重新產生的PNG/ZIP及本報告，供教師審閱。
- 全套逐章教材目前狀態為「source-checked、tested、適合教師審閱」，不是
  「教師已核准、student-ready或published」。
