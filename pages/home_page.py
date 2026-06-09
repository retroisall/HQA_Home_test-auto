import os
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.ocr_helper import OcrHelper

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
TWITCH_LOGO_TEMPLATE = os.path.join(_ASSETS, "twitch_logo.png")
SEARCH_ICON_TEMPLATE = os.path.join(_ASSETS, "search_icon.png")

_COOKIE_ACCEPT = (By.CSS_SELECTOR, '[data-a-target="consent-banner-accept"]')


class HomePage(BasePage):
    URL = "https://www.twitch.tv"

    def open(self) -> "HomePage":
        """前往 Twitch，以 OCR 辨識 logo 確認載入，並關閉 cookie 橫幅避免遮擋底部導航。"""
        self.driver.get(self.URL)
        self.wait_for_page_load()
        OcrHelper(self.driver).find_icon_center(TWITCH_LOGO_TEMPLATE)
        self.dismiss_if_present(_COOKIE_ACCEPT, timeout=5)
        return self

    def click_search(self) -> "HomePage":
        """透過 OCR 圖形比對定位放大鏡圖示後，用 JS 點擊絕對座標。"""
        ocr = OcrHelper(self.driver)
        x, y = ocr.find_icon_center(SEARCH_ICON_TEMPLATE)
        print(f"[OCR] search icon CSS coords: ({x:.1f}, {y:.1f})")
        self.driver.execute_script(
            """
            var el = document.elementFromPoint(arguments[0], arguments[1]);
            if (!el) throw new Error(
                'elementFromPoint(' + arguments[0] + ',' + arguments[1] + ') returned null.'
                + ' viewport=' + window.innerWidth + 'x' + window.innerHeight
            );
            // 往上找最近的 button / a / role=button，讓 React 事件正確觸發
            var target = el;
            while (target && target.tagName !== 'BUTTON' && target.tagName !== 'A'
                   && target.getAttribute('role') !== 'button') {
                target = target.parentElement;
            }
            (target || el).click();
            """,
            x, y,
        )
        import time; time.sleep(2)
        self.driver.save_screenshot("debug_after_click_search.png")
        print(f"[OCR] URL after click: {self.driver.current_url}")
        return self
