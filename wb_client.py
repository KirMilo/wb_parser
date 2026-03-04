import time

import requests
import random

from selen_client import get_wb_token


class WBClient:
    def __init__(self):
        self._cookies: dict | None = None

    @property
    def cookies(self) -> dict | None:
        if not self._cookies:
            self._cookies = get_wb_token()
        return self._cookies

    def get(self, url: str, params: dict = None) -> requests.Response | None:
        print(url)
        for retry in range(3):
            try:
                # time.sleep(random.random())  # Рандомная задержка
                response = requests.get(
                    url=url,
                    params=params,
                    headers={
                        "X-Service": "true",
                        "Connection": "Keep-Alive",
                        "User-Agent": "Android; 12; Google; google_pixel_27; 8.72.5; 13311234;",
                    },
                    cookies=self.cookies,
                )
                response.raise_for_status()
            except Exception as e:
                if retry > 1:
                    raise e
            else:
                return response

        return None
