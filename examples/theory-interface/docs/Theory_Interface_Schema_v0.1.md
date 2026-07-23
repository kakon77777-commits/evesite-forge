# Theory Interface Schema v0.1
## 理論介面共同格式

**版本：** 0.1  
**日期：** 2026-07-23  
**定位：** 將理論內容轉換為公共門面、可操作摘要、正式模型、實驗、文件、限制與研究狀態的宣告式格式。

---

# 1. 核心命題

Theory Interface Schema 不規定理論本身，而規定理論如何被公開投影。

```text
Theory Source
    ↓
Theory Interface Schema
    ↓
Public Narrative
Operable Summary
Formal Model
Experiments
Documents
Limitations
Status
Roadmap
```

它是介於理論真源與公開介面之間的結構化中介層。

# 2. 最小結構

```json
{
  "project": {},
  "thesis": {},
  "evidence": {},
  "sections": [],
  "documents": [],
  "status": {
    "metrics": [],
    "roadmap": []
  }
}
```

# 3. 證據階層

```text
L0 概念敘述
L1 視覺比喻
L2 互動示範
L3 可重現模型
L4 系統性實驗
L5 外部驗證
L6 形式證明或穩健證據
```

# 4. v0.1 互動模組

- `none`：純文件型網站；
- `weighted-risk`：多參數加權、門檻、事件與歸因；
- `maturity-ladder`：成熟度、階段與治理責任。

# 5. 治理原則

1. Schema 是公開投影來源，不是理論本體的唯一真源。
2. 文件保留正式 Markdown、PDF 或其他權威版本。
3. 互動模組必須顯示證據級別與省略內容。
4. 介面完整不代表證據級別提高。
5. 網站可重新生成，但文件與版本歷史不得被抹除。
6. `limitations` 與 `status` 不得省略。
7. 視覺模板可以替換，理論資料結構應保持穩定。

# 6. v0.1 限制

- 只提供兩種互動模組；
- 尚未支援多語言路由；
- 尚未自動解析 Markdown；
- 尚未建立數學公式渲染；
- 尚未建立文件與網站差異檢查；
- 尚未整合 GitHub Releases、DOI 或部署流程。
