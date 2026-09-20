# 資料庫管理 - Project Context

本檔只記錄資料庫管理課程的事實、固定決策、權威文件、核准用語、限制與
未解問題。通用工作規則見 `AGENTS.md`；`CLAUDE.md` 是其位元一致鏡像。

- 最後更新日期：2026-09-20

## 最新範圍與授課順序

2026-09-20 教師確認「依舊只公開到ch3」。現行main只公開Ch1-3教材、
Ch3圖解與Ch3解答；Ch4教材與解答PDF從最新公開版本、README與allow-list移除。
課綱仍保留全學期章節安排，授課範圍與評量不變。所有本機原檔保留。
15份含中文解答的教師備課PDF與私人分支不推送；此次公開提交從origin/main
獨立建立，不包含任何私人備課commit。未改寫歷史，過去已發布的Ch4仍可在
舊commit找到。以下Ch4發布紀錄屬歷史，不代表目前允許發布。
舊course-materials與student-preview分支最新內容亦對齊同一Ch1-3公開版本；
使用保留既有歷史的提交，不force-push。Notebook checkout固定LF，避免Windows
換行轉換讓PDF來源雜湊誤報不一致；Ch1-3教材與課綱內容完全不變。

2026-09-17 教師進一步授權Ch4教材commit/push。本次發布範圍為
`Intro DB/ch04_redesigned.pdf`、首頁入口、公開allow-list、課程檔案清單及相應測試。
PDF內容維持已驗證的43頁，SHA256為
e593c6a054ae9870eb88949a6aad939ef5d5390e9b4a516035ac41b78f4d15f5。
維護來源、QA、課本及舊Ch4 notebook仍保持本機ignored，不隨本次提交公開。
下段的「未授權發布」狀態已由本次授權取代；實際同步結果以Git紀錄為準。
發布檢查修正獨立PDF被誤認為notebook匯出的既有問題，29項課程測試通過；
PDF統一以Git binary處理，不更改PDF內容。

2026-09-17 教師要求依Ch3目前做法完成Ch4教學。新增本機審閱版
`Intro DB/ch04_redesigned.pdf`：43頁英文、27幅向量圖、55張小表格，涵蓋核准的
4.1-4.7；以背景、規則、圖、資料及錯／對比較連續說明。維護來源及逐節來源對照在
`maintenance/course_repository/ch04_redesign/`，QA在對應output/ch04_redesign。
Ch3各版本、notebook與既有Ch4解答均未改；課綱、配分及週次未改。本次沒有新增
notebook或SQL作業；舊under_revision/ch04.ipynb不是現用課本的EER教材。
43頁建置、資料與圖形限制檢查、文字邊界／重疊檢查及Poppler渲染通過，已看全部
頁面總覽與複雜圖放大。大學案例明確縮小至教學／研究角色與三個關係，並非完整
複製Figure 4.9；UML圖採OMG 2.5.1空心三角與明示限制，課本差異已標示。
教材尚待教師審閱，不能宣稱已經課堂驗證。新PDF、來源與QA維持ignored，未更動
公開allow-list，未commit/push。主要下一步改為審閱14-20頁的shared subclass與
category比較；原因是本次已完成Ch4客觀製作檢查，現在需確認BOTH與EITHER的圖例
能清楚講解。完成條件：能從資料解釋P1為何不能當assistant，以及partial category
為何允許未選入OWNER的P2。下方製作Ch4前的建議保留為歷史紀錄。

2026-09-17 教師要求將新版Ch3 PDF移到課程資料夾。目前正式路徑為
Intro DB/ch03_redesigned.pdf，與原ch03.pdf並列；README、.gitignore、PDF產生程式
及課程建置檔案清單已同步，舊output/pdf路徑不保留第二份現行檔。
36項教材檢查通過；與09062e6的PDF逐頁像素比對，60頁全部相同，教材內容未變。
重建只因來源路徑修改而更新PDF來源雜湊metadata。新版SHA256：
58d74191a4a4ccf47e5b8dd053cbc7ebc152bf7932db0dd703334655935dc7ae。
路徑移動、README連結及建置清單已驗證；本次尚未commit/push。
以下舊路徑及舊雜湊均為歷史紀錄，不代表目前入口。

2026-09-17 教師同意針對重複內容修正並commit/push。本次只改60頁版的32、36、58頁：
32頁保留圖書館正確模型，加四個編號指出weak COPY、MAKES人數、LOAN必要參與及
日期位置；36頁只解讀三筆批准，不提前回答37頁的錯誤推論；58頁只保留畫圖、
改錯、解釋三種作答方式，不重講52頁TEACHES答案。必要的錯／對圖及就地資料
對照仍保留，因此不宣稱所有圖表或觀念只出現一次。60頁、7,046字，字級不變。
36項檢查通過，三頁Poppler渲染已檢視；逐頁像素比較確認相較bb9fb24只變動
32、36、58頁。原ch03.pdf與notebook不變。新版SHA256：
27a4b48d0deae456167904782d00879507c9dc8def5a0d02affac9bee3c42863。
維護來源及檢查仍在既有ignored maintenance目錄，本次不強制加入Git；公開提交
範圍為本檔及output/pdf/ch03_redesigned.pdf。以下較舊雜湊與檢查紀錄為歷史版本。

