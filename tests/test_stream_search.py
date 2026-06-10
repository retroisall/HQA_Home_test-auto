import os
import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.live_page import LivePage

SEARCH_QUERY = "StarCraft II"


@pytest.mark.smoke
class TestTwitchWAP:
    def test_search_and_view_starcraft_streamer(self, driver):
        # 前往 Twitch
        home = HomePage(driver)
        home.open()
        assert "twitch.tv" in driver.current_url, "未成功導航至 Twitch"
        home.verify_logo()

        # 點擊搜尋圖標
        home.click_search()
        search = SearchPage(driver)
        assert search.is_search_input_visible(), "點擊搜尋後輸入框未出現"

        # 輸入星海爭霸II
        search.type_query(SEARCH_QUERY)
        assert search.get_input_value() == SEARCH_QUERY, "輸入框內容與預期不符"

        # 送出搜尋
        search.submit_search()
        assert "starcraft" in driver.current_url.lower(), "搜尋後 URL 未包含關鍵字"
        assert search.has_results(), "搜尋結果頁未出現任何結果卡片"

        # 向下捲動 2 次
        y = search.get_scroll_y()
        search.scroll_down()
        assert search.get_scroll_y() > y, "第一次捲動後頁面未移動"

        y = search.get_scroll_y()
        search.scroll_down()
        assert search.get_scroll_y() > y, "第二次捲動後頁面未移動"

        # 選擇一位主播
        search.select_first_streamer()
        assert "twitch.tv/search" not in driver.current_url, "點擊主播後未離開搜尋頁"

        # 關閉可選彈窗
        live = LivePage(driver)
        live.dismiss_if_present(LivePage.MATURE_ACCEPT, timeout=5)
        live.dismiss_if_present(LivePage.MODAL_CLOSE, timeout=3)

        # 等待串流載入
        live.wait_for_page()
        live.wait_for_player()
        assert live.is_player_visible(), "播放器元素不可見"
        assert live.is_stream_playing(), "串流未開始播放（video.readyState < 2）"

        # 截圖存檔
        screenshot_path = live.capture(filename="starcraft2_streamer.png")
        assert os.path.exists(screenshot_path), "截圖檔案不存在"
        assert os.path.getsize(screenshot_path) > 10_000, "截圖檔案過小，可能為空白畫面"
