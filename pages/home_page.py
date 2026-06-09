from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Twitch 首頁：負責開啟網站與點擊搜尋輸入框。"""

    URL = "https://www.twitch.tv"

    # 搜尋 input（390px 手機版面下已直接顯示於 nav，無需先點擊搜尋按鈕）
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[autocomplete="twitch-nav-search"]')

    def open(self) -> "HomePage":
        """前往 Twitch 首頁並等待頁面載入完成。"""
        self.driver.get(self.URL)
        self.wait_for_page_load()
        return self

    def click_search(self) -> "HomePage":
        """點擊搜尋輸入框（即規格中的「點擊搜尋圖示」步驟）。"""
        self.find_visible(self.SEARCH_INPUT).click()
        return self
