import io
import numpy as np
import cv2
from PIL import Image


class OcrHelper:
    """透過截圖 + OpenCV 彩色模板比對，在畫面上定位圖示並回傳中心座標。"""

    def __init__(self, driver, threshold: float = 0.75):
        self.driver = driver
        self.threshold = threshold

    def find_icon_center(self, template_path: str) -> tuple:
        """
        在當前頁面截圖中尋找 template_path 圖示的位置。
        回傳 (x, y) 為圖示中心的 CSS 像素座標（已除以 devicePixelRatio），
        可直接傳給 document.elementFromPoint。找不到則拋出 RuntimeError。
        """
        screenshot = self._get_screenshot_color()
        template = self._load_template_color(template_path)
        top_left = self._match(screenshot, template)
        h, w = template.shape[:2]
        cx = top_left[0] + w // 2
        cy = top_left[1] + h // 2
        dpr = self.driver.execute_script("return window.devicePixelRatio") or 1
        return cx / dpr, cy / dpr

    def _get_screenshot_color(self) -> np.ndarray:
        png_bytes = self.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def _load_template_color(self, path: str) -> np.ndarray:
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError(f"模板圖片不存在: {path}")
        return template

    def _match(self, screenshot: np.ndarray, template: np.ndarray) -> tuple:
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val < self.threshold:
            cv2.imwrite("debug_ocr_fail.png", screenshot)
            raise RuntimeError(
                f"找不到目標圖示（相似度 {max_val:.2f} < 門檻 {self.threshold}）"
                f"，已儲存 debug_ocr_fail.png"
            )
        return max_loc
