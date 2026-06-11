import pytest
from pages.mobile_home_page import MobileHomePage
from pages.mobile_search_page import MobileSearchPage
from pages.live_page import LivePage

SEARCH_QUERY = "StarCraft II"


@pytest.mark.wap
class TestWAPSearch:
    """WAP 連續流程：iPhone 12 Pro Chrome 模擬，依序走完使用者旅程。

    測試依順序共用同一個 session-scoped browser，每步接續上一步的狀態：
      Step 1 (homepage_loads)   → 開啟首頁
      Step 2 (search_results)   → 點搜尋、輸入、送出，停在結果頁
      Step 3 (scroll_works)     → 在結果頁捲動
      Step 4 (enter_live_page)  → 點進直播頁並驗證播放器
    """

    def test_wap_homepage_loads(self, mobile_driver):
        """Step 1：行動版首頁應可成功載入並停在 Twitch 網域。"""
        home = MobileHomePage(mobile_driver)
        home.open()
        assert "twitch.tv" in mobile_driver.current_url, "行動版首頁未導航至 Twitch"
        assert mobile_driver.title != "", "行動版首頁 title 為空，可能未載入"

    def test_wap_search_and_results(self, mobile_driver):
        """Step 2：從首頁點搜尋、輸入 StarCraft II，應顯示搜尋結果。"""
        home = MobileHomePage(mobile_driver)
        home.click_search()

        search = MobileSearchPage(mobile_driver)
        assert search.is_search_input_visible(), "行動版搜尋輸入框未出現"

        search.type_query(SEARCH_QUERY)
        search.submit_search()

        assert "starcraft" in mobile_driver.current_url.lower(), \
            "搜尋後 URL 未包含 starcraft"
        assert search.has_results(), "行動版搜尋結果頁未出現任何結果卡片"

    def test_wap_scroll_works(self, mobile_driver):
        """Step 3：在搜尋結果頁捲動，頁面位置應往下移動。"""
        search = MobileSearchPage(mobile_driver)

        y_before = search.get_scroll_y()
        search.scroll_down()
        y_after = search.get_scroll_y()

        assert y_after > y_before, "行動版捲動後頁面未移動"
        assert "twitch.tv" in mobile_driver.current_url, "捲動後不應離開 Twitch"

    def test_wap_enter_live_page(self, mobile_driver):
        """Step 4：從搜尋結果頁點進直播頁，應看到播放器。"""
        search = MobileSearchPage(mobile_driver)
        search.select_first_streamer()

        assert "twitch.tv/search" not in mobile_driver.current_url, \
            "點擊直播主後未離開搜尋頁"

        live = LivePage(mobile_driver)
        live.dismiss_if_present(LivePage.MATURE_ACCEPT, timeout=5)
        live.dismiss_if_present(LivePage.MODAL_CLOSE, timeout=3)
        live.wait_for_page()
        live.wait_for_player()

        assert live.is_player_visible(), "行動版播放器元素不可見"
