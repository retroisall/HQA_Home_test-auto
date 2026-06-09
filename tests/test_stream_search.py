from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.live_page import LivePage

SEARCH_QUERY = "StarCraft II"


class TestTwitchWAP:
    """WAP 端對端測試：使用 Chrome 手機模擬器操作 Twitch 搜尋與觀看直播。"""

    def test_search_and_view_starcraft_streamer(self, driver):
        """
        完整流程測試：
        1. 前往 Twitch
        2. 點擊搜尋圖示
        3. 輸入 StarCraft II
        4. 向下捲動兩次
        5. 選取一位直播主
        6. 等待頁面載入完成並截圖
        """
        # Step 1 & 2 — 前往首頁並點擊搜尋
        home = HomePage(driver)
        home.open().click_search()

        # Step 3 — 輸入搜尋關鍵字
        search = SearchPage(driver)
        search.dismiss_cookie_banner()
        search.search_for(SEARCH_QUERY)

        # Step 4 — 向下捲動兩次
        search.scroll_down_twice()

        # Step 5 — 選取第一位直播主
        search.select_first_streamer()

        # Step 6 — 處理可選彈窗、等待串流、截圖
        live = LivePage(driver)
        live.dismiss_popups()
        live.wait_for_stream()
        screenshot_path = live.capture(filename="starcraft2_streamer.png")

        assert screenshot_path.endswith(".png"), "截圖檔案未正確儲存"
