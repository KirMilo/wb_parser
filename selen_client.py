import time

from selenium import webdriver


def get_wb_token() -> dict[str, str] | None:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/121.0.0.0 Safari/537.36")
    options.add_argument("--enable-features=WebRtcHideLocalIpsWithMdns")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); """}
                           )

    driver.get("https://www.wildberries.ru/")
    for i in range(3):
        time.sleep(5)
        cookies = driver.get_cookies()
        if not cookies:
            print(f"Не удалось получить куки. Попытка {i + 1} ")
        else:
            driver.close()
            return {cookies[0]["name"]: cookies[0]["value"]}

    raise Exception("Не удалось получить куки. Попытки кончились.")
