# TODOS

## 進行中


## 已完成
- [x] 專案初始化
- [x] 加入 retry() 遞迴方法到 BasePage（展示 Recursivity）
- [x] click_search() 與 select_first_streamer() 使用 retry()
- [x] 新增 tests/test_search_edge_cases.py（4 個 edge case 測試）
- [x] pytest.ini 新增 smoke / edge markers + --strict-markers
- [x] 補上 WAP 測試場景（mobile_driver fixture + MobileHomePage + test_wap_search.py）
- [x] 新增 Slow 3G CDP 網路限速測試（TestWAPNetwork）
- [x] home_page.py 重構：template 路徑移為 class attribute 支援子類別覆寫

## 已知問題
- WAP 測試在 assets/twitch_logo_mobile.png 與 assets/search_icon_mobile.png 尚未截圖前，若 CSS selector 也失效則 OCR 部分會 fail。
  解決方式：執行 `python utils/capture_mobile_templates.py --interactive` 生成 mobile template

## 已知問題


## 暫緩