2026-09-17 教師要求重新編排、減量及聚焦，並明確保留圖書館案例。
目前ch03_redesigned.pdf為60頁，取代以下93頁版本的現行狀態；歷次紀錄保留。
順序：1–11實體與屬性、12–21關係與限制、22–26weak entity、27–32圖書館、
33–38三元關係、39–57UNIVERSITY、58–60總結。圖書館接續weak entity，依序呈現
背景需求、COPY／LOAN資料、完整ERD、錯圖、四項修正及修正後總圖。
標題改為明確概念與案例名称，每頁加單元標示；弱實體先固定COURSE／SECTION，
再用ORDER_ITEM比較同三筆資料。33頁移出課堂PDF，但93頁原稿及全部來源保留；
移出同名教師、巢狀備註、多owner面試、CONTACT深化與重複表格／練習等。
新增classroom.py維護選頁、順序、標題及必要銜接；不得再宣稱刪減後包含所有
先前延伸概念。34項檢查通過；60頁render、五張總覽及23、25、28頁放大檢視。
正文共7,093字，最多157字／頁，未縮字級；原ch03.pdf及notebook不變。
PDF SHA256：e65c7bab2325cd6d6a0abeeebfd085bbca3d5edca1035aa9308a24920d545b1d。
詳細範圍及限制見maintenance/course_repository/ch03_redesign/classroom_reduction_review.md。
本次未commit/push，未更改課綱或評量政策。下一步先連讀22–32頁，確認弱實體
到圖書館案例的銜接清楚，能用資料指出owner、partial key及各項錯圖的修正理由。

2026-09-17 教師要求ORDER_ITEM錯圖／修正圖各有獨立資料表，並延伸至重點entity。
新增15頁表格對照，現93頁；原78頁正文與圖形像素不變，僅頁碼順延。ORDER_ITEM
現32頁ERD、33頁表格；同三筆資料比較ItemID單獨識別與OrderId + ItemID。
保留ItemID命名，不因截圖舊LineNo而改回；owner欄表示關係中的識別參照，不表示
一律新增ER屬性或開始SQL mapping。Wrong指錯誤key／屬性位置／限制，不把合法
重複值說成錯誤資料。Grade、StartDate及contact verification分開標示entity與
relationship資料；其餘新增頁涵蓋STUDENT、ROOM、SECTION、CARD、ITEM_NOTE、
INTERVIEW、CONTACT、INSTRUCTOR、COPY、LOAN。既有UNIVERSITY各entity表保留。
54項檢查通過；93頁render、八張總覽及23、33、41頁放大檢視；原PDF與notebook
雜湊不變。11,337字，最多160字／頁，未縮字級。PDF SHA256：
3653394e12dc4896cd486311c99035e6b86df9bd3707087a56ce3a2921ad8272。
maintained source新增entity_records.py；逐項紀錄、頁碼及來源限制見
maintenance/course_repository/ch03_redesign/entity_records_review.md。
未commit/push。下一步先連讀32–33頁，能用同三筆明細說明key主張錯在哪，以及
owner如何區分兩個ItemID 1；不更動課綱、考試政策或新增必交練習。

2026-09-17 教師指出INTERVIEW等範例背景不清，要求全份檢查。已讀完整78頁，
修正39頁，保留39頁；不增加頁數或縮小字級。新增情境先說用途、人物與編號，
改規則先明示：任職1:N/M:N、卡片數量、不同校園資料集及各項獨立變體。
第29頁先講商品包裝備註及每項內編號，三筆資料對照weak owner；第30頁先講
職涯中心記錄面試、學生／公司及每組內VisitNo，再看表與ERD。第38頁APPROVES
現已改成指定批准的逐列比對，不再使用State A/B。此紀錄取代下方「尚未實作」狀態。
50項檢查通過；78頁render、七張總覽及28–30、38頁放大檢視。原PDF與notebook
雜湊不變，未commit/push。全份仍78頁、9,554字（抽取英文空白分詞），最多160字／頁。
PDF SHA256：ebfb5396f84d4df1b636c85c2a433079458e23a273004f360b88f36c684480ff。
完整逐頁紀錄見maintenance/course_repository/ch03_redesign/context_review.md。
本次不是全書逐句來源查核，也未做學生理解實測。下一步先連讀29–30頁，確認能
說清楚記錄用途、各編號意思與完整識別組合，不需自行補背景；既有進階內容省略
及1:1屬性移置未涵蓋仍保留，30頁不再延伸無partial key的另一種變體。

2026-09-17 教師核准將訂單明細範例欄位LineNo改名為ItemID（大小寫固定）。
適用於ch03_redesigned第27–29頁的表格、ERD、說明及後續同一案例；ItemID仍為
同一訂單內唯一的partial key，不是全域識別碼；完整識別為OrderId + ItemID。
原版PDF、notebook及歷史紀錄不回溯改寫。本次未commit/push。

2026-09-17 UNIVERSITY依教師新指示改為圖書館案例的需求／錯圖／修正形式。
現78頁：41背景；42–43需求R1–R9；44完整錯誤關係圖；45–53原資料；54–59六組
錯圖與修正（SecId、TEACHES、Grade、至少五人、CHAIR可選角色、SECS多班別）；
60以教科書Figure 3.20重繪關係正解，61保留排課反例。正解沿用課本全部九種關係、
key與min-max；為可讀性省略多數非key實體屬性橢圓，但完整屬性值保留於資料表。
HAS以圖的(0,1)為準，正文差異仍明示。原三張局部說明保留來源但不再輸出。
47項檢查通過；78頁render，檢視需求、六組比較及總圖；67個保留頁正文像素不變。
原ch03.pdf與notebook不變；本次未commit/push。APPROVES的先前討論尚未在本次
UNIVERSITY修改中實作。下一步先檢閱54–59頁，能用每張表解釋錯誤及修正符號。
完整紀錄與新版hash見maintenance/course_repository/ch03_redesign/README.md。

