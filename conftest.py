import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    """建立桌面版 Chrome WebDriver，測試結束後自動關閉。"""
    options = Options()
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
