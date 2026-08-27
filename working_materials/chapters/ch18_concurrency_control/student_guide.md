# Chapter 18 Concurrency Control

## 核心問題

Chapter 17 說明正確的 concurrent schedule 應符合 serializability 與
recoverability。本章改問：DBMS 實際用什麼規則限制 operations，使不正確的
schedule 不會發生？本課聚焦 shared/exclusive locks、two-phase locking、deadlock
handling。Multiversion與snapshot isolation作課後延伸。

## 與前後章的關係

- Chapter 17 的 conflict、precedence graph、cascadelessness 是本章判讀 lock schedule
  的基礎。
- 本章暫時忽略 system failure，專注於 concurrent transactions 的互動。
- Chapter 19 會加入 log、undo、redo 與 crash recovery。

## 先備知識

你應能讀懂 `r1(A)`、`w2(B)`、`c1` 等 schedule 記號，並能由 conflict edges 判斷
小型 precedence graph 是否有 cycle。

## 學習目標

完成本章後，你應能：

1. 依 shared/exclusive lock compatibility matrix 判斷 lock request 應 grant 或 wait。
2. 解釋 growing phase、shrinking phase、lock point 與 basic two-phase locking (2PL)。
3. 分辨 basic與strict 2PL的lock-release規則。
4. 由 blocked lock requests 建立 wait-for graph，判斷 deadlock，並說明 recovery
   需要選擇 victim。
5. 說明 deadlock prevention、detection/recovery、timeout 的基本差異。

## 授課摘要

本章與 Chapter 19 共用一個教學週次。課堂完成locks、2PL及deadlock的共同核心，
再連接Chapter 19的failure與recovery：

| 教學內容 | 完整範例與練習 | 學習證據 |
|---|---|---|
| S/X locks與compatibility | 判斷lock request應grant或wait | compatibility判斷與理由 |
| basic/strict 2PL | 比較符合與違反2PL的lock sequences | sequence分類與修正 |
| wait-for graph與deadlock | 建立cycle並說明victim選擇的影響 | graph、cycle與處理理由 |

Multiversion visibility、snapshot isolation與write skew保留完整閱讀及範例，但屬於
課後延伸，不列入Exam 3主要操作題。

---

## 1. Shared 與 Exclusive Locks

Lock 是 DBMS 控制 concurrent access 的一種機制。Transaction 取得適當 lock 後才可
對 data item 執行 operation；若現有 locks 不相容，request 必須等待。

- **Shared lock (S)**：transaction 可 read item，但不能用此 lock write item。
- **Exclusive lock (X)**：transaction 可 read 及 write item。

### 1.1 Compatibility matrix

| Existing lock | Request S | Request X |
|---|---:|---:|
| S | grant | wait |
| X | wait | wait |

`S` 與 `S` 相容，因此多個 readers 可同時讀同一 item。只要另一個 transaction 已持有
`X`，任何 `S` 或 `X` request 都不相容；若已有一個或多個 `S`，新的 `X` 也必須
等待。

Compatibility 只比較不同 transactions 在同一 item 的 lock modes。它不表示
application logic 正確，也不單獨決定 lock 應持有多久。

### Worked example 1：兩個 readers 與一個 writer

```text
1. T1 requests S(A) -> grant
2. T2 requests S(A) -> grant
3. T3 requests X(A) -> wait for T1 and T2
4. T1 releases S(A)
5. T2 releases S(A) -> T3 can now receive X(A)
```

T3 不能在 step 4 立刻取得 `X(A)`，因為 T2 仍持有 `S(A)`。判斷 request 時要檢查
所有 incompatible holders，不是只找最早的一個。

### Practice 1

目前 `T1:S(A)`、`T2:S(A)`、`T3:X(B)`。判斷下列 requests：

1. `T4:S(A)`
2. `T4:X(A)`
3. `T4:S(B)`
4. `T4:X(C)`，且 C 沒有任何 holder

**檢查依據：** 依序為 grant、wait、wait、grant；每題都要指出同一 item 的現有
holder 與 compatibility matrix 格子。

---

## 2. Two-Phase Locking

只要求 operation 前有 lock 還不夠；若 transaction 太早 unlock，另一個 transaction
可能讀到不一致的中間狀態。Locking protocol 因此規定何時可取得與釋放 locks。

