# 資料庫管理

本資料夾保存資料庫管理課程的 115-1 規劃、歷年來源、SQL labs 與
評量工作材料。現行決策以 `PROJECT.md`、英文修訂課綱及 `COURSE_PLAN.md`
為準。

## 主要內容

- `1151_course_analysis.md`：課程分析。
- `PROJECT.md`：固定決策、章節範圍、文件優先順序及未解問題。
- `1151_database_management_revised_syllabus.md`：現行英文課綱。
- `COURSE_PLAN.md`：現行18週授課摘要、課堂活動、評量與備課依據。
- `working_materials/`：建置中的 SQL labs、資料庫與評量材料。
- `working_materials/course_material_integration_report.md`：逐章教材與驗證總表。
- `working_materials/pre_instructor_review_audit.md`：教師審閱前的全課程檢查結果。
- `from_11001_DB/`：歷史來源。

## GitHub 注意事項

本資料夾是獨立 Git repository，`main`追蹤GitHub的`origin/main`。目前只追蹤經
allow-list檢查的治理文件、課綱、課程計畫、逐章教材、驗證程式及核准的SQLite
學生套件。

現行`KennethWYLee/Database`是private repository。GitHub visibility作用於整個
repository，不能在同一private repository內只把個別檔案設為public。未來選擇性公開
時，應把教師核准的逐檔allow-list複製到另一個public repository或release artifact；
未核准內容不得移出目前private repository。

歷屆題目、答案、評分資料、教科書、歷史來源、暫存檔及發布來源未確認的資料仍由
`.gitignore`排除，不得因檔案存在於本機就直接加入或公開。
