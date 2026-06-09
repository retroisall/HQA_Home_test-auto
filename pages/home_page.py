from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Twitch 首頁：負責開啟網站與點擊搜尋圖示。"""

    URL = "https://www.twitch.tv"

    # 新版 Twitch 首頁直接顯示搜尋框，無獨立搜尋按鈕
    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        '[data-a-target="nav-search-box"] input[type="search"]',
    )

    def open(self) -> "HomePage":
        """前往 Twitch 首頁並等待頁面載入完成。"""
        self.driver.get(self.URL)
        self.wait_for_page_load()
        return self

    def click_search(self) -> "HomePage":
        """點擊搜尋輸入框以取得焦點。"""
        self.click(self.SEARCH_INPUT)
        return self
