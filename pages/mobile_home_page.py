import os
from selenium.webdriver.common.by import By
from pages.home_page import HomePage

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

# CSS selector 作為 mobile OCR 的備援（原始 WAP 版本使用）
_SEARCH_BUTTON_CSS = (
    By.CSS_SELECTOR,
    '[data-a-target="nav-search-button"], a[href="/search"], [aria-label="Search"]',
)


class MobileHomePage(HomePage):
    """行動版首頁：覆寫 OCR template 路徑，優先嘗試 CSS selector 點擊搜尋。"""

    # 行動版 OCR template（需先執行 utils/capture_mobile_templates.py 生成）
    LOGO_TEMPLATE = os.path.join(_ASSETS, "twitch_logo_mobile.png")
    SEARCH_ICON_TEMPLATE = os.path.join(_ASSETS, "search_icon_mobile.png")

    def verify_logo(self) -> "MobileHomePage":
        """行動版首頁以 URL 確認載入（行動版 logo 位置因裝置而異，略過 OCR）。"""
        assert "twitch.tv" in self.driver.current_url, "行動版首頁未成功載入 Twitch"
        return self

    def click_search(self) -> "MobileHomePage":
        """行動版搜尋：優先用 CSS selector，否則直接導航至行動版瀏覽/搜尋頁。"""
        if self.is_present(_SEARCH_BUTTON_CSS, timeout=3):
            self.click(_SEARCH_BUTTON_CSS)
            return self

        # 行動版底部 tab 搜尋入口位於 /directory，直接導航
        self.driver.get("https://m.twitch.tv/directory")
        return self
