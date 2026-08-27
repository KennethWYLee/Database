# Chapter 17 Transactions

## 核心問題

一筆銀行轉帳同時修改兩個帳戶。如果程式只完成扣款就失敗，或兩位使用者同時
修改相同資料，資料庫如何避免留下不完整或互相矛盾的結果？本章用
**transaction**、**schedule**、**serializability**、**recoverability** 與
**isolation level** 回答這個問題。

## 與前章的關係

Chapter 14-16 說明 DBMS 如何用 index、physical plan 與 optimizer 執行一個
query。本章改問：當多個 query 與 update 同時執行，而且執行期間可能失敗時，
整體結果如何維持正確。Chapter 18 會進一步說明 lock 與其他 concurrency-control
方法，Chapter 19 則處理 log-based recovery。

## 先備知識

你應能閱讀 `SELECT`、`INSERT`、`UPDATE`、primary key、foreign key 與 `CHECK`
constraint，並能區分資料庫 schema 與目前的資料內容。

## 學習目標

完成閱讀與活動後，你應能：

1. 用一個完整例子解釋 atomicity、consistency、isolation、durability。
2. 判斷 transaction 的 active、partially committed、failed、aborted 與 committed
   state。
3. 說明 concurrent execution 的效益，以及錯誤 interleaving 的風險。
4. 找出兩個 operations 是否 conflict，建立小型 precedence graph，並判斷 graph
   是否有 cycle。
5. 以小型schedule判斷basic recoverability及不安全的commit/read order。
6. 比較 SQL isolation levels 與 dirty read、nonrepeatable read、phantom。
7. 使用 SQL transaction 完成 `COMMIT` 與 `ROLLBACK`，並保存可檢查的結果。

## 授課摘要

| 教學內容 | 完整範例與練習 | 學習證據 |
|---|---|---|
| transaction boundaries、ACID、states | 銀行轉帳成功與中途失敗案例 | 轉帳判斷表 |
| concurrent schedules、conflicts、small precedence graphs | acyclic與cyclic schedules | precedence graphs與判斷理由 |
| basic recoverability及isolation phenomena | commit/read order、dirty read、nonrepeatable read與phantom | anomaly/isolation對照 |
| SQL transaction操作 | rollback、commit與constraint failure | SQL輸出與修正說明 |

Locking、timestamp ordering及multiversion implementation只作與Chapter 18的銜接，
不列為本章主要操作題。

---

## 1. Transaction 與 ACID

### 1.1 Transaction 是什麼

Transaction 是一個存取且可能更新多個 data items 的執行單位。應用程式可能用
多個 SQL statements 完成一個 transaction；因此，「一個 statement 成功」不等於
「整個業務操作完成」。

銀行從 A 轉 50 到 B 的 transaction 可抽象為：

```text
read(A)
A := A - 50
write(A)
read(B)
B := B + 50
write(B)
```

若初始 `A=1000`、`B=2000`，正確完成後是 `A=950`、`B=2050`，而總額仍為
3000。

### 1.2 ACID 的四個要求

| Property | 本章中的意思 | 轉帳例子 |
|---|---|---|
| Atomicity | transaction 的效果全部發生，或全部不發生 | 不能只扣 A 而沒有增加 B |
| Consistency | 若開始時符合規則，transaction 單獨正確執行後仍符合規則 | 餘額不可為負，總額應保持 3000 |
| Isolation | concurrent transactions 的交互作用受到控制 | 其他 transaction 不應把半完成轉帳當成最終資料 |
| Durability | committed updates 在系統故障後仍應保存 | 成功回覆後，轉帳不能因 crash 消失 |

Consistency 不是 DBMS 能單獨保證的一切。DBMS 可執行 constraint 與
concurrency/recovery protocol，但應用程式仍必須寫出正確的業務操作。例如，若
程式在同一個 transaction 中同時替 A 與 B 各增加 50，transaction 即使完整
`COMMIT`，仍破壞「總額不變」的規則。

Durability 也不能由本章的一次正常關閉實驗證明。lab 只檢查：SQLite 回報
`COMMIT` 後，關閉並重新開啟 database file 時資料仍存在。真正的 crash、storage
failure 與 recovery mechanism 留待 Chapter 19。

### Worked example 1：判斷失敗位置

某程式依序執行：

```text
1. A := A - 50
2. 寫入 A
3. 系統失敗
4. B := B + 50
```

若 step 2 已保留而 step 4 沒有執行，atomicity 被破壞，資料也不再符合總額規則。
Recovery system 必須撤銷這個未完成 transaction 的部分效果；不能把半套結果當成
committed transaction。