Basic **two-phase locking (2PL)** 分成：

1. **Growing phase**：可以取得新 locks，不可釋放 lock。
2. **Shrinking phase**：可以釋放 locks，不可再取得新 lock。

Transaction 取得最後一個 lock 的位置稱為 **lock point**。Basic 2PL 產生的 legal
schedules 都是 conflict serializable，transactions 可依 lock points 排出一個
serialization order。這不表示每個 conflict-serializable schedule 都能由 2PL 產生。

### Worked example 2：符合與違反 2PL

```text
P1: lock-X(A), lock-S(B), unlock(A), unlock(B), commit
P2: lock-S(A), unlock(A), lock-X(B), commit
```

- `P1` 符合 basic 2PL：取得完兩個 locks 後才開始 unlock。
- `P2` 違反 basic 2PL：釋放 A 後已進入 shrinking phase，卻又要求 `X(B)`。

2PL 仍可能 deadlock，因為兩個 transactions 都可在 growing phase 持有一個 lock，
同時等待另一個 lock。

### 2.1 Strict 2PL與rigorous 2PL（rigorous作概念延伸）

| Protocol | Release rule | 主要結果 |
|---|---|---|
| Basic 2PL | shrinking phase 可逐步釋放 locks | conflict serializable；仍可能 cascading rollback |
| Strict 2PL | 所有 X locks 保留到 commit/abort | recoverable 且避免 cascading rollback |
| Rigorous 2PL | 所有 S 與 X locks 保留到 commit/abort | 可依 commit order serialization |

Strict 2PL 的重點是未 committed writes 仍受 `X` lock 保護。若只保留 `S` 但提早
釋放 `X`，就沒有達成這項要求。

### Worked example 3：basic 但不 strict

```text
lock-X(A), lock-S(B), unlock(A), unlock(B), commit
```

這個 sequence 符合 basic 2PL，因為 unlock 後沒有再取 lock；但 `X(A)` 在 commit
前已釋放，所以不符合 strict 2PL。

### Practice 2

分析：

```text
lock-S(A), lock-X(B), unlock(A), commit
```

1. 是否符合 basic 2PL？
2. 是否符合 strict 2PL？
3. 是否符合 rigorous 2PL？

**檢查依據：** basic 為 Yes；strict 為 Yes，因為 `X(B)` 仍保留到 commit；
rigorous 為 No，因為 `S(A)` 提前釋放。不要把 strict 誤寫成「所有 locks 都保留」。

---

## 3. Deadlock 與 Wait-For Graph

Deadlock 是一組 transactions 互相等待，集合中的每一個 transaction 都無法繼續。
以 locks 表示：

```text
1. T1 gets X(A)
2. T2 gets X(B)
3. T1 requests X(B) -> waits for T2
4. T2 requests X(A) -> waits for T1
```

### 3.1 Wait-for graph

Wait-for graph 的 vertex 是 transaction。若 `Ti` 正等待 `Tj` 釋放 incompatible lock，
畫 edge `Ti -> Tj`。上述例子得到：

```text
T1 -> T2
T2 -> T1
```

Wait-for graph 有 cycle，當且僅當目前存在 deadlock。這裡的 edge 方向是「等待者指向
holder」，不要和 Chapter 17 precedence graph 的 conflict order 混在一起。

### 3.2 Handling choices

- **Prevention**：讓 deadlock 不可能形成。例如所有 transactions 依共同 item order
  取得 locks；實務限制是程式可能事前不知道完整 access set。
- **Detection and recovery**：允許等待，維護 wait-for graph 並找 cycle；偵測到後選
  一個或多個 victims rollback，使 locks 釋放。
- **Timeout**：等待超過門檻就 rollback。它容易實作，但長等待不一定是 deadlock，
  所以可能造成不必要 rollback；門檻太長也會延後真正 deadlock 的處理。

Victim selection 可考慮已執行工作、持有 locks、rollback 影響與過去被選次數。
若同一 transaction 一再成為 victim，會發生 starvation；retry 也應避免立即無限重跑。

### Worked example 4：用共同順序預防

