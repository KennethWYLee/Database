# Chapter 19 Recovery System

## 核心問題

Transaction 已顯示成功，但更新後的 data page 尚未寫回 disk；或未 committed
transaction 的 data page 已先寫回 disk。此時 system crash，DBMS 如何同時做到：

- 不遺失 committed transaction 的效果；
- 不保留 incomplete transaction 的效果？

答案不能只靠查看 crash 後的 database values，因為相同 values 可能由不同執行歷程
形成。Recovery system 必須在正常執行時先保存足以判斷與重建的 log information。

## 與前章的關係

- Chapter 17 定義 atomicity 與 durability。
- Chapter 18 說明 strict 2PL 將 X locks 保留到 transaction end；本章的簡化 recovery
  algorithm 假設 uncommitted update 不會先被另一個 transaction 覆寫。
- 本章處理 transaction failure、system crash 與 storage loss 後的恢復。

## 先備知識

你應能追蹤 transaction state、`COMMIT`、`ROLLBACK`、buffer 與 disk 的差別，並能
依序閱讀一組 transaction events。

## 學習目標

完成本章後，你應能：

1. 分辨 logical transaction error、system transaction error、system crash 與 disk
   failure。
2. 比較 volatile、non-volatile 與 stable storage 在 recovery model 中的角色。
3. 解讀 start、update、commit、abort log records，以及 old/new values 的用途。
4. 解釋 write-ahead logging (WAL) 的 data-flush rule 與 commit rule。
5. 由 log 判斷 committed 與 incomplete transactions，執行簡化 redo/undo。
6. 說明 checkpoint 如何縮小 restart recovery 需要處理的 log 範圍。
7. 解釋 archival backup 與 post-backup log 如何一起處理 non-volatile storage loss。

## 授課摘要

本章與 Chapter 18 共用一個教學週次，使用同一組transaction events連接lock、
failure與recovery：

| 教學內容 | 完整範例與練習 | 學習證據 |
|---|---|---|
| failure classes與必要的recovery input | logical error、deadlock victim、system crash與disk failure分類 | failure classification與理由 |
| log records、WAL、commit | valid與invalid event timelines | WAL判斷與修正 |
| redo、undo與basic checkpoint | crash時混合data pages的log案例 | redo/undo判斷 |
| backup加後續log | storage loss後的restore sequence | restore順序與限制 |

完整recovery algorithms、fuzzy checkpoint、ARIES及production administration作課後
延伸，不列入Exam 3主要操作題。

---

## 1. Failure Classification

不同 failure 破壞的資訊不同，因此需要不同 recovery input。

| Failure | 本章定義 | Example | 主要 recovery direction |
|---|---|---|---|
| Logical transaction error | transaction 因自身條件無法正常繼續 | bad input、找不到必要資料、resource limit | abort/rollback 該 transaction |
| System transaction error | DBMS 因系統狀態終止 transaction，但之後可能重跑 | deadlock victim | rollback，符合條件時 retry |
| System crash | volatile storage 遺失、transaction processing 停止；在 fail-stop assumption 下 non-volatile storage 未損壞 | power loss、DBMS/OS crash | 使用 stable log 做 restart recovery |
| Disk failure | non-volatile blocks 部分或全部遺失 | device failure、無法讀取且 checksum 顯示損壞 | restore backup，再使用 log 推進 |

Fail-stop assumption 是本章 system-crash algorithm 的條件，不是「所有 crash 都不會
corrupt disk」的自然定律。若 non-volatile data 本身遺失，必須改用 disk-failure
recovery path。

### Worked example 1：同樣是失敗，不同處理

1. Transaction 因 `CHECK (balance >= 0)` 失敗：logical transaction error。
2. DBMS 偵測 deadlock 並選 T2 為 victim：system transaction error。
3. Server 斷電，但 data disk 與 stable log 仍可讀：在 fail-stop assumption 下的
   system crash。
4. Data disk 無法讀取部分 blocks：disk failure，restart log alone 不足以還原遺失的
   base blocks。

### Practice 1

將下列情境分類，並寫出遺失的是 transaction progress、volatile contents，還是
non-volatile data：

1. 使用者輸入不存在的 account id，程式主動 rollback。
2. DBMS process crash 後重新啟動，disk blocks 完整。
3. SSD controller failure 使 database file 無法讀取。
4. Lock wait 形成 cycle，T7 被 abort。

**檢查依據：** 依序是 logical transaction error、system crash、disk failure、
system transaction error；理由必須指出 recovery 可依賴哪些持久資料。

---

## 2. Storage Assumptions

- **Volatile storage**：system crash 時內容遺失，例如 main memory。
- **Non-volatile storage**：一般 system crash 後仍保留，例如 disk/flash，但 device
  failure 仍可能使資料遺失。