2026-09-17 教師要求UNIVERSITY先講背景、完整ERD及每張表的範例資料，再談重點。
新版72頁：41背景；42橫式完整關係圖（六種實體、九種關係、全部key及兩個關係
屬性，其餘實體屬性於資料表呈現）；43–47全部實體欄位資料；48–51全部關係資料；
52–55保留辨識班別、組織職務、人數限制、排課衝突四個討論。新增university.py
維護同一組虛構資料；原67頁中的42、45、46、48、49頁移出課堂PDF，核心說明
併入資料頁，原稿仍保留於OPTIONAL_PAGES。新增10頁、移除5頁，未增加必交作業。
重讀教科書3.10（完整書PDF123–125／印刷92–94及圖3.20）；HAS依圖的(0,1)，
學生U2可尚無系所，明示正文要求一系所與圖不同。排課反例改為新增Q103–Q105，
不得暗中更改Q101、Q102；每個提案分別判斷。所有身份、聯繫資料及成績均為虛構。
44項檢查通過（含4項保留進階來源檢查），72頁render；檢視41–60頁總覽及重點
放大頁；59個保留頁正文像素不變。原ch03.pdf和notebook不變，未commit/push。
PDF SHA256：7c034722452c18dcff72cd26895b458a8486545b68f1919a5eca18d14c763bf1。
依本次新回饋，下一步先讀41–55頁：能以同一組資料將Q101連到DB101、D1、I1及
五位學生，再解釋四項重點。尚未做實際投影或學生理解測試；詳細紀錄見
maintenance/course_repository/ch03_redesign/README.md。以下為歷次版本紀錄。

2026-09-17 教師要求刪除較不重要或使APPROVES主線複雜的slides。課堂版由74縮為
67頁，移除舊39–42、44–45、69頁：三元weak／人工ID替代、特殊binary重建、
eligibility、三元總筆數限制、兩限制同時檢查、重複三元讀圖。來源保留為
OPTIONAL_PAGES且備份完整74頁，不再輸出於課堂PDF；不得再宣稱這些概念已涵蓋。
APPROVES現34–39頁依序為背景、完整圖、參與者、三筆紀錄、pair不足、三元1。
一般weak entity、binary min-max、畫ERD與改錯案例仍保留。課末摘要、selected來源
範圍與目前觀念頁碼已同步；原ch03.pdf和notebook不變，未更改正式評量政策。
40項檢查通過（36項目前成品／通用、4項保留進階來源），67頁render並檢視變動
銜接頁；65個保留頁正文像素不變。未commit/push。PDF SHA256：
0e03a54205bcee53baf464afb6198ac219df7e6480b361985d627783c845ee9d。
下一步先以34–39頁確認同一組資料能講清楚三元關係及1，不再同時切換多種進階規則。
刪減清單與檢查紀錄見maintenance/course_repository/ch03_redesign/README.md。

2026-09-17 教師要求APPROVES先說背景、完整ERD與對應資料，再逐步討論細節。
新版PDF現74頁：34背景、35完整APPROVES案例ERD（含三個key及Name/Title）、
36學生／教師／課程資料、37原三筆批准紀錄及逐列讀法；38–45接續討論。
案例是教師批准學生修讀課程的原創教學情境，不代表校規；批准不等於選課或成績。
表示法變化保留原資料，新增限制的案例明示資料重設，後續限制檢查明示回到state A。
40項檢查通過、74頁render，重點頁檢視；64個原頁正文像素不變，七個原頁修改、
新增三頁。原ch03.pdf及notebook仍保留，未commit/push；目前來源範圍與1:1屬性移置
未明示的限制不變。PDF SHA256：5a6007a80558a67bb0739aff8f1aa9698836060e882fe7cbec5bd8ed966d4e33。
下一步依本次回饋改為先讀34–37頁，能將每筆批准讀成完整句子並對應ERD，再討論38頁。
詳見maintenance/course_repository/ch03_redesign/README.md最新紀錄。

2026-09-17 教師回報抽象結論不利課堂討論，要求全份改成具體問題、錯誤ERD或
相似圖比較。已檢視71頁、調整55頁，未增加頁數或縮小字級；第27頁說明LineNo
是訂單內明細編號而非產線，使用同一表格比較錯誤完整key與正確partial key圖。
第28–30頁以卡片、兩筆備註、面試查找銜接；其他頁把問題連到具體資料和符號。
37項檢查通過，71頁重新render並檢視總覽及八個放大頁；原ch03.pdf和notebook
保持不變，未commit/push。逐頁紀錄見maintenance/course_repository/ch03_redesign/
discussion_review.md；本次不是全書來源重查，1:1屬性移置的既有未涵蓋項仍保留。
新版PDF SHA256：bd3cf347718f1f41ee76746379b55dbd74267ffd304146aa60421593498fcf1c。
新課堂回饋使下一步改為連讀27–30頁：能以兩筆明細說明錯誤key與修正符號，
再區分有全域ID的卡片和需要多層owner的備註。未增加必交練習或更動評量政策。

2026-09-17 教師要求全份範例檢視：已讀新版PDF全部71頁，補強21頁且未增加頁數。
第23、25頁直接放入同一組三筆CourseCode／SectionNo資料；第24頁區分合法的
跨課程重複編號、錯誤的完整key主張，以及同課程不同班別重複編號的非法新增。
後續案例優先採「具體資料、判斷、理由、對應ER符號」，保留相同資料以比較觀點。
新增同名學生、任職限制、三元辨識、跨學期與借閱讀圖等範例；33項檢查通過，
71頁重新render、檢視六份總覽與重點頁。原ch03.pdf及notebook保持不變，未commit/push。
逐頁結果見maintenance/course_repository/ch03_redesign/example_review.md；此為教材
範例檢查，不宣稱重新逐句查完教科書。下一步先以23–25頁確認能從資料說明
合法重複、錯誤判斷、非法新增與ER符號，再繼續閱讀後續案例。

2026-09-17 教師確認圖解方向：後續ERD範例優先保留相同實體、版面與既有資料，
逐次改變一項限制或屬性位置，再用具體資料指出意義的差別；區分兩種合法畫法
與不符合需求的錯誤畫法，不只重複相似圖片。本次先實作StartDate的接續比較，
不宣稱其餘全部案例已重寫。

2026-09-17 在第21頁1:N StartDate後新增第22頁M:N比較：保留原兩筆任職資料，
加入I1／D2及不同日期，用兩張ERD比較EMPLOYS屬性與不適用的INSTRUCTOR屬性。
依課本3.4.4核對；30項檢查通過，71頁均重新render，檢視新增頁及相鄰頁。
原70頁正文像素保持不變，只有頁尾頁碼更新；weak entity現從第23頁開始。
已同步觀念對照頁碼；原ch03.pdf及notebook不变。本次未commit/push。
下一步比較21–22頁，確認能用I1與D1的兩個日期說明為何M:N需要任職配對。

