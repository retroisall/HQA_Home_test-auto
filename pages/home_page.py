from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Twitch 首頁：負責開啟網站與點擊搜尋圖示。"""

    URL = "https://www.twitch.tv"

    # 搜尋圖示按鈕（支援英文與中文介面）
    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        'button[aria-label="Search"], button[aria-label="搜尋"]',
    )

    def open(self) -> "HomePage":
        """前往 Twitch 首頁並等待頁面載入完成。"""
        self.driver.get(self.URL)
        self.wait_for_page_load()
        return self

    def click_search(self) -> "HomePage":
        """點擊搜尋圖示按鈕，展開搜尋輸入框。"""
        self.click(self.SEARCH_BUTTON)
        return self