- **Stable storage**：理論上不遺失；實務以獨立 failure modes 的多份 non-volatile
  copies、受控寫入與錯誤偵測近似。

Database blocks 可先在 memory buffer 被修改，再於不同時間 output 到 disk。SQL
statement 的 `write(X)` 改到 buffer，不代表包含 X 的 physical block 已寫回 disk。
這個時間差同時造成兩種 recovery need：

1. Committed update 仍只在 volatile buffer，crash 後需要 **redo**。
2. Uncommitted update 已 output 到 disk，abort/crash 後需要 **undo**。

### Worked example 2：為何只看 disk values 不夠

轉帳把 A 由 1000 改成 950、B 由 2000 改成 2050。Crash 時 disk 是
`A=950, B=2000`。這可能表示只寫出 A 的部分 transaction，也可能原始 database
本來就是這組 values。沒有 log，就無法由 values 單獨判斷 transaction 是否開始、
是否 commit，以及 old/new values。

### Practice 2

解釋下列兩句為何不能互相替代：

1. `write(B)` 已修改 buffer block。
2. `output(BB)` 已把 containing block 寫回 disk。

**檢查依據：** 答案需明確指出 memory/disk location 與 crash survival；只說「一個
比較快」不完整。

---

## 3. Log Records

Log 是依序記錄 database update activities 的 records。基本形式：

```text
<T0 start>
<T0, A, 1000, 950>
<T0, B, 2000, 2050>
<T0 commit>
```

Update record `<Ti, X, old, new>` 包含：

- transaction identifier；
- data-item identifier；
- old value，供 undo 使用；
- new value，供 redo 使用。

`<Ti start>` 表示 Ti 開始；`<Ti commit>` 表示 commit record 已進入 log；
`<Ti abort>` 表示 rollback 已完成。Log records 可以交錯，因為多個 transactions
共用 system log。

### 3.1 Immediate 與 deferred modification

- **Immediate modification**：transaction commit 前，updated buffer/data block 可能
  已 output；因此要能 undo old value，也要能 redo new value。
- **Deferred modification**：直到 commit 才把 transaction updates 套用到 database；
  可以減少 undo need，但需要保存 local updates，且讀取自己更新過的 item 時要讀
  local copy。

本章程式使用簡化的 immediate-modification model。

### Worked example 3：old 與 new 各救哪個問題

Log 有 `<T1, C, 700, 600>`：

- T1 未 commit 而 crash，若 disk 已是 600，undo 將 C 設回 old value 700。
- T1 已 commit 而 crash，若 disk 仍是 700，redo 將 C 設成 new value 600。

Redo/undo 是設定記錄中的值，不是重新執行原 application code。後者可能讀到不同
資料、呼叫外部服務或產生不同結果。

### Practice 3

給定 `<T5, inventory, 12, 9>`：

1. T5 incomplete 時應使用哪個 value？
2. T5 committed 但 data page 未寫出時應使用哪個 value？

**檢查依據：** 依序是 undo to 12、redo to 9；每題都需說明 transaction status。

---

## 4. Write-Ahead Logging 與 Commit

Log 可先留在 memory log buffer 以合併 I/O，但 crash 會遺失尚未 force 到 stable
storage 的部分。Write-ahead logging (WAL) 因此要求重要順序：

1. **Data-flush rule**：包含 update 的 data block 寫到 non-volatile database 前，該
   update 所需的 log information 必須先到 stable storage。
2. **Commit rule**：transaction 進入 committed state 前，該 transaction 的所有較早
   log records 及 commit record 必須到 stable storage。

WAL 的名稱是「log 在 data 前」，不是「所有 data pages 都必須在 commit 前寫完」。
No-force policy 允許 committed data pages 之後再寫，因為 stable log 提供 redo
information。

### Worked example 4：valid timeline

```text
1. create <T0, A, 1000, 950> in log buffer
2. force log through this update record
3. flush data block containing A
4. create <T0 commit>
5. force log through commit record
6. acknowledge commit
```

若交換 step 2/3，data-flush rule 被破壞：uncommitted data 已在 disk，卻可能沒有
stable old value 可 undo。若交換 step 5/6，系統可能對外承諾 commit，但 crash 後
stable log 沒有 commit evidence。

### Practice 4

修正 timeline：

```text
create update log -> flush data -> create commit log -> acknowledge commit -> force log
```

**檢查依據：** 至少改成 `create update log -> force update log -> flush data -> create
commit log -> force through commit -> acknowledge commit`。Force 可以較早，但不能
晚於它保護的 data flush 或 commit acknowledgement。

---

