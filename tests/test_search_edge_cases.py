import pytest
from pages.home_page import HomePage
from pages.live_page import LivePage
from pages.search_page import SearchPage


@pytest.mark.edge
class TestSearchEdgeCases:
    def test_empty_search_does_not_crash(self, driver):
        """直接按 Enter 不輸入內容，頁面不應崩潰，應仍在 Twitch 網域。"""
        home = HomePage(driver)
        home.open()
        home.click_search()

        search = SearchPage(driver)
        search.submit_search()  # 不輸入任何文字，直接送出

        assert "twitch.tv" in driver.current_url, "空白搜尋後不應離開 Twitch 網域"
        assert driver.title != "", "空白搜尋後頁面不應空白崩潰"

    def test_gibberish_search_shows_no_crash(self, driver):
        """輸入極不可能有結果的亂碼，頁面不應崩潰，應仍在 Twitch 網域。"""
        home = HomePage(driver)
        home.open()
        home.click_search()

        search = SearchPage(driver)
        search.type_query("xqzjwmvbnoplasdfghijkl99999")
        search.submit_search()

        assert "twitch.tv" in driver.current_url, "亂碼搜尋後不應離開 Twitch 網域"
        assert driver.title != "", "亂碼搜尋後頁面不應空白崩潰"

    def test_excessive_scroll_does_not_crash(self, driver):
        """捲動超過頁面底端 10 次，不應拋出 JS 例外，頁面仍應在 Twitch 網域。"""
        home = HomePage(driver)
        home.open()
        home.click_search()

        search = SearchPage(driver)
        search.type_query("StarCraft II")
        search.submit_search()

        for _ in range(10):
            search.scroll_down()

        assert "twitch.tv" in driver.current_url, "過度捲動後頁面不應崩潰"

    def test_player_absent_before_entering_live_page(self, driver):
        """在進入直播頁之前，播放器元素不應出現（防止後續 assert 誤判）。"""
        home = HomePage(driver)
        home.open()
        home.click_search()

        search = SearchPage(driver)
        search.type_query("StarCraft II")
        search.submit_search()

        live = LivePage(driver)
        assert not live.is_player_visible(), "搜尋結果頁不應存在直播播放器"
