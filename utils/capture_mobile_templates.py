"""
行動版 OCR template 截圖工具

執行方式：
    python utils/capture_mobile_templates.py

功能：
    以 iPhone 12 Pro 模擬開啟 Twitch 首頁，
    自動截取全頁快照並儲存至 assets/mobile_full.png，
    供人工裁切 twitch_logo_mobile.png 與 search_icon_mobile.png。

    若想互動式選取區域，加上 --interactive 旗標（需安裝 opencv-python）。
"""

import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


def _build_mobile_driver():
    options = Options()
    options.add_experimental_option("mobileEmulation", {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 "
            "Mobile/15E148 Safari/604.1"
        ),
    })
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def capture_full_page(interactive: bool = False) -> None:
    driver = _build_mobile_driver()
    try:
        driver.get("https://www.twitch.tv")
        time.sleep(4)  # 等待首頁完整渲染

        full_path = os.path.join(_ASSETS, "mobile_full.png")
        driver.save_screenshot(full_path)
        print(f"[OK] 全頁截圖已儲存：{full_path}")
        print()
        print("下一步：")
        print(f"  用圖像編輯軟體開啟 {full_path}")
        print("  裁切 Twitch logo 區域 → 另存為 assets/twitch_logo_mobile.png")
        print("  裁切搜尋圖示區域     → 另存為 assets/search_icon_mobile.png")

        if interactive:
            try:
                import cv2
                import numpy as np
                img = cv2.imread(full_path)
                roi = cv2.selectROI("選取 Logo 區域（按 Enter 確認）", img)
                if any(roi):
                    x, y, w, h = roi
                    crop = img[y:y+h, x:x+w]
                    logo_path = os.path.join(_ASSETS, "twitch_logo_mobile.png")
                    cv2.imwrite(logo_path, crop)
                    print(f"[OK] Logo template 已儲存：{logo_path}")

                roi = cv2.selectROI("選取搜尋圖示區域（按 Enter 確認）", img)
                if any(roi):
                    x, y, w, h = roi
                    crop = img[y:y+h, x:x+w]
                    search_path = os.path.join(_ASSETS, "search_icon_mobile.png")
                    cv2.imwrite(search_path, crop)
                    print(f"[OK] 搜尋圖示 template 已儲存：{search_path}")

                cv2.destroyAllWindows()
            except ImportError:
                print("[WARN] 未安裝 opencv-python，略過互動式裁切。")
    finally:
        driver.quit()


if __name__ == "__main__":
    interactive = "--interactive" in sys.argv
    capture_full_page(interactive=interactive)
