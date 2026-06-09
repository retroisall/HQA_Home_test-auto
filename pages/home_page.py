from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Twitch 首頁：負責開啟網站與點擊搜尋圖示。"""

    URL = "https://www.twitch.tv"

    # Twitch 一致使用 data-a-target 屬性；第二個 selector 作為 fallback
    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        '[data-a-target="nav-search-button"], a[href="/search"]',
    )

    def open(self) -> "HomePage":
        """前往 Twitch 首頁並等待頁面載入完成。"""
        self.driver.get(self.URL)
        self.wait_for_page_load()
        return self

    def click_search(self) -> "HomePage":
        """點擊頂部搜尋圖示，進入搜尋頁。"""
        self.click(self.SEARCH_BUTTON)
        return self