### Practice 1

判斷下列敘述主要涉及哪一個 ACID property，並寫一句理由：

1. 兩位職員同時修改同一帳戶後，其中一人的修改消失。
2. 系統已顯示訂單成功，但重新啟動後訂單不存在。
3. 訂單明細建立成功，但訂單主檔沒有建立。
4. 程式讓庫存量成為負數，而且 schema 沒有 constraint 阻止它。

**檢查依據：** 依序應以 isolation、durability、atomicity、consistency 為主要
判斷；答案必須指出具體資料效果，不能只抄四個名詞。

---

## 2. Transaction State

### 2.1 主要 states

```text
active -> partially committed -> committed -> terminated
   |               |
   +-----> failed <-+
             |
             v
          aborted -> terminated
             |
             +-----> active (符合重新執行條件時)
```

- **active**：transaction 正在執行。
- **partially committed**：最後一個 statement 已執行，但 commit 的 durability 尚未
  確立。
- **committed**：transaction 成功完成，系統已接受其效果為永久結果。
- **failed**：transaction 無法繼續正常執行。
- **aborted**：系統已撤銷 transaction 的資料效果，database 回到該 transaction
  開始前的狀態。
- **terminated**：transaction 已離開系統。

Aborted transaction 不一定都能重新執行。若原因是暫時性 deadlock，restart 可能
合理；若原因是錯誤 SQL、違反 constraint 或不正確的應用邏輯，原樣重跑通常仍會
失敗。

### Worked example 2：constraint failure

假設 `balance` 有 `CHECK (balance >= 0)`。A 的餘額是 1000，但程式要求扣除
5000。Transaction 在 active state 遇到 constraint violation，接著必須由程式或
DBMS 依該 DBMS 的規則處理 statement failure，並在需要時 `ROLLBACK`。不能把
「某一 statement 失敗」一概當成「所有 DBMS 都自動 rollback 整個 transaction」；
錯誤後 transaction 是否仍可用，必須查該 DBMS 的規則。

### Practice 2

為下列事件寫出可能的 state path：

1. 所有 statements 完成，commit record 成功寫入。
2. 執行中發生 deadlock，系統選擇此 transaction 為 victim，rollback 後重試。
3. 最後一個 statement 完成，但在 commit 確立前發生 failure。

**檢查依據：** 第 1 題應經過 `active -> partially committed -> committed`；第 2 題
至少包括 `active -> failed -> aborted -> active`；第 3 題必須指出 partially
committed 仍不等於 committed。

---

## 3. Concurrent Execution 與 Schedule

### 3.1 為何同時執行

Concurrent execution 可讓一個 transaction 等待 I/O 時，另一個 transaction 使用
CPU 或其他資源，因此可改善 throughput 與 resource utilization，也可減少短
transaction 被長 transaction 完全擋住的平均等待時間。代價是 operations 的
interleaving 可能產生不正確結果。

**Schedule** 記錄多個 transactions 的重要 operations 先後次序，而且必須保留每個
transaction 內原有的 operation order。若一個 transaction 完成後下一個才開始，
它是 **serial schedule**。Operations 可以交錯，但結果等價於某個 serial order，則
它是 **serializable schedule**。

### 3.2 哪些 operations 會 conflict

兩個 operations 同時符合以下三個條件才 conflict：

1. 來自不同 transactions。
2. 存取相同 data item。
3. 至少一個是 `write`。

因此同一 item 的 `read-read` 不 conflict；`read-write`、`write-read`、
`write-write` 都 conflict。不同 items 的 operations 不因時間接近就自動 conflict。

### Worked example 3：acyclic precedence graph

```text
1. r1(A)
2. w1(A)
3. r2(A)
4. r2(B)
5. w2(B)
```

`w1(A)` 在 `r2(A)` 前，因此 precedence graph 有 `T1 -> T2`。沒有反方向的 edge，
graph 無 cycle；此 schedule 是 conflict serializable，一個對應的 serial order 是
`T1, T2`。

### Worked example 4：cycle

```text
1. r1(A)
2. r2(B)
3. w1(B)
4. w2(A)
```

- `r2(B)` 在 `w1(B)` 前，得到 `T2 -> T1`。
- `r1(A)` 在 `w2(A)` 前，得到 `T1 -> T2`。

Graph 有 cycle，所以此 schedule 不是 conflict serializable。Cycle 已足以否定
conflict serializability；本課不要求實作一般化的完整測試演算法。

### Practice 3

分析下列 schedule：

```text
r1(A), r2(A), w2(A), r1(B), w1(B), c2, c1
```

