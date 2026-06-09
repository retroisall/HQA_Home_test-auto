import os
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from utils.ocr_helper import OcrHelper

SEARCH_ICON_TEMPLATE = os.path.join(
    os.path.dirname(__file__), "..", "assets", "search_icon.png"
)


class HomePage(BasePage):
    URL = "https://www.twitch.tv"

    def open(self) -> "HomePage":
        self.driver.get(self.URL)
        self.wait_for_page_load()
        return self

    def click_search(self) -> "HomePage":
        """透過 OCR 圖形比對定位放大鏡圖示後點擊。"""
        ocr = OcrHelper(self.driver)
        x, y = ocr.find_icon_center(SEARCH_ICON_TEMPLATE)
        ActionChains(self.driver).move_by_offset(x, y).click().perform()
        return self