## 5. Restart Recovery：Redo 再 Undo

本課使用教科書的簡化 repeating-history algorithm：

1. 從最近 checkpoint forward scan。
2. Redo phase 依 log order 重放 update 與 redo-only records，同時建立
   `undo-list`。
3. 遇到 `<Ti start>` 就把 Ti 加入 `undo-list`；遇到 `<Ti commit>` 或
   `<Ti abort>` 就移除。
4. Redo 結束後，`undo-list` 中是 crash 時 incomplete transactions。
5. Undo phase backward scan，只對 `undo-list` transaction 的 update 使用 old value。
6. Undo 每個 update 時寫 redo-only compensation record；找到 transaction start 後寫
   abort record 並從 `undo-list` 移除。

Redo incomplete transaction 再 undo 看起來多做一次，但它先把 disk 重建到 crash 前
最後 stable log 所描述的狀態，再以一致的 backward order rollback incomplete
transactions。這是 **repeating history** 的基本想法。

### Worked example 5：混合 data pages at crash

Crash 時 disk：

```text
A=950, B=2000, C=600
```

從 checkpoint 後的 log：

```text
<T0 start>
<T0, A, 1000, 950>
<T0, B, 2000, 2050>
<T0 commit>
<T1 start>
<T1, C, 700, 600>
-- crash, no T1 commit/abort
```

Redo forward：A=950、B=2050、C=600。Scan 結束時 T0 已 commit，所以不在
`undo-list`；T1 incomplete，留在 `undo-list`。Undo backward 將 C 設回 700，並
產生 redo-only `<T1,C,700>` 與 `<T1 abort>`。Final database：

```text
A=950, B=2050, C=700
```

### Practice 5

若再加入：

```text
<T2 start>
<T2, A, 950, 900>
<T2 commit>
```

且 crash 在 T2 commit record stable 之後，final A 應是多少？

**檢查依據：** Redo T2 後 A=900，T2 不在 undo-list，因此 final A=900。Commit
status 來自 stable log，不由 crash 時碰巧看到的 page value決定。

---

## 6. Checkpoint

若每次 restart 都從 log 最前端掃描，時間會隨系統歷史增加。Checkpoint 記錄一個可
縮小 recovery scan 的位置與當時 active transactions。教科書的簡化 checkpoint：

1. Force current log records。
2. Output modified buffer blocks。
3. Force `<checkpoint L>`，其中 L 是當時 active transactions。

Recovery 找到最近 checkpoint 後，只需考慮 L 中的 transactions 與之後開始的
transactions；但若 L 中某 transaction 在 checkpoint 前就開始，undo 仍可能需要其
較早 update records。

Checkpoint 不是 backup。它主要縮短 log recovery scan，並假設 database storage
仍存在；archival backup 則提供 data blocks 遺失後可還原的 base copy。

### Worked example 6

Checkpoint 的 `L={T8}`。T7 在 checkpoint 前已 commit；T8 在 checkpoint 前開始、
之後沒有 commit；T9 在 checkpoint 後開始並 commit。Recovery 可以忽略 T7，redo
T9，undo T8；為了 undo T8，可能需要往 checkpoint 前找 T8 的 update records。

### Practice 6

說明「有 checkpoint，所以不需要 log」哪裡錯。

**檢查依據：** 必須指出 checkpoint 後的 committed updates 需要 redo，當時 active
transactions 可能需要 checkpoint 前的 old values 做 undo。

---

## 7. Backup 與 Log-Based Recovery

Disk failure 遺失 non-volatile database blocks 時，restart log 不能憑空提供所有 base
rows。基本順序是：

1. 由最近 archival backup/dump restore database base copy。
2. 取得 backup 之後仍保存的 log。
3. 依 recovery rule 套用需保留的後續 updates，使 database 前進到較新的 consistent
   state。

因此 backup 與 log 解決不同時間範圍：backup 限制必須從多舊的 base 開始；log
決定 backup 後能前進到哪裡。只有 backup 可能遺失 backup 後的 committed work；
只有 post-backup log 而沒有可讀 base data，也未必能重建完整 database。

Remote backup/replica 可縮短 primary failure 後的 takeover time，但還涉及 failure
detection、control transfer、log synchronization 與 durability tradeoff。本課只保留
這層關係，不教 remote backup protocol 細節。

### Worked example 7

Backup：`A=1000, B=2000, C=700`。Backup 後 stable committed log 有 T0 的 A/B
轉帳。Restore backup 後 redo T0，得到 `A=950, B=2050, C=700`，與 Worked
example 5 的 restart result 一致。

### Practice 7

回答兩題：

1. 每日 backup 在 00:00 完成，12:00 disk failure；11:55 的 committed transaction
   要靠哪一份資料恢復？
