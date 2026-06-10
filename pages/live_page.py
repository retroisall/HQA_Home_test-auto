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

    def wait_for_page(self) -> "LivePage":
        """等待頁面 document.readyState 為 complete。"""
        self.wait_for_page_load()
        return self

    def wait_for_player(self) -> "LivePage":
        """等待播放器元素出現，確認串流已載入。"""
        self.is_present(self.PLAYER, timeout=15)
        return self

    def is_player_visible(self) -> bool:
        """確認播放器元素在畫面上可見。"""
        try:
            self.find_visible(self.PLAYER)
            return True
        except Exception:
            return False

    def is_stream_playing(self) -> bool:
        """確認 video 元素已開始播放（readyState >= 2 表示有足夠資料可播放）。"""
        try:
            return self.driver.execute_script(
                "var v = document.querySelector('video'); return v && v.readyState >= 2;"
            )
        except Exception:
            return False

    def capture(self, directory: str = "screenshots", filename: str = "streamer.png") -> str:
        """截圖並儲存至 screenshots/ 資料夾，回傳儲存路徑。"""
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        return self.take_screenshot(path)