2026-09-17 Ch3弱實體段落銜接：第22–25頁以同一組三個班別，依序說明課程
代碼與班別編號的差異、owner加partial key的辨識、ER符號及新增全域ID的反例。
第26–30頁補上與主例子的連接，不改案例規則或教學範圍。已重查課本3.5、
檢視九頁並通過29項檢查；仍70頁，原ch03.pdf及notebook不變。累積相對已發布
版僅第6、14、17、19、21–30頁改變。未commit/push。下一步先連續閱讀22–25頁，
確認同一班別的辨認方式與ER符號能連貫說明，再讀延伸例子。

2026-09-17 Ch3第21頁重寫：依教師要求，以兩張ERD及I1／I2的日期表對照
StartDate放在EMPLOYS或INSTRUCTOR，限定每位教師恰有一個現職系所；說明
經過時間可由日期計算。移除成績、系主任與任職歷史岔題；1:1屬性移置規則
不再於此PDF明示，已如實更新觀念對照。28項檢查通過並檢視第21頁，仍70頁；
累積修改僅第6、14、17、19、21頁，原ch03.pdf及notebook不變。未commit/push。

2026-09-17 Ch3第19頁釐清：依教師註解，新增英文表格對照mentor／mentee的
參與次數與可連結人數，明示(min,max)不能套用先前M:N的對側讀法，並用
S101指導S102及S103說明。27項檢查通過並檢視該頁，仍70頁；累積修改僅
第6、14、17、19頁，其餘與已發布版本像素一致。本次未commit/push。

2026-09-17 Ch3第17頁補充：依教師要求，以英文表格解釋partial／單線允許
教師不授課、total／雙線要求每班有教師；說明partial不要求一定有人未授課，
並區分雙線的最低參與要求與1的最高人數限制。26項檢查通過並檢視該頁；
相較已發布版本僅第6、14、17頁改變，仍70頁。本次未commit/push。

2026-09-17 Ch3第14頁補充：在STUDENT／ENROLLS_IN／SECTION圖下新增兩句英文，
說明一位學生可選幾個section看N、一個section可有幾位學生看M。
25項檢查通過，已檢視第14頁；相較GitHub版本僅第6、14頁像素改變，仍70頁。
前次第6頁簡化保留，本次未commit/push。

2026-09-17 Ch3第6頁簡化：依教師要求移除退選與狀態比較，只保留兩張表格：
S101的兩筆選課紀錄，以及Student／EnrollmentCount的單列S101／2。
維護來源重建後仍為70頁，24項檢查通過，像素比對僅第6頁改變；原ch03.pdf及
notebook不變。本次只更新本機，未commit/push，GitHub仍為下方已發布版本。

2026-09-17 Ch3新版PDF發布授權：教師要求commit and push，並明確同意
ch03_redesigned.pdf加入Git。本次僅新增公開output/pdf/ch03_redesigned.pdf，
以精確路徑加入.gitignore例外並在README提供入口；原ch03.pdf及notebook不變。
以.gitattributes將此PDF明確標為binary，避免文字換行轉換並保留原始位元。
發布沿用已驗證70頁成品，SHA256為
`b54e5d862a921a15d2f7145e48c8e9d89544359f2c8f081de9502b33e1907bc7`。
維護來源、詳細查核、48頁備份與其他output仍留本機，不擴大其公開範圍。
本次授權取代下方新版PDF尚未授權發布的歷史狀態；不代表notebook已同步。
提交前fetch確認HEAD與origin/main一致，重新執行23項檢查；發布不重建或改寫PDF。
主要下一步仍為依序審閱第53-59頁借閱案例及四類錯誤，確認課堂講解是否順暢。

2026-09-16 Ch3觀念查核與整合案例：教師確認圖表式方向，要求先核對課本ER觀念，
再支援三種預計考試方向：依描述畫ERD、依描述修正錯誤ERD、依ERD解釋關係。
新版課堂PDF現70頁，58組向量圖、67個表格；補強8頁觀念及14頁案例，不改配分、
週次或必交作業。範圍仍為3.1-3.7、3.9.1-3.9.2、3.10；3.8 UML與Ch4 EER分開。
已建立逐項來源與頁碼對照，不宣稱整本書或所有習題逐句查核；正式集合符號
在本份圖解教材中保留概念說明，不以完整數學推導取代圖解。
原57頁Intro DB/ch03.pdf及notebook不變，先前48頁重設草稿另行備份。
23項檢查通過，70頁均已render檢視；修正連線穿過無關學生框及比率標籤貼線。
新來源、查核與PDF仍依既有ignore僅留本機；本次未stage、commit或push。
下一步優先看第53-59頁借閱案例，確認能從R1-R5逐項畫出完整ERD並解釋四類錯誤，
再決定是否同步notebook及發布。這項新考試方向要求取代下方只看弱實體的建議。
詳見[觀念對照](maintenance/course_repository/ch03_redesign/concept_coverage.md)與
[重設紀錄](maintenance/course_repository/ch03_redesign/README.md)。

2026-09-16 Ch3課堂版重新設計：教師回報文字過多、重點不明，指定參考IoT的
Week2_main_layout_sample.pdf並先保留舊版。原Intro DB/ch03.pdf與notebook均未
覆寫，另備份原PDF；新版在output/pdf/ch03_redesigned.pdf，目前48頁，英文重點、
向量ER圖與小表格，每頁收束一個結論。原教學範圍、評量及完整練習不變，詳細
閱讀與練習仍留原notebook。維護來源在maintenance/course_repository/ch03_redesign/，
來源與新版PDF依既有ignore規則只留本機，不自動發布，也未commit/push。
12項新版檢查通過並檢視48頁；沒有實際投影或學生理解測試，不宣稱一堂能教完。
下一步優先依序看第19至22頁，確認重複編號、owner查找與ER符號能順暢講解，
再決定是否替換公開PDF或同步notebook。此次課堂回報取代先前只審第27頁的建議。
詳見[重設紀錄](maintenance/course_repository/ch03_redesign/README.md)。

