from selenium.webdriver.common.by import By
from pages.search_page import SearchPage

_NAV_SKIP = frozenset([
    "https://m.twitch.tv/",
    "https://m.twitch.tv/directory",
    "https://m.twitch.tv/activity",
    "https://m.twitch.tv/home",
])


class MobileSearchPage(SearchPage):
    """行動版搜尋頁：覆寫 selector 以相容 m.twitch.tv 行動介面。

    行動版搜尋流程：
      1. /directory 頁輸入關鍵字 → 送出後到 /search?term=X
      2. 選第一個分類結果 → /directory/category/X
      3. 分類頁有標準 channel link，點擊後進入直播
    """

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        'input[type="search"], input[autocomplete="twitch-nav-search"]',
    )
    # 行動版搜尋結果出現的分類卡片（有標準 href，可靠性高）
    CATEGORY_CARD = (By.CSS_SELECTOR, 'a[href*="/directory/category/"]')

    def has_results(self) -> bool:
        """分類卡片出現即視為有搜尋結果。"""
        return self.is_present(self.CATEGORY_CARD, timeout=10)

    def select_first_streamer(self) -> "MobileSearchPage":
        """行動版：點分類卡片 → 分類頁點第一個頻道連結。"""
        # Step 1: 取得分類頁 URL 後直接導航（避免 SPA click → DOM 渲染時序問題）
        cat_link = self.driver.find_element(*self.CATEGORY_CARD)
        cat_url = cat_link.get_attribute("href")
        self.driver.get(cat_url)
        self.wait_for_page_load()

        # Step 2: 分類頁找第一個頻道 stream 連結（排除 nav、/home、/directory）
        def _click_first_channel():
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a')
            for link in links:
                href = link.get_attribute("href") or ""
                if (href not in _NAV_SKIP
                        and "/directory" not in href
                        and "/search" not in href
                        and "/home" not in href
                        and "twitch.tv/" in href
                        and not href.rstrip("/").endswith("twitch.tv")):
                    link.click()
                    return
            raise RuntimeError(f"分類頁找不到頻道連結")

        self.retry(_click_first_channel)
        return self