若規定所有 transactions 都只能依 `A` 再 `B` 取得 locks，T1 與 T2 都不能先持有
`B` 再要求 `A`。前述 `T1 waits for T2` 且 `T2 waits for T1` 的 cycle 就無法以同樣
方式形成。代價是程式與資料存取必須遵守共同順序。

### Practice 3

目前 edges：`T1->T2`、`T2->T3`、`T3->T1`、`T4->T2`。

1. 哪些 transactions 在 deadlock cycle 中？
2. Rollback T4 能否打破 cycle？
3. Rollback T2 後哪些 cycle edges 會失效？

**檢查依據：** Cycle 是 T1、T2、T3；T4 不在 cycle，rollback T4 不能打破該
cycle；rollback T2 並釋放 locks 後，與 T2 相關的等待關係需重算，原 cycle 被打破。

---

## 4. Multiversion Schemes（課後延伸）

Locking 可能讓 reader 等待 writer。Multiversion concurrency control 保存同一 data
item 的多個 versions；每次成功 write 建立新 version，read 依 transaction timestamp
選擇適當版本。具體 protocol 必須規定 version selection、write conflicts、commit、
rollback 與舊版本回收，不能只靠「保留歷史值」宣稱 serializable。

### Worked example 5：version visibility

Data item Q 有三個 committed versions：

| Commit timestamp | Value |
|---:|---:|
| 10 | 100 |
| 20 | 90 |
| 30 | 120 |

若規則是讀取 `commit timestamp <= transaction start timestamp` 中最新的 version：

- Start 15 的 reader 看到 timestamp 10、value 100。
- Start 25 的 reader 看到 timestamp 20、value 90。
- Start 35 的 reader 看到 timestamp 30、value 120。

較早 reader 可繼續讀舊 committed version，不必因新 version 出現就改變同一 snapshot
中的結果。代價包括 version storage、查找與 garbage collection。

### Practice 4

新增 `Q@40=80`。Start timestamps 19、20、39、40 各看到哪個 value？

**檢查依據：** 依序 100、90、120、80；`<=` 的 boundary 會讓 start 20 看見
timestamp 20 的 version。

---

## 5. Snapshot Isolation 與 Write Skew（課後延伸）

Snapshot isolation 是 multiversion 方法。Transaction 讀取開始時可見的 committed
snapshot；concurrent transactions 後來 committed 的 updates 不會突然出現在該
snapshot。Readers 因此通常不必等待 writers。

Update transaction 仍需 validation。以 first-committer-wins 的基本想法為例：若
concurrent transaction 已寫入目前 transaction 也打算寫的 item，後者不能直接一起
commit。這可防止兩個 transactions 對同一 item 的 lost update。

但是只檢查 overlapping write sets 不保證 serializability。兩個 transactions 可能讀
相同條件、更新不同 items，最後共同破壞 constraint，這是 **write skew**。

### Worked example 6：兩個帳戶的 write skew

Constraint：`checking + savings >= 0`。初始值為 100 與 200。

- T1 讀 snapshot `(100, 200)`，判斷可從 checking 提 200，準備寫
  `checking=-100`。
- T2 也讀同一 snapshot，判斷可從 savings 提 200，準備寫 `savings=0`。
- T1 write set 是 `{checking}`，T2 是 `{savings}`，沒有 write-write overlap。
- 若兩者都 commit，final sum 是 -100，constraint 被破壞。

每個 transaction 對自己的 snapshot 單獨檢查都得到 final sum 100，但 combined
result 不等價於任何合法 serial execution。Snapshot isolation 因此不能直接當成
serializable isolation。Serializable snapshot isolation 或應用程式明確建立必要
conflicts 是不同的進階作法，本課不教其完整演算法。

### Practice 5

將兩個 transactions 都改成更新同一 row `account_summary.total`。這會對
first-committer-wins 的判斷產生什麼差異？

**檢查依據：** Write sets 現在重疊；其中一個 concurrent writer 通過 commit 後，
另一個應被 validation 拒絕或 rollback。這只能回答該 protocol 的 write-write
conflict，不能由此推廣成所有 application constraints 都安全。

---

## 6. 執行活動

### 6.1 Lock simulator

先預測，再執行：

```powershell
py -3 lock_simulator.py lock_scenarios.json
```

