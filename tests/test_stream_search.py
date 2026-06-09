from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.live_page import LivePage

SEARCH_QUERY = "StarCraft II"


class TestTwitchWAP:
    def test_search_and_view_starcraft_streamer(self, driver):
        # 前往 Twitch
        home = HomePage(driver)
        home.open()

        # 點擊搜尋圖標
        home.click_search()

        # 輸入星海爭霸II
        search = SearchPage(driver)
        search.dismiss_cookie_banner()
        search.search_for(SEARCH_QUERY)

        # 向下捲動 2 次
        search.scroll_down_twice()

        # 選擇一位主播
        search.select_first_streamer()

        # 在直播頁面等待所有內容載入完畢後截圖
        live = LivePage(driver)
        live.dismiss_popups()
        live.wait_for_stream()
        screenshot_path = live.capture(filename="starcraft2_streamer.png")

        assert screenshot_path.endswith(".png"), "截圖檔案未正確儲存"
