import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """所有頁面物件的基底類別，封裝常用等待與操作方法。"""

    EXPLICIT_WAIT = 15
    STEP_PAUSE = 1.5  # 每個動作後的停頓秒數，設為 0 關閉

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.EXPLICIT_WAIT)

    def find(self, locator):
        """等待元素出現於 DOM 後回傳。"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """等待元素出現後用 JS 點擊（繞過 overlay / React hydration 未完成的問題）。"""
        el = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", el)
        if self.STEP_PAUSE:
            time.sleep(self.STEP_PAUSE)

    def type_text(self, locator, text: str):
        """清空欄位後輸入指定文字。"""
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
        if self.STEP_PAUSE:
            time.sleep(self.STEP_PAUSE)

    def scroll_down(self, pixels: int = 600):
        """向下捲動指定像素後等待動畫完成。"""
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(self.STEP_PAUSE)

    def is_present(self, locator, timeout: int = 3) -> bool:
        """在 timeout 秒內若元素存在回傳 True，否則 False。"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def find_visible(self, locator):
        """多個元素符合 locator 時，等待並回傳第一個可見的。"""
        def _check(driver):
            for el in driver.find_elements(*locator):
                if el.is_displayed():
                    return el
            return False
        return WebDriverWait(self.driver, self.EXPLICIT_WAIT).until(_check)

    def dismiss_if_present(self, locator, timeout: int = 3):
        """若元素可見且可點擊則點擊（用於關閉可選彈窗）。"""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

    def take_screenshot(self, filepath: str) -> str:
        """截圖並儲存至指定路徑，回傳路徑字串。"""
        self.driver.save_screenshot(filepath)
        return filepath

    def get_scroll_y(self) -> int:
        """回傳目前頁面的垂直捲動位置。"""
        return self.driver.execute_script("return window.scrollY")

    def wait_for_page_load(self):
        """等待 document.readyState 為 complete。"""
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
