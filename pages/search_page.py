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

    COOKIE_ACCEPT = (By.CSS_SELECTOR, '[data-a-target="consent-banner-accept"]')

    def dismiss_cookie_banner(self) -> "SearchPage":
        """若出現 Cookie 同意橫幅則關閉，避免遮擋後續操作。"""
        self.dismiss_if_present(self.COOKIE_ACCEPT, timeout=5)
        return self

    def search_for(self, query: str) -> "SearchPage":
        """在展開的搜尋框中輸入關鍵字並送出搜尋。"""
        el = self.find_visible(self.SEARCH_INPUT)
        el.clear()
        el.send_keys(query)
        el.send_keys(Keys.RETURN)
        self.wait_for_page_load()
        return self

    def scroll_down_twice(self) -> "SearchPage":
        """向下捲動兩次以載入更多搜尋結果。"""
        self.scroll_down()
        self.scroll_down()
        return self

    def select_first_streamer(self) -> "SearchPage":
        """點擊第一個直播主卡片，進入其直播頁面。"""
        self.click(self.STREAMER_CARD)
        return self
