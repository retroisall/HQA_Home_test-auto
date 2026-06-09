import os
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LivePage(BasePage):
    """直播頁面：處理可選彈窗、等待串流載入、截圖儲存。"""

    # 成人內容確認按鈕（部分頻道會出現）
    MATURE_ACCEPT = (By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')
    # 訂閱 / 通知 / 登入彈窗的關閉按鈕（含中文 aria-label）
    MODAL_CLOSE = (By.CSS_SELECTOR, '[aria-label="Close"], [aria-label="關閉對話框"], [data-a-target="modal-close-button"]')
    # Cookie 同意橫幅
    COOKIE_ACCEPT = (By.CSS_SELECTOR, '[data-a-target="consent-banner-accept"]')
    # 播放器元素（確認串流已載入的依據）
    PLAYER = (By.CSS_SELECTOR, 'video, [data-a-target="video-player"]')

    def dismiss_popups(self) -> "LivePage":
        """依序嘗試關閉成人內容確認、彈窗、Cookie 橫幅（皆為可選）。"""
        self.dismiss_if_present(self.MATURE_ACCEPT, timeout=5)
        self.dismiss_if_present(self.MODAL_CLOSE, timeout=3)
        self.dismiss_if_present(self.COOKIE_ACCEPT, timeout=3)
        return self

    def wait_for_stream(self) -> "LivePage":
        """等待頁面與播放器元素完全載入。"""
        self.wait_for_page_load()
        self.is_present(self.PLAYER, timeout=15)
        return self

    def capture(self, directory: str = "screenshots", filename: str = "streamer.png") -> str:
        """截圖並儲存至 screenshots/ 資料夾，回傳儲存路徑。"""
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        return self.take_screenshot(path)
