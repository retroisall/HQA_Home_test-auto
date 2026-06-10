from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class SearchPage(BasePage):
    """搜尋頁：輸入關鍵字、捲動結果清單、選取直播主。"""

    # Twitch 搜尋框展開後的可見 input（DOM 中存在兩個相同 selector，用 find_visible 取可見的）
    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        'input[autocomplete="twitch-nav-search"]',
    )
    # 搜尋結果卡片中的第一個連結（縮圖連結）
    STREAMER_CARD = (By.CSS_SELECTOR, '.search-result-card a')

    def type_query(self, query: str) -> "SearchPage":
        """在展開的搜尋框中輸入關鍵字。"""
        el = self.find_visible(self.SEARCH_INPUT)
        el.clear()
        el.send_keys(query)
        return self

    def submit_search(self) -> "SearchPage":
        """送出搜尋（按下 Enter）並等待結果頁載入。"""
        el = self.find_visible(self.SEARCH_INPUT)
        el.send_keys(Keys.RETURN)
        self.wait_for_page_load()
        return self

    def select_first_streamer(self) -> "SearchPage":
        """點擊第一個直播主卡片，動態渲染未完成時自動遞迴重試。"""
        self.retry(lambda: self.click(self.STREAMER_CARD))
        return self

    def is_search_input_visible(self) -> bool:
        """確認搜尋輸入框已出現且可見。"""
        try:
            self.find_visible(self.SEARCH_INPUT)
            return True
        except Exception:
            return False

    def get_input_value(self) -> str:
        """回傳搜尋輸入框目前的值。"""
        return self.find_visible(self.SEARCH_INPUT).get_attribute("value")

    def has_results(self) -> bool:
        """確認搜尋結果卡片至少出現一張。"""
        return self.is_present(self.STREAMER_CARD, timeout=10)