| Scenario | 主要預期 |
|---|---|
| `compatible_reads` | T1/T2 都取得 S(A)，無 wait |
| `writer_waits` | T2 的 X(A) 等 T1 commit 後取得 |
| `deadlock` | edges `T1->T2`、`T2->T1`，找到 cycle |
| `violates_two_phase` | `two_phase=false` |
| `basic_two_phase_not_strict` | `two_phase=true`、`strict_two_phase=false` |

程式只模擬 S/X compatibility、FIFO waiting 的簡化版本、2PL release rule 與
wait-for graph。它沒有 lock upgrade、multiple granularity、predicate/index locks、
DBMS scheduler、failure recovery 或 transaction SQL semantics。

### 6.2 Multiversion demo（課後延伸）

```powershell
py -3 mvcc_demo.py
```

核對三個 readers 的 visible version，再核對 write-skew output：

```text
both_pass_write_write_check = true
constraint_sum_nonnegative = false
final = {checking: -100, savings: 0}
```

這是由明示規則計算的 counterexample，不是對特定 DBMS snapshot implementation 的
實測。

---

## 7. 常見錯誤與反例

1. **S lock 表示只能有一個 reader。** 反例是 S/S compatible。
2. **X lock 只排斥其他 writers。** X 也排斥其他 transactions 的 S requests。
3. **2PL 表示 transaction 同時只能持有兩個 locks。** Two-phase 指取得與釋放的兩個
   phases，不是 lock 數量。
4. **Basic 2PL 不會 deadlock。** 兩個 transactions 可在 growing phase 互等。
5. **Graph 有 wait edge 就是 deadlock。** 必須有 cycle；單向等待不是 deadlock。
6. **Timeout 一定表示偵測到 deadlock。** Timeout 也可能只是正常長等待。
7. **Strict 2PL 保留所有 locks。** Strict 要求 X locks 到 transaction end；rigorous
   才要求所有 locks。
8. **MVCC 一定 serializable。** 必須看 version selection 與 validation protocol；
   snapshot isolation 可能有 write skew。

## 8. 課堂討論

### Discussion A

API 遇到 deadlock victim error 時，應直接向使用者顯示失敗，還是自動 retry？

**回答依據：** 至少討論 transaction 是否可安全重試、是否可能重複外部 side
effect、最大 retries、backoff、紀錄與最終失敗處理。只有「retry 就好」不完整。

### Discussion B

一個只讀月報要掃描大量 rows；同時有短交易更新少量 rows。你會先研究 locking 還是
multiversion 方案？

**回答依據：** 比較 reader 是否阻擋 writer、可接受 snapshot staleness、version
storage、DBMS guarantee 與 write workload；答案需提出要量測或查證的證據。

## 9. 個人應保存的學習證據

1. 完成的 S/X compatibility matrix 與四題理由。
2. 一個 basic 2PL 與一個 2PL violation sequence。
3. Deadlock wait-for graph、cycle 與 victim 說明。
4. `lock_simulator.py` 五組 output。
5. 四個 timestamp boundary 的 version visibility 計算。
6. `mvcc_demo.py` write-skew output 與「為何無 write overlap 仍不安全」的解釋。
7. 一項 simulator 沒有處理、因此不能推廣到真實 DBMS 的限制。

## 10. 課後接續與下一章

課後修改 `lock_scenarios.json`，加入一個三個 transactions、無 cycle 但有兩層等待
的 scenario，並畫出 wait-for graph。下一章會說明 transaction 因 deadlock 或 crash
abort 時，recovery system 如何利用 log、undo 與 redo 恢復 atomicity 與 durability。

## 本章總結

- S/S compatible；任何涉及 X 的不同 transaction lock pair 都不相容。
- Basic 2PL 以 growing/shrinking phases 保證 conflict serializability，但仍可能
  deadlock 與 cascading rollback。
- Strict 2PL 保留 X locks 到 transaction end；rigorous 2PL 保留所有 locks。
- Wait-for graph cycle 表示 deadlock；處理方式必須考慮 rollback cost 與 starvation。
- Multiversion reads 依 timestamp 選擇 committed version，可降低 reader/writer
  blocking，但 protocol 仍要處理 writes、版本回收與 correctness。
- Snapshot isolation 可防止若干 anomalies，卻可能因 write skew 產生
  nonserializable result。