1. 圈出所有 conflict pairs。
2. 寫出 precedence graph edges。
3. 判斷是否 conflict serializable；若是，給一個 serial order。

**檢查依據：** `r1(A)` 在 `w2(A)` 前產生 `T1 -> T2`；沒有 `T2 -> T1` 的
conflict，故 graph acyclic，serial order 為 `T1, T2`。Commit order 不必等於
serialization order。

---

## 4. Recoverability 與 Cascadeless Schedules

Serializability 處理 concurrent result 是否等價於 serial result；recoverability 則
處理一個 transaction 讀到另一個 transaction 的值之後，兩者應以什麼順序 commit。
兩者回答不同問題。

若 `Tj` 讀到 `Ti` 寫入的值，recoverable schedule 要求 `commit(Ti)` 發生在
`commit(Tj)` 之前。否則 `Tj` 已 commit，之後 `Ti` abort 時，系統無法再正常撤銷
已對外承諾的 `Tj`。

Cascadeless schedule 要求更早：`commit(Ti)` 必須發生在 `Tj` 讀取該值之前。
因此 `Tj` 不會讀到未 committed data，也不會因 `Ti` abort 而被迫 cascading
rollback。所有 cascadeless schedules 都是 recoverable；反方向不一定成立。

### Worked example 5：三種 commit/read order

```text
S1: w1(A), r2(A), c2, a1
S2: w1(A), r2(A), c1, c2
S3: w1(A), c1, r2(A), c2
```

- `S1` nonrecoverable：T2 在 T1 之前 commit。
- `S2` recoverable but not cascadeless：T2 commit 前 T1 已 commit，但 T2 讀取時
  T1 尚未 commit。
- `S3` cascadeless：T2 只讀已 committed 的 T1 結果。

### Practice 4

將 `w1(X), r2(X), c1, c2` 改成 cascadeless schedule，只能移動 `r2(X)`，且不可
改變每個 transaction 內的順序。

**檢查依據：** 合法答案是 `w1(X), c1, r2(X), c2`；重點是 writer commit 先於
dependent read，不只是先於 reader commit。

---

## 5. Isolation Levels 與 Anomalies

完整 serializability 可能限制 concurrency。SQL 因此提供較弱 isolation levels，讓
系統在一致性風險與效能之間作選擇。名稱相同的 isolation level 在不同 DBMS 的實作
細節仍可能不同；使用時要查該 DBMS 文件並執行 concurrent test。

### 5.1 三種常見 anomalies

- **dirty read**：T2 讀到 T1 尚未 commit 的值，之後 T1 abort。
- **nonrepeatable read**：T1 在同一 transaction 兩次讀同一 row，T2 在中間 commit
  update，使兩次值不同。
- **phantom**：T1 以 predicate 查詢一組 rows；T2 在中間 insert、delete 或 update
  會改變 predicate matching set 的資料，T1 再查時看到不同的一組 rows。

Lost update 是另一個重要風險：兩個 transactions 都以較舊值計算更新，其中一個
write 覆蓋另一個 write 的效果。不能只用「我沒有 dirty read」推論 lost update
一定不會發生。

### 5.2 Textbook model 中的四個 levels

| Isolation level | 讀取承諾 | 主要限制與風險 |
|---|---|---|
| Serializable | 結果須符合 serializable execution | 最強標準層級；仍需 DBMS 正確處理 predicate conflicts |
| Repeatable read | 只讀 committed data；同一 item 重讀保持一致 | 仍可能有 phantom，因此不必然 serializable |
| Read committed | 只讀 committed data | 同一 item 重讀可能不同，也可能有 phantom |
| Read uncommitted | 可讀 uncommitted data | dirty read、nonrepeatable read、phantom 都可能發生 |

本章教科書的定義中，四個 levels 都不允許 dirty write，也就是不能直接覆寫另一個
尚未 commit transaction 所寫的 item。實際 DBMS 的 statement behavior、locking、
version visibility 與錯誤處理仍需另行確認。

### Worked example 6：phantom 不是一般的同一 row 重讀

T1 執行：

```sql
SELECT COUNT(*) FROM instructor WHERE salary > 90000;
```

接著 T2 insert 一位薪資 100000 的 instructor 並 commit，然後 T1 再執行同一個
predicate query。第二次可能多一 row。新 row 第一次查詢時尚不存在，所以只追蹤
第一次實際讀到的 row locks，未必足以表示 predicate conflict。Concurrency control
還必須考慮尋找 rows 所使用的 predicate 或 access structure。

### Practice 5

將情境配對到最直接的 anomaly：

