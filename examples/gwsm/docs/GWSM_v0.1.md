# 遊戲波動語意模型 0.1
## Game Wave Semantic Model 0.1 (GWSM)

**副標題：** 以波、狀態、關係、事件與自適應共同描述複雜遊戲世界  
**日期：** 2026-07-23  
**作者：** Neo.K（許筌崴）  
**組織：** EveMissLab／一言諾科技有限公司  
**狀態：** 公開研究草案  

---

# 摘要

傳統遊戲系統常以分離的旗標、計時器、狀態機與事件腳本描述角色、經濟、生態、派系、敘事與 NPC 行為。這些方法適合局部控制，卻難以表達跨系統的長期耦合、延遲、慣性、週期、共振、漂移與累積壓力。

GWSM 提出一套混合式世界語意模型：

```text
離散事實
+ 連續狀態
+ 波動通道
+ 關係耦合
+ 離散事件
+ 限制條件
+ 歷史記憶
+ 意圖
+ 自適應
```

它不主張一切皆為波。任務完成、物品數量、角色死亡與陣營歸屬仍應保留離散表示；市場需求、社會緊張、生態恢復、疲勞、士氣、謠言、敘事壓力與戰爭風險，則可用動態通道描述。

# 1. 核心架構

```text
Game Wave Language
        ↓
Game Semantic IR
        ↓
Wave-State Runtime
        ↓
Temporal / Event Database
        ↕
Human Control Surface
        ↕
AI Adaptation Layer
```

- **Language**：人類與 AI 編寫世界規則的表面語言。
- **Semantic IR**：保存狀態、波、關係、事件與限制的共同表示。
- **Runtime**：執行世界演化、耦合與事件觸發。
- **Database**：保存歷史、快照、事件來源、版本與隨機種子。
- **Control Surface**：讓設計者觀察、凍結、回放、分支與比較。
- **AI Layer**：先解釋與建議，再進入受限調整。

# 2. 十個最小語意結構

```text
Entity
Fact
State
Wave
Coupling
Event
Constraint
Timeline
Observation
Adaptation
```

## Entity

角色、派系、城市、區域、資源、建築、生物、任務、物品與制度等世界實體。

## Fact

離散且明確的事實，例如：

```text
alive = true
faction = north_union
quest_completed = false
item_count = 3
gate_state = closed
```

## State

可連續或分段改變的狀態，例如健康、疲勞、財富、穩定度與信任。

## Wave

用於描述週期、延遲、慣性、漂移、阻尼、記憶、調變與多尺度累積的動態通道。

```text
WaveChannel {
    value
    amplitude
    period
    phase
    envelope
    damping
    drift
    noise
    memory
    source
    target
    coupling
    bounds
    adaptation_policy
}
```

## Coupling

描述一個狀態或通道如何影響另一個通道，可包含權重、延遲、方向、門控與乘法交互作用。

## Event

當連續壓力跨越門檻並維持足夠時間後形成的離散結果。事件應包含門檻、持續時間、遲滯、冷卻與來源解釋。

## Constraint

限制合法世界狀態、數值範圍、互斥條件、資源守恆與設計者權限。

## Timeline

保存世界更新、快照、事件與版本的時間結構。

## Observation

把底層動態投影為設計者與 AI 可理解的圖表、警報、關係圖與歸因。

## Adaptation

描述允許 AI 調整什麼、調整幅度、目標、驗證條件、回滾點與批准者。

# 3. 混合世界更新

GWSM 的一般形式為：

\[
x_{t+1}=\Pi_{\mathcal C}\left[F(x_t,e_t,u_t)+\sum_i G_i(w_i(t),x_t,K_t)\right]
\]

其中：

- \(x_t\)：當前世界狀態；
- \(e_t\)：離散事件；
- \(u_t\)：玩家、設計者或 AI 輸入；
- \(w_i(t)\)：第 \(i\) 個動態通道；
- \(K_t\)：關係與耦合結構；
- \(\Pi_{\mathcal C}\)：將結果投影回合法世界狀態。

