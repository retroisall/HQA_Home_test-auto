import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 手機螢幕尺寸（390x844 / 3x DPR）搭配桌面 Chrome UA。
# 原因：iOS / Android UA 會觸發 Twitch 強制 redirect 到 m.twitch.tv（另一套完全不同的行動版），
# 導致所有選取器全部失效。使用桌面 UA 讓 Twitch 服務 responsive 桌面版，
# 在 390px 寬度下自動顯示手機版面配置，符合「Chrome Mobile Emulator」規格要求。
_MOBILE_EMULATION = {
    "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
    "userAgent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}


@pytest.fixture(scope="session")
def driver():
    """建立使用 Chrome Mobile Emulator 的 WebDriver，測試結束後自動關閉。"""
    options = Options()
    options.add_experimental_option("mobileEmulation", _MOBILE_EMULATION)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # 降低自動化偵測特徵，避免被網站封鎖
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()