2. 最近 backup 損壞但 log 完整，是否已足以保證完整 restore？

**檢查依據：** 第 1 題需要 00:00 backup 加上之後包含該 commit 的 log；第 2 題
答案是不能由此保證，因為 log 的 update records 不等於完整可用 base database。

---

## 8. 執行活動

### 8.1 Recovery simulator

先手算 Worked example 5，再執行：

```powershell
py -3 recovery_simulator.py recovery_case.json
```

核對：

```text
incomplete_after_redo = [T1]
redo: T0.A=950, T0.B=2050, T1.C=600
undo: T1.C=700
final_database = {A:950, B:2050, C:700}
backup_plus_committed_log = {A:950, B:2050, C:700}
```

Simulator 假設 physical update records 可透過「設定成 old/new value」重複執行，且
同一 item 不會被後續 uncommitted transaction 覆寫後又需要複雜 logical undo。它
沒有 ARIES LSN/PageLSN、dirty-page table、fuzzy checkpoint、logical undo 或
parallel recovery。

### 8.2 WAL checker

```powershell
py -3 wal_checker.py wal_scenarios.json
```

預期：

- `valid`: valid。
- `invalid_data_before_log`: event 2 違反 data-flush order。
- `invalid_commit_before_force`: event 4 在 commit log force 前 acknowledgement。

Checker 使用單一遞增 LSN timeline，沒有模擬 log blocks、concurrent flush、group
commit 或 partial disk writes。

---

## 9. 常見錯誤與反例

1. **System crash 與 disk failure 相同。** 前者在 fail-stop assumption 下保留
   non-volatile contents；後者遺失 blocks。
2. **`COMMIT` 表示所有 data pages 已在 disk。** No-force recovery 可先持久化 log，
   pages 之後再寫。
3. **WAL 表示 data 一定先寫。** 正好相反，recovery information 必須在相關 data
   page 前到 stable storage。
4. **Committed transaction 只需 redo 未寫出的 page。** 簡化 algorithm 可重做所有
   relevant updates；設定同一 new value 不改變結果。
5. **Incomplete transaction 只需忽略。** 若其 page 已在 disk，必須 undo old value。
6. **Redo 只處理 committed transactions。** Repeating-history redo 也重放
   incomplete/aborted history，之後再 undo incomplete transactions。
7. **Checkpoint 等於 backup。** Checkpoint 縮小 restart log work；backup 提供 storage
   loss 的 base copy。
8. **有 backup 就不需要測 restore。** 無法讀取、缺 log 或順序錯誤的 backup plan
   不能由「檔案存在」證明可恢復。

## 10. 課堂討論

### Discussion A

API 已對付款回覆 success，但 commit record 尚未 stable，接著 server crash。這是
哪一項 contract 被破壞？

**回答依據：** 連結 commit acknowledgement、stable commit record 與 durability；
不能只說「系統壞了」。

### Discussion B

團隊每天產生 backup，但從未做 restore test。可以把 recovery plan 評為完成嗎？

**回答依據：** 至少列出 backup 可讀性、base/log 配對、restore sequence、目標
consistent point、驗證 queries 與完成時間等可檢查證據。

## 11. 個人應保存的學習證據

1. 四個 failure classification 答案與 storage-loss 理由。
2. 一個 update log record 的 old/new value 解釋。
3. Valid 與兩個 invalid WAL timelines。
4. Worked example 5 的 redo/undo 手算表。
5. `recovery_simulator.py` 與 `wal_checker.py` outputs。
6. Checkpoint 與 backup 的差異說明。
7. 一項 simulator 未處理、因此不能推廣到 production DBMS 的限制。

## 12. 課後接續

修改 `recovery_case.json`，新增一個 committed T2 與一個 incomplete T3，預測 final
database 後再執行。有興趣的學生可選一個server DBMS查核其WAL/log名稱、backup
format、point-in-time recovery所需檔案、restore command與驗證方法。這項查核是
課後延伸，不屬於SQLite課堂核心，也不列入Exam 3主要操作題。

## 本章總結

- Recovery algorithm 要在正常執行時先保存資訊，也要在 failure 後重建狀態。
- Update log 的 old value 支援 undo，new value 支援 redo；stable commit record 是
  durability 判斷的重要界線。
- WAL 要求 recovery log information 先於相關 data page output，且 transaction 的
  log records 先於 commit acknowledgement 持久化。
- 簡化 restart recovery forward redo history，再 backward undo incomplete
  transactions；checkpoint 縮小需處理的 log 範圍。
- Non-volatile storage loss 需要先 restore backup base，再用保存的 log 推進；backup
  與 log 缺一都可能無法達到目標 recovery point。