這個方程不是要求所有遊戲使用同一數學形式，而是用來明確表達：離散更新與動態通道應共同作用，最後仍須接受限制檢查。

# 4. 事件結晶

```text
event Riot {
    when resonance(
        food_shortage,
        public_anger,
        rumor_pressure
    ) > 0.82

    sustain 3 days
    hysteresis 0.08
    cooldown 30 days

    effects {
        city.stability -= 0.25
        guard.alert += 0.40
        spawn riot_groups
    }
}
```

門檻避免每個微小變化都生成事件；持續時間避免瞬間雜訊；遲滯避免在門檻附近反覆開關；冷卻避免同一事件無限制重複。

# 5. 表面語法

第一版可以保持傳統、可讀與可版本控制：

```text
wave faction_tension {
    base: 0.25
    amplitude: 0.40
    period: 90d
    phase: 12d
    damping: 0.03
    drift: adaptive
    bounds: [0, 1]
}

couple food_shortage -> faction_tension {
    weight: 0.65
    delay: 5d
    mode: multiplicative
}
```

波原生不等於波形字元語言；重點是動態傾向、節律、壓力、延遲與耦合成為一級語意。

# 6. 人類控制面板

控制面板分成三層：

1. **設計語意層**：戰爭傾向、經濟活力、生態恢復、敘事張力、NPC 自主性、世界變化速度。
2. **工程層**：振幅、週期、相位、阻尼、耦合矩陣、雜訊、延遲、積分步長、自適應率與穩定邊界。
3. **觀測層**：時間序列、波形、頻譜、相位關係、狀態空間、關係圖、事件來源、異常警報與短期分支。

必要控制包括：

```text
Freeze
Mute
Solo
Bound
Replay
Branch
Compare
Explain
Reset
Seed
Snapshot
Authority
```

其介面可借用數位音訊工作站的多軌、包絡、調變、自動化、靜音、獨奏與時間線概念，但每一軌代表世界狀態而非聲音。

# 7. AI 自適應階段

- **Level 0：** 人類完全控制，AI 僅觀察。
- **Level 1：** AI 解釋與提出建議。
- **Level 2：** AI 在明確範圍內自動調參。
- **Level 3：** AI 依高階目標進行受限適應。
- **Level 4：** AI 在沙盒分支提出結構修改，經驗證後才可合併。

AI 不應直接改寫即時世界的核心規則。所有修改必須保存原因、目標、前後差異、影響、版本、權限與回滾點。

# 8. 時序與事件資料庫

建議最小資料結構：

```text
entities
facts
state_channels
wave_channels
couplings
constraints
events
event_causes
snapshots
telemetry
adaptation_actions
model_versions
random_seeds
```

資料庫保存定義與歷史；Runtime 負責動態計算。兩者不可混為單一資料表或只靠即時記憶。

# 9. 第一個驗證世界

MVP 建議只包含：

- 一座城市；
- 三個派系；
- 食物與貨幣；
- 天氣與生態；
- 公共情緒；
- 十個世界事件；
- 五個具有意圖的 NPC。

需要提供：文字定義、控制面板、波與關係視圖、事件歷史、Replay／Branch，以及 AI 建議模式。

# 10. 成功條件

GWSM 0.1 的成功不是「做出完整遊戲引擎」，而是證明：

1. 不同世界系統能透過共同語意交換狀態；
2. 動態通道可以產生可解釋事件；
3. 設計者能回放並重現世界演化；
4. 控制面板能在不接觸底層數學時調整高階意圖；
5. AI 的修改可被限制、比較、批准與回滾。

# 11. 限制與非宣稱

GWSM 0.1 尚未證明它優於所有傳統遊戲架構，也未完成大型世界效能測試。網站中的波形與風險只屬於互動示範，不應被解讀為物理波、完整因果或社會預測。

# 結論

> 需要建立的不是一門單純「用波寫程式」的語言，而是一套讓遊戲世界以波、狀態、關係與事件共同演化的語意計算棧。表面可以保持傳統；底層必須能原生描述動態傾向、記憶、延遲、耦合與受限自適應。