1. 同一 transaction 兩次查詢 `student_id=101` 的 GPA，值不同。
2. 同一 transaction 兩次查詢 `GPA >= 3.5`，第二次多一位新 student。
3. 查到一個尚未 commit 的餘額，writer 隨後 rollback。

**檢查依據：** 依序是 nonrepeatable read、phantom、dirty read。第 1 題鎖定同一
row；第 2 題是 predicate matching set 改變。

---

## 6. DBMS 如何實作 Isolation：概念比較（課後延伸）

本節只建立 Chapter 18 所需的地圖，不推導完整 protocol。

| 方法 | 基本做法 | Worked example | 需注意的限制 |
|---|---|---|---|
| Locking | 讀寫 data item 前取得相容的 lock | reader 取得 shared lock；writer 需要 exclusive lock | lock 持有時間與順序影響 correctness、等待與 deadlock |
| Timestamp ordering | 以 transaction timestamp 與 data-item read/write timestamps 判斷操作是否過時 | 較舊 transaction 嘗試做不符 timestamp order 的 write 時可能被拒絕或 restart | 規則與 abort 成本需由具體 protocol 決定 |
| Multiversion | 保存同一 item 的多個 versions，讓 reader 讀合適 snapshot | reader 可讀 transaction 開始時可見的 committed version | snapshot isolation 不自動等於 serializable，write conflict 可能導致 abort |

Locking 不表示「整個 database 永遠只能一人使用」；lock granularity 可以是 database
或較小 data item。Multiversion 也不表示「所有 concurrent schedules 都正確」；
version visibility 與 writer conflict rule 決定實際 isolation。

### Practice 6

某系統讓長時間 report 讀取舊的 committed versions，同時允許另一個 transaction
更新新 version。這最接近哪一類方法？你還需要哪一項證據才能聲稱 execution 是
serializable？

**檢查依據：** 第一問是 multiversion。第二問必須檢查具體 isolation guarantee 或
整個 schedule，而不能由「reader 沒有等待」推論 serializable。

---

## 7. Transaction Definition in SQL

教科書以 transaction 隱含開始、下列 statements 結束目前 transaction：

```sql
UPDATE account SET balance = balance - 50 WHERE account_id = 'A';
UPDATE account SET balance = balance + 50 WHERE account_id = 'B';
COMMIT WORK;

-- 發現錯誤時改用：
ROLLBACK WORK;
```

`COMMIT WORK` 與 `ROLLBACK WORK` 是兩種不同結尾，不會在同一次 execution 中
連續執行。SQL 也提供設定 transaction isolation level 的概念，例如
`SERIALIZABLE`、`REPEATABLE READ`、`READ COMMITTED` 與 `READ UNCOMMITTED`。
但是 transaction 開始語法、autocommit default、設定 isolation 的語法與實際行為
都依 DBMS/driver 而異。

本 lab 使用 SQLite 可執行語法：

```sql
BEGIN;
-- statements
COMMIT;

BEGIN;
-- statements
ROLLBACK;
```

`BEGIN IMMEDIATE` 在此 lab 中用來在 transaction 開始時要求 write transaction。
它不是可直接移植到所有 DBMS 的標準寫法。

### Worked example 7：rollback 與 commit

初始資料：

```text
A = 1000, B = 2000
```

第一次 transaction 將 A 暫時改成 950，接著 `ROLLBACK`。Rollback 後應回到
`A=1000, B=2000`。第二次 transaction 同時扣 A、加 B、寫入 log，然後
`COMMIT`。最終應為 `A=950, B=2050`，總額仍為 3000，且有一筆 committed log。

### Practice 7

替轉帳加上三個檢查：

1. 來源帳戶存在且餘額足夠。
2. 目的帳戶存在。
3. Account updates 與 transfer log 必須一起 commit 或一起 rollback。

**檢查依據：** 測試至少包含正常轉帳與餘額不足兩條路徑；每條路徑都檢查兩個
balances、總額與 log row count。只顯示「SQL 沒報錯」不算完整證據。

---

## 8. 執行活動

### 8.1 SQL transaction lab

先寫下兩個預測，再執行：

```powershell
sqlite3 ch17_lab.db ".read student_lab.sql"
```

核對重點：

1. Transaction 內、rollback 前，A 暫時是 950。
2. `ROLLBACK` 後 A 回到 1000，B 仍是 2000。
3. `COMMIT` 後 A 是 950，B 是 2050。
4. Total 是 3000，log count 是 1。

不要把第 1 點的中間結果解讀成其他 connections 一定能看到它；那是目前同一
transaction 內的觀察。

### 8.2 Schedule analyzer

執行：

```powershell
py -3 schedule_analyzer.py schedule_examples.json
```

