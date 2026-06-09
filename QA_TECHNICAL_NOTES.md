# QA 技術筆記 — 踩坑紀錄

## 1. OCR 模板比對的 DPR 問題

**現象：** 相似度長期 < 0.5，比對失敗。  
**原因：** Selenium 截圖是物理像素（physical px），Windows 125% 縮放導致 DPR=1.25，截圖實際是 1685×1239，而模板是 CSS px 尺寸，兩者比例不符。  
**教訓：** 每次換機器或改 Chrome 設定前，先確認 `window.devicePixelRatio`，模板必須從**同一台機器、同一個 Selenium session** 截出來。

---

## 2. 模板必須從完全載入的頁面截

**現象：** 截出來的 logo 是灰色 skeleton 佔位符，不是正式 icon。  
**原因：** debug 截圖是在頁面 loading 中觸發的，`wait_for_page_load` 時間不夠。  
**正確做法：** 截模板時要先 `time.sleep(5~8)` 或等 network idle，確認頁面完全渲染再截。

---

## 3. 模板裁切邊界估錯

**現象：** 截出的 logo 只有半邊。  
**原因：** 用肉眼猜座標，沒有用像素分析確認邊界。  
**正確做法：** 用 numpy 找非背景色像素的 min/max 座標，再加 2px padding，不要猜。

```python
dark = gray < 220
y_min, y_max = np.where(np.any(dark, axis=1))[0][[0, -1]]
x_min, x_max = np.where(np.any(dark, axis=0))[0][[0, -1]]
```

---

## 4. 彩色 vs 灰階比對

**現象：** 灰階比對對顏色相近的背景容易誤判。  
**結論：** `ocr_helper.py` 已改成彩色比對（BGR）。模板必須是彩色 PNG，不能是灰階或 skeleton 截圖。  
**注意：** PIL 讀進來是 RGB，cv2 是 BGR，轉換用 `cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)`。

---

## 5. Mobile Emulation 與模板不符

**現象：** conftest.py 有 iPhone 12 Pro 模擬（3x DPR），但模板是從桌面截的，logo 形狀完全不同（桌面=小 icon，手機=大文字 wordmark）。  
**結論：** 規格沒有要求 mobile，已移除模擬器設定，改回桌面 Chrome。  
**教訓：** 新增或修改模擬設定時，所有 OCR 模板都要跟著重截。

---

## 6. 模板沒有進 git

**現象：** `assets/twitch_logo.png` 是 untracked，搞壞之後無法還原。  
**結論：** 所有 `assets/` 下的模板圖片都要 `git add` 並 commit。  
**檢查指令：** `git status assets/`

---

## 模板重截 SOP

1. 確認 `window.devicePixelRatio`
2. 用與測試相同的 Selenium 設定開瀏覽器
3. 導向目標頁面，等待 8 秒確保完全載入
4. `driver.save_screenshot('tmp.png')`
5. 用 numpy 找目標顏色像素邊界，加 2px padding 裁切
6. 確認截出的圖視覺正確後覆蓋 `assets/` 下對應檔案
7. 跑一次測試驗證相似度 ≥ 0.75
8. `git add assets/ && git commit`