2026-09-14 本批發布授權：教師要求commit and push，範圍包含累積的Ch3教學圖文、
weak entity重點式說明、Ch3／Ch4解答修正及相關維護程式與檢查紀錄。
提交前fetch確認HEAD與origin/main一致；沿用已驗證成品，不重新匯出PDF。
此授權取代下列本批歷史紀錄中的未授權發布狀態；私人來源與其他章節不加入Git。

2026-09-14 Weak entity重點式文字：依教師要求，第12節改用英文短句與條列，
保留全部11個表格、圖片、例子及成立條件；圖後的重點說明與圖保持同頁。
notebook仍為138個Markdown cells／45個附件，PDF仍為57頁；本次僅第24至36頁
有像素變動，其餘頁面與前版相同。77項測試通過；fresh-kernel檢查完成但出現
ZeroMQ socket關閉診斷，詳見紀錄。本次未commit/push；下一步先讀第27頁，
確認條列式講解是否符合課堂使用，再決定是否套用到其他段落。
詳見[本次紀錄](maintenance/course_repository/ch03_er_release.md#weak-entity-key-points-2026-09-14)。

2026-09-14 Weak entity講解重寫：教師表示文字與圖解仍難理解，本次聚焦Ch3第12節，
先以同一組COURSE／SECTION資料辨認物件，再介紹owner、partial key及ER符號；
新增實例連線圖及保留相同課程歸屬、改用全域SectionId的對照。訂單明細、卡片、
多層及多owner例子改用具體編號逐步說明；未調整課程範圍或增加必交作業。
目前notebook為138個Markdown cells；45個附件為23組ER圖、17組表格、5組
個別物件連線圖。PDF57頁，先讀第25、27、28頁；第30頁保留訂單圖與三步讀法。
76項測試與桌面／手機檢查通過，已檢視57頁；這不代表教師或學生已確認理解。
本次只更新本機，保留前次所有未提交工作，未commit/push。下一步先用第25至28頁
確認能解釋「需要owner的身分」與「必須有owner」的差異，再決定是否擴及其他節。
詳見[本次紀錄](maintenance/course_repository/ch03_er_release.md#weak-entity-explanation-2026-09-14)。

2026-09-14 Ch3表格與示意圖修正：教師授權修正本機教材，未授權本次commit/push。
原41個圖片附件不代表41張ER圖；現有43個附件包括22組ER圖、17組表格及4組
個別物件連線圖。新增需求逐步成圖及教師名稱改為授課關係的ER對照，保留原表格；
四處表格解讀改用Tables標題，混合內容明列Diagram and Tables。notebook現132個
Markdown cells，PDF現52頁。新圖在第3、33頁；完整校園圖與讀圖首段同在第40頁。
74項測試、三個全新kernel、桌面／手機預覽及52頁排版檢查通過。來源查核限本次
涉及的課本符號與設計原則，不是完整章節重審；手機密集圖仍需放大，未測教室投影。
Ch1、Ch2、課綱與前次修好的兩份解答成品不變。下一步先看第3、33頁，確認圖形
確實支援課堂逐步講解。詳見
[本次檢查紀錄](maintenance/course_repository/ch03_er_release.md#tables-and-er-diagrams-2026-09-14)。

2026-09-14 Ch3及Ch4解答圖文檢查：教師同意檢查兩份解答並修正已確認問題，
本次未授權commit或push。Ch3解答現為55頁／31圖，Ch4為62頁／47圖；保留全部
35題與33題。移除重複製作標語，Ch3第6、54頁改為具體資料比較，Ch4第4頁
區分relationship與attribute，第20頁補上Address；補充min-max及簡化圖例說明。
已檢查117頁排版、78張PDF圖片與生成來源的像素一致性；19項Ch3、27項Ch4及
71項repository測試通過。此為解答圖文一致性與排版檢查，並非重新逐句查核整本書；
11題建模工具練習仍只有概念解答，未執行ERwin或Rational Rose。課綱與教學版
Ch1至Ch3成品未變。下一步先以Ch3第6頁及Ch4第20頁確認課堂講解與投影可讀性。
完整修正、來源、命令及限制見
[解答檢查紀錄](maintenance/course_repository/ch03_er_release.md#ch3-and-ch4-answer-visual-review-2026-09-14)。

2026-09-14 Ch3發布授權：教師明確要求commit and push。本次提交包含先前累積的
圖文一致性修正、14張新增圖表及去除重複標題／圖說，發布現行41圖、48頁版本。
此項取代下列歷史紀錄中的本機未發布狀態；課綱、解答與未公開章節範圍不變。
提交前已fetch並確認與origin/main沒有分歧；成品沿用已檢查版本，不重新匯出PDF。

2026-09-14 Ch3重複圖文修正：教師指出標題在頁面及圖片內重複。全部41張圖表
改為只在頁面保留一次可搜尋標題與圖說，圖片不再重畫相同標題、結論或固定
Original teaching illustration等文字；資料、符號、連線、解說與練習不變。
notebook仍為128個Markdown cells／41圖，PDF現為48頁，取代下方54頁的成品狀態。
教室查找例子現位於PDF第8頁。70項測試通過，包括34項Ch3測試，已檢查48頁
排版與桌面／手機顯示。此為排版修正，不是新一輪教科書內容查核。Ch1、Ch2、
課綱、解答PDF及發布範圍均未更動；全部本機工作仍未stage、commit或push。
下一步先確認第8頁已符合教師期待的簡潔程度，再沿用既定三組例子試講。
驗證、hash與頁碼變動見maintenance/course_repository/ch03_er_release.md頂端。

2026-09-14 Ch3圖表講解補充：教師表示課堂主要講解圖片與表格，Practice較少使用。
本次依此增加可直接講解的具體資料、連線、正反例與變動前後對照；不把概念的
完整解釋留在Practice。保留原有練習與評量政策，不增加必交要求或新增教學章節。
Ch3新增14張圖表與13段完整worked examples，現為41圖、128個Markdown cells、
54頁PDF；修正前一則27圖／42頁紀錄所述的目前成品數量，該則仍保留修正歷程。
67項repository測試通過，其中31項Ch3測試；三份公開notebook與PDF來源查核、
桌面／手機預覽通過。手機寬表須橫向捲動、密集圖片須放大；未測實際教室投影。
目前只完成Ch3本機更新，未套用到其他章節，也未stage、commit或push。
下一步優先請教師用選課連線、Grade矩陣及弱實體查找三組例子確認講解是否順暢；
預期確認能只靠顯示的圖表解釋資料、規則與結論。完整來源定位、hash、失敗及
重驗紀錄見maintenance/course_repository/ch03_er_release.md最上方。

2026-09-14 Ch3圖文一致性修正：教師同意依課堂回報修正圖表，僅授權本機修正，
本次不commit/push。27張教學圖中11張更新、16張圖片不變；補齊Phone、Product、
Grade及owner keys，保留教師姓名與相同section的改寫對照，兩項限制與衝突判斷
合併為同列，澄清遞迴角色及刻意省略的屬性。課綱、範圍、評量與解答不變。
Intro DB/ch03.ipynb與42頁ch03.pdf已由來源重建；59項repository測試通過，
包含23項Ch3測試，PDF的27張圖與notebook像素一致。桌面與手機無頁面溢出；
手機密集圖仍需放大，不宣稱真實教室投影已驗證。這不是全章重新逐句來源查核。
逐圖對照、hash、命令與限制見maintenance/course_repository/ch03_er_release.md
最上方紀錄。先前的測試未涵蓋本次缺漏，不能據其通過推定全部圖文正確。

2026-09-13 Ch4解答發布：教師明確同意分享ch04_answer.pdf，並授權commit/push。
本次只公開已查核的62頁、47圖原創解答PDF及必要閱讀連結、發布設定與紀錄；
不公開ch04.ipynb、翻拍課本或private_references中的維護來源、HTML與notebook。
此項取代下方Ch4 PDF「僅本機、未授權發布」的限制，其他私人來源限制不變。
解答可獨立於教學notebook發布，仍須明列檔名並驗證PDF及來源notebook的SHA256。
4.28-4.33建模軟體未執行的限制不變；發布授權不代表教師已逐題審閱或六題實驗已完成。
發布查核與重建限制見maintenance/course_repository/README.md的Ch4發布紀錄。

2026-09-12 Ch4解答：教師要求沿用Ch3方式提供answer PDF，未授權本次commit/push。
本機Intro DB/ch04_answer.pdf含翻拍本4.1-4.33英文原創解答、47圖、62頁，
維護來源與逐題查核在private_references/ch04_solutions，均維持Git忽略。
已逐張閱讀Chapter4.pdf全部20張翻拍跨頁；翻拍缺pp.138-139，改以完整同版
教科書pp.108-109補查。4.16、4.18、4.25與4.26(a)存在跨來源差異，依翻拍題目。
另明示BANK圖號錯植、Figure4.9研究生predicate與正文差異，以及UML composition用語。
已通過26項本機測試、重建一致性、PDF文字/47圖完整性及全62頁排版檢查。
4.28-4.33有概念模型與例子，但未操作ERwin/Rational Rose，六題軟體實驗仍未完成。
此份不是出版社官方解答，不代表ch04教學notebook已重寫完成，也不變更課綱與評量。
公開範圍仍為Ch1-Ch3及已核准Ch3解答，未解除Ch4忽略、未更動既有公開教材。
PDF及來源hash、已知限制與逐題定位見private_references/ch04_solutions/source_audit.md。
本份解答下一步為教師確認開放設計題的明示假設，確認前不自動發布。

2026-09-12後續解答查核：教師同意逐題對照翻拍Ch3；查核階段僅修正及驗證本機，
未commit/push。修正3.5答錯比較對象、3.21指定domain遺漏及其他不完整說明；
補齊AIRLINE關係圖、ADOPTS三元圖、資料庫環境及3.28逐項正反例。
本機解答現含35題、31圖；3.1-3.30書面要求已逐項查核，3.31-3.35有概念解答，
但原題要求的建模軟體操作仍未完成，不得把五題實驗題標為全部完成。
詳細對照與驗證見maintenance/course_repository/ch03_er_release.md頂端逐題紀錄。
教師隨後明確授權commit/push。本次提交將已查核的56頁、31圖解答PDF及相關
維護紀錄納入origin/main發布；PDF內容及hash不再變更。私人來源不在提交範圍。
下方26圖是前次發布紀錄；private_references及其他未發布章節維持忽略。

2026-09-12教師明確授權將既有Ch3原創解答轉成Intro DB/ch03_answer.pdf，
並commit/push到公開GitHub。此份獨立PDF包含3.1-3.35及26張原創圖；
不混入ch03.ipynb或ch03.pdf，不變更教學範圍或評量。
這項決策取代下方「解答不發布」的舊限制，但只核准解答PDF；
private_references內維護來源、解答HTML/notebook及翻拍課本仍忽略且不上傳。
首頁新增PDF連結；公開成品的hash及來源notebook hash列入repository_config.json。
重新生成需本機private_references/ch03_solutions來源；公開clone可驗證成品，
不能只靠公開檔案重建這份解答。詳細驗證見maintenance/course_repository/README.md。

GitHub最新發布決策：教師要求線上教材僅放現用課本Ch1、Ch2、Ch3。
教師後續要求將這三份notebook另轉PDF並commit/push；Intro DB保留原notebook，
並加入ch01.pdf、ch02.pdf、ch03.pdf，內容與保存的輸出不變，不包含習題解答。
PDF由export_chapter_pdfs.py及print_chapter_pdfs.cjs生成，metadata記錄notebook
SHA256，避免教材改版後誤把舊PDF視為最新版。公開章節仍限Ch1-Ch3。
課綱保留完整學期進度；Intro DB/ch05、ch08及全部under_revision只留本機，
其他章節的maintenance來源與SQLite整包同步停止Git追蹤並ignore，不刪本機資料。
既有Git歷史不改寫。首頁與課綱不再連到未發布notebook。
published_chapters控制預設建置及驗證；--include-unreleased僅供有完整本機來源時使用，
不會將ignore解除或自動發布。此決策只限制發布範圍，不取消後續章節教學。
本次GitHub更新包括上一筆已核准的Ch3修正；解答與翻拍原書仍不發布。

Ch3最新追加：教師回報已使用ch03.ipynb，要求增加weak entities範例並加入
3.9.2及3.10。現行範圍為3.1-3.7、3.9.1-3.9.2、3.10；3.8仍不列本章教學。
同一notebook擴至27張圖，增加owner-local、strong/weak對照、多層及多owner，
三元pair限制與participation counts，以及UNIVERSITY全部九種relationships和額外唯一性規則。
原本單學期弱SECTION與3.10有SecId的regular SECTION必須分開；Figure 3.20的
HAS學生(0,1)與翻拍本p.123正文一個主系所的差異原樣記錄，不假裝來源完全一致。
教師後續同意查核修正並授權本機commit，未要求push或調動週次、考試；
新增份量需另行確認授課停止點。翻拍Chapter3.pdf共24張跨頁、紙本pp.89-135，
已逐頁檢視並對照現行教學；學生閱讀頁碼改用翻拍本，章節號碼作跨版本定位。
Figure 3.20的CCode與CoName在兩份來源都有底線；先前說CoName未加底線是
查核錯誤，已修正，不再稱為課本差異。
教師另要求所有Ch3習題解答，涵蓋3.1-3.35，含review及laboratory questions。
原創英文解答、圖表、生成來源與驗證暫存private_references/ch03_solutions，
維持Git忽略，不混入學生ch03.ipynb；公開課程repo不自動包含解答或翻拍原書。
解答不是出版社官方解答；ERwin/Rational Rose未實際執行，課程不因此增加UML範圍。
最新驗證及限制見maintenance/course_repository/ch03_er_release.md頂端紀錄。
下方Ch3首次發布的16圖及commit/push授權為歷史狀態，不適用本次追加。

教師最新指定：今天只教Ch1、Ch2；之後按Ch3-Ch9、Ch14-Ch19順序授課，
並授權修正相關文件後commit/push。ER/EER均必教；Ch4仍含4.1-4.7，
Ch9仍含9.1-9.2。Ch15、Ch18、Ch19恢復正式選講；Ch16安排完整一週選講，
Ch20不另列授課章節。不得再沿用先SQL後ER的次序或今天安排Ch5。

Weeks 2/3/4分別為Ch3、Ch4前段、Ch4後段及Ch5；Week 5為Ch6；
Weeks 7/8為Ch7/Ch8；Week 10為Ch9；Week 11為Ch14/Ch15選講；
Weeks 13/14/15為Ch16、Ch17、Ch18/Ch19選講。
考試日期及30/30/30/10不變；Exam 1為Ch1-6，Exam 2為Ch7-9與Ch14-15，
Exam 3為Ch16-19加已教SQL與設計。出國、放假、期末考及補考安排不變。
細部必教/排除內容依maintenance/COURSE_PLAN.md，不能將列章等同整章全教。
Ch14/15與Ch18/19各合併一週，份量仍需實際授課確認；只考已教與練習內容。

今天入口是課綱、ch01.ipynb、ch02.ipynb；現有ch05/ch08延至Weeks 4/8。
Ch3後續已新增一章一份的教材：16張原創圖、校園小例子、逐節預測及畫圖練習，
含Week 2既定小組比較；不要求SQL或提前教Ch9 mapping。教科書Ch3完整文字
pp.59-105已閱讀，所教概念及關鍵符號另有對照；不是全書或每題習題查核完成。
目前新版為Ch1、Ch2、Ch3、Ch5及Ch8；Ch4及其餘章節仍待改寫。
本次授權完成後commit/push，驗證與限制見maintenance/course_repository/ch03_er_release.md。
最新查核見maintenance/course_repository/full_source_audit.md#chapter-order-and-expanded-scope。

## 歷史決策紀錄

以下日期紀錄保留追溯；與上方最新範圍衝突時，不再作為本期指令。
- 2026-09-10教材續修：教師授權修正後commit/push。Ch1、Ch2保留導論選講；
  Ch5在原第一堂停止點後補5.1-5.3的keys、constraints與資料異動；
  新增獨立Ch8 notebook，依課綱教8.1-8.3指定algebra及8.5簡單組合，
  不含division、calculus或進階algebra。維持一章一份，日期、配分與EER範圍不變。
  Ch5/Ch8完整章節文字已閱讀，所教主題逐項定位並以原創例子驗證；
  不等於逐題解答、所有原圖目視或全書逐句完整查核完成。
  最新教材入口、範圍與驗證紀錄見
  maintenance/course_repository/full_source_audit.md#relational-foundations-revision。
  此段取代下方Ch5只有第一堂及Ch8尚無新版的歷史狀態；舊ER缺陷仍待處理。
- 2026-09-10最新EER決策：教師要求EER都教，重新調整進度，課綱標明章號及
  教科書正式章名。Ch4的4.1-4.7全列教學，搭配Ch9的9.1-9.2；Weeks 7-8
  完成ER與9.1，Weeks 10-11教EER與9.2。UML、abstraction、knowledge
  representation及ontology依課本作入門介紹，不新增軟體或ontology專案。
  為維持既有授課週數，14.1-14.4移至Week 13，以已給定candidate keys教至3NF；
  14.5 BCNF及Ch15改為延伸，不列必考。Exam 2改考ER/EER及mapping；
  正規化移至Exam 3。小組比較改Weeks 2、4、10、13、14，AI活動仍4、10、14。
  Exam 1/2/3日期、30/30/30/10配分、11/1-8出國、Week 17放假及Week 18補考不變。
  這是進度修正，不是Ch4/9.2教材或完整來源查核完成；新範圍對照尚需補齊。
  下方較早排除Ch4/9.2、Week 11正規化及Week 13必教Ch15的紀錄由此取代。
  教師後續要求本機相關文件與這份課綱一致，並明確授權commit/push至既有origin/main。
  考試與出國複習週也列Ch章號；首頁使用完整章名。保留舊教材的修訂中狀態，
  不將新進度等同於全章教材完成。發布結果以Git history與遠端核對為準。
  詳細查核見maintenance/course_repository/full_source_audit.md#eer-schedule-revision-record。
- 2026-09-09課綱精簡：教師要求所有課綱內容簡短、只留必要訊息。學生課綱保留
  基本資料、教科書、簡短介紹、逐週簡短進度、評量及必要規則；詳細選講小節、
  教學範圍、排除內容及備課要求移至maintenance/COURSE_PLAN.md的Detailed Coverage，
  原有範圍原文保留。本次不增刪章節、不改日期、配分或政策，也不改notebook。
  每週Topic至多16個英文單字；教師後續明確授權修正後commit/push至既有main。
  驗證：七項課綱測試、內容/連結及manifest檢查通過；詳細範圍與移動前原文
  完全相同；1440/390像素預覽無頁面溢出，已目視桌面完整課綱。未修改或重跑
  notebook/SQL；發布結果以Git history為準。
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
- 課程主體：relational model、relational algebra、SQL、ER/EER model、
  ER- and EER-to-relational mapping、functional dependencies、normalization，以及選定的
  storage/file organization、indexing、query processing與query optimization選講；
  不要求DBMS實作、完整成本推導、concurrency-control或recovery演算法。
- 課程可在教師允許時訓練學生檢查 AI 產生的 SQL、ER diagram、schema、
  query plan判讀；這是教師加入的應用，不宣稱為教科書原有章節。

## 用語與學生可見內容

- 所有正式學生教材使用English-only prose；technical terms使用教科書與資料庫領域
  的標準英文用語。教師端治理、查核與備課文件可使用繁體中文。
- 學生可見文件直接描述概念講解、完整範例、個人練習、小組比較、教師回饋
  與個人修正，不使用學生無法從課程內容理解的教學設計分類名稱。
- 課程計畫與逐章教材不寫分鐘配置；需要控制份量時，以授課摘要、課堂核心
  內容及課後延伸內容區分。
- 不把課堂流程、評量方式或 AI 使用方式另取未經教師核准的名稱。
- Week 1只教Ch1/Ch2導論與架構；Ch3 ER在Week 2，Ch4 EER在Weeks 3-4，
  Ch5關聯模型與正式keys分類在Week 4。SQL寫作從Week 5的Ch6開始。
- 一章一份notebook，不建立week1.ipynb；只在教師指定時繳交練習。
- 預測正確時可解釋原因，不要求學生捏造一次修正。

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
  2026-11-05 不排實體課、考試或新進度，只複習已教的Ch1-Ch8選定內容。
- Week 17 的 2026-12-31 為校慶補假，不排課。
- Week 6 的 2026-10-15 辦理Exam 1；Week 12的2026-11-26辦理Exam 2。
- Weeks 13-15的既有範例併入複習；Week 16的2026-12-24辦理Exam 3與課程期末考。
- Week 18的2027-01-07在校定期末考週，保留補考，不另排正式期末考或新進度。

## 評量與章節對應

| 評量 | 週次與日期 | 比例 | 範圍 |
|---|---|---:|---|
| Written Exam 1 | Week 6, 2026-10-15 | 30% | Ch1-6已教內容：導論、ER/EER、關聯模型、basic SQL |
| Written Exam 2 | Week 12, 2026-11-26 | 30% | Ch7-9及Ch14-15已教選講：SQL、algebra、mapping、正規化與引導式分解 |
| Written Exam 3 / Final Examination | Week 16, 2026-12-24 | 30% | Ch16-19選講；累積已教SQL與database design |
| Class Performance（課堂表現） | 全學期 | 10% | 指定練習、解釋、驗證與修正；peer rank不直接計分 |

- Exam 2的Ch14包括至BCNF的小例子；Ch15提供candidate keys及minimal cover，
  教短closure、lossless/dependency preservation比較與Algorithm 15.4引導步驟。
  不考general chase、minimal-cover推導、完整BCNF演算法或未練習內容。
- Exam 3考所教storage、indexing、query processing及optimization，不另考Ch20。
- 三次written exams皆為個人且AI-free，其他可用資源待宣布。
- Week 18補考不另增配分；資格、範圍及計分安排待教師另行宣布。

## 課堂活動決策

- 全學期規劃5次小組共同回答與個人完整比較，安排於Weeks 2、4、10、13、14。
  主題改為ER限制、EER/keys、mapping、file organization、indexes。
  AI活動仍Weeks 4、10、14，依序檢查EER/constraint、mapping與index建議。
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

Ch3課後追加後的下一步：先依教師今天實際講到的位置，確定新增弱實體、3.9.2、
3.10的接續授課停止點。新增範圍及教材份量是改變優先順序的新原因；完成條件為
教師確認接續範圍與是否需要調整Ch4開始位置，再更新有必要變動的週次。
本次不自行改期、不增加考試要求。下方Ch4製作建議保留，待此教學銜接確定。

2026-09-10最新：Ch3完成後，下一步是Ch4的4.1-4.7教材，優先準備Week 3使用的
4.1-4.4，仍維持一章一份並沿用本次校園案例。理由是Ch3已補上且Ch4為下一堂
必教內容；預期成果為有原文定位、圖解及例子的ch04.ipynb，完成條件是核准範圍
具備講解、預測、範例、判讀及練習，並通過來源、圖形與重建查核。這是下一步
建議，尚未自動開始Ch4。舊ER SQL的NULL-key缺陷仍待Ch9重用前修正；本章未重用。
下方是歷史建議，不再取代此處的下一步。

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