程式依序：

1. 找出不同 transactions 對同一 item 的 conflicting operations。
2. 建立 precedence graph edges。
3. 對小型 graph 進行 topological ordering；找不到完整 order 表示有 cycle。
4. 在範例假設下，追蹤每次 read 所看到的最近 preceding write，判斷 commit/read
   order 是否 recoverable、cascadeless。

這個程式是教學用的有限模型，不是 DBMS concurrency controller。它沒有處理
predicate reads、versions、conditional writes 或完整 SQL semantics；因此 phantom
仍要用本章的 predicate example 另外說明。

### 執行前預測

| Schedule | Conflict serializable? | Recoverable? | Cascadeless? |
|---|---:|---:|---:|
| `acyclic` | Yes | Yes | Yes |
| `cycle` | No | Yes | Yes |
| `recoverable_but_not_cascadeless` | Yes | Yes | No |
| `nonrecoverable` | Yes | No | No |
| `cascadeless` | Yes | Yes | Yes |

`cycle` 沒有 read-from dependency，因此 recoverability checks 會通過；這再次說明
serializability 與 recoverability 是不同條件。

---

## 9. 常見錯誤、反例與失敗情境

1. **把 serial schedule 與 serializable schedule 當同義。** 前者沒有 interleaving；
   後者可 interleave，但效果等價於某個 serial order。
2. **看到 write 就畫 edge。** Edge 需要不同 transactions、相同 item、至少一個
   write，而且方向由 schedule order 決定。
3. **只檢查 graph 就宣稱可安全 recovery。** Acyclic graph 不保證 recoverable。
4. **把 recoverable 當成 cascadeless。** Writer 在 reader commit 前 commit 還不夠；
   cascadeless 要 writer 在 dependent read 前 commit。
5. **把 `COMMIT` 當成業務邏輯正確證明。** DBMS 可 commit 一個邏輯寫錯但未違反
   constraint 的 transaction。
6. **把 repeatable read 當成一定沒有 phantom。** 同一 row 重讀穩定，不表示
   predicate matching set 不會改變。
7. **把 snapshot isolation 當成 serializable。** 某些 executions 可能不
   serializable，必須看具體 protocol 與 schedule。
8. **從單一 SQLite connection 推論一般 concurrent behavior。** Isolation 必須用
   多 connections、明確 transaction boundary 與指定 DBMS 重新驗證。

## 10. 課堂討論

### Discussion A

訂票系統只剩一個座位。兩個 transactions 都先讀到 `remaining=1`，再各自建立一筆
訂單。請分別用 consistency、isolation 與 serializability 說明問題。

**回答依據：** 必須寫出 initial state、兩個 reads/writes、final state，以及哪個
serial order 能否產生相同結果。只說「race condition」不足以完成分析。

### Discussion B

某 dashboard 可接受報表略舊，但付款流程不可重複扣款。兩者是否應一律使用相同
isolation level？

**回答依據：** 比較資料錯誤後果、可接受 staleness、read/write pattern、retry 與
DBMS 實際 guarantee；不能只以「越高越安全」作結論。

## 11. 個人應保存的學習證據

1. ACID 四題判斷與理由。
2. 一張 acyclic 與一張 cyclic precedence graph。
3. 三個 recoverability/cascadelessness 判斷。
4. Isolation anomaly 配對與 phantom 解釋。
5. `student_lab.sql` 的 rollback、commit、total、log count 輸出。
6. `schedule_analyzer.py` 的五組輸出，以及一項程式模型限制。
7. 一段修正前後的錯誤敘述，例如將「snapshot 一定 serializable」改成有條件且可
   查核的說法。

## 12. 課後接續與下一章

課後完成 Practice 3、4、5、7，並將 `schedule_examples.json` 新增一個自訂
schedule。下一章會把本章的需求落實為 shared/exclusive locks、lock
compatibility、two-phase locking、deadlock handling 與 multiversion 的基本規則。

## 本章總結

- Transaction 是包含多個 data operations 的執行單位；ACID 分別約束完整性、規則
  維持、並行可見性與 committed result 的保存。
- Precedence graph acyclic 當且僅當該 schedule conflict serializable；小型例子可由
  conflicts 手工建立 graph。
- Recoverable 與 cascadeless 關心 read-from dependency 的 commit/read order，並非
  serializability 的別名。
- 較弱 isolation levels 提高 concurrency 的空間，也留下不同 anomalies；phantom
  需要考慮 predicate matching set。
- SQL transaction boundary 與 isolation 行為必須依實際 DBMS/driver 驗證，不能只
  靠相同的 isolation level 名稱推論。
