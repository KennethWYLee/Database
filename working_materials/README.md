# Working Materials

這裡放 115-1 資料庫管理會高頻使用的工作素材。原始完整教材仍保留在 `from_11001_DB`。

## 目前已整理

| 位置 | 內容 |
|---|---|
| `chapters/` | Ch2-Ch7與Ch14-Ch19的學生教材、活動及教師驗證紀錄 |
| `sql_labs/university_db` | `smallRelationsInsertFile.sql`, `largeRelationsInsertFile.sql`, `univdb-sqlite.db` |
| `assessments/reference_midterm` | 舊期中考題、答案、公版 PDF/DOC |
| `student_sqlite_package` | 學生SQLite套件allow-list、操作說明、build script、output資料夾與ZIP |
| `course_repository` | 將各章來源整合為12份自包含`chXX.ipynb`及單一課程進度表 |
| `pre_instructor_review_audit.md` | 教師審閱前的一致性、完整性、執行與發布邊界檢查 |

## 使用原則

- `from_11001_DB` 視為原始素材庫，不直接清理。
- `working_materials` 放本學期會直接使用或改寫的材料。
- SQL上機正式使用SQLite 3；現有教材以SQLite 3.45.3驗證。學生不需另裝server
  DBMS，SQLite未完整呈現的功能以概念、schedule、log或教學程式說明。
- `student_sqlite_package/package_files.json`是學生套件的發布allow-list；個別
  SQL、schema、data、diagram及program仍以chapter目錄中的檔案為維護來源。
- `course_repository/repository_config.json`定義週次、章節與來源對應；build script
  將reading、SQL、Python、data及圖片整合成根目錄的一份`chXX.ipynb`。圖片以
  notebook attachment保存，其他範例以cell內嵌，目前不需要`assets/`、lab runner或
  chapter subdirectories；生成的`output/`不加入Git或自動發布。
- `sql_labs/university_db`的發布來源與授權尚未確認，不放入學生套件。
