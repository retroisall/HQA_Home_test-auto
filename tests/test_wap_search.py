import pytest
from pages.mobile_home_page import MobileHomePage
from pages.search_page import SearchPage
from pages.live_page import LivePage

SEARCH_QUERY = "StarCraft II"

# Slow 3G 網路條件（Chrome DevTools Protocol 參數）
_SLOW_3G = {
    "offline": False,
    "downloadThroughput": 500 * 1024 / 8,   # 500 Kbps
    "uploadThroughput": 500 * 1024 / 8,
    "latency": 400,                          # 400ms RTT
}
_NO_THROTTLE = {
    "offline": False,
    "downloadThroughput": -1,
    "uploadThroughput": -1,
    "latency": 0,
}


@pytest.mark.wap
class TestWAPSearch:
    """WAP 基礎場景：iPhone 12 Pro Chrome 模擬，驗證行動版 Twitch 核心功能。"""

    def test_wap_homepage_loads(self, mobile_driver):
        """行動版首頁應可成功載入並停在 Twitch 網域。"""
        home = MobileHomePage(mobile_driver)
        home.open()
        assert "twitch.tv" in mobile_driver.current_url, "行動版首頁未導航至 Twitch"
        assert mobile_driver.title != "", "行動版首頁 title 為空，可能未載入"

    def test_wap_search_and_results(self, mobile_driver):
        """行動版搜尋 StarCraft II 應顯示搜尋結果。"""
        home = MobileHomePage(mobile_driver)
        home.open()
        home.click_search()

        search = SearchPage(mobile_driver)
        assert search.is_search_input_visible(), "行動版搜尋輸入框未出現"

        search.type_query(SEARCH_QUERY)
        search.submit_search()

        assert "starcraft" in mobile_driver.current_url.lower(), \
            "搜尋後 URL 未包含 starcraft"
        assert search.has_results(), "行動版搜尋結果頁未出現任何結果卡片"

    def test_wap_scroll_works(self, mobile_driver):
        """行動版捲動應正常移動頁面位置。"""
        home = MobileHomePage(mobile_driver)
        home.open()
        home.click_search()

        search = SearchPage(mobile_driver)
        search.type_query(SEARCH_QUERY)
        search.submit_search()

        y_before = search.get_scroll_y()
        search.scroll_down()
        y_after = search.get_scroll_y()

        assert y_after > y_before, "行動版捲動後頁面未移動"
        assert "twitch.tv" in mobile_driver.current_url, "捲動後不應離開 Twitch"

    def test_wap_enter_live_page(self, mobile_driver):
        """行動版應可進入直播頁並看到播放器。"""
        home = MobileHomePage(mobile_driver)
        home.open()
        home.click_search()

        search = SearchPage(mobile_driver)
        search.type_query(SEARCH_QUERY)
        search.submit_search()
        search.select_first_streamer()

        assert "twitch.tv/search" not in mobile_driver.current_url, \
            "點擊直播主後未離開搜尋頁"

        live = LivePage(mobile_driver)
        live.dismiss_if_present(LivePage.MATURE_ACCEPT, timeout=5)
        live.dismiss_if_present(LivePage.MODAL_CLOSE, timeout=3)
        live.wait_for_page()
        live.wait_for_player()

        assert live.is_player_visible(), "行動版播放器元素不可見"


@pytest.mark.wap
class TestWAPNetwork:
    """WAP 網路品質場景：Slow 3G (500 Kbps / 400ms RTT) 下的基礎功能驗證。"""

    def test_wap_slow_3g_homepage_loads(self, mobile_driver):
        """Slow 3G 下行動版首頁仍應在合理時間內載入完成。"""
        mobile_driver.execute_cdp_cmd("Network.enable", {})
        mobile_driver.execute_cdp_cmd("Network.emulateNetworkConditions", _SLOW_3G)
        try:
            home = MobileHomePage(mobile_driver)
            home.open()
            assert "twitch.tv" in mobile_driver.current_url, \
                "Slow 3G 下首頁未載入 Twitch"
            assert mobile_driver.title != "", "Slow 3G 下首頁 title 為空"
        finally:
            mobile_driver.execute_cdp_cmd("Network.emulateNetworkConditions", _NO_THROTTLE)

    def test_wap_slow_3g_search_works(self, mobile_driver):
        """Slow 3G 下行動版搜尋應仍可送出並得到搜尋結果頁。"""
        mobile_driver.execute_cdp_cmd("Network.enable", {})
        mobile_driver.execute_cdp_cmd("Network.emulateNetworkConditions", _SLOW_3G)
        try:
            home = MobileHomePage(mobile_driver)
            home.open()
            home.click_search()

            search = SearchPage(mobile_driver)
            search.type_query(SEARCH_QUERY)
            search.submit_search()

            assert "twitch.tv" in mobile_driver.current_url, \
                "Slow 3G 下搜尋後不應離開 Twitch"
        finally:
            mobile_driver.execute_cdp_cmd("Network.emulateNetworkConditions", _NO_THROTTLE)
