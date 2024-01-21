import requests


class Instance:
    def __init__(self, url: str) -> None:
        self.url = url
        self.is_alive = True

    def forward(self, payload: dict, retry_no: int = 0):
        if retry_no > 2:
            return None
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            return response.json()
        except TimeoutError:
            # Allow retry for timeout
            self.forward(payload=payload, retry_no=retry_no + 1)
        except Exception:
            self.is_alive = False
            return None

    def __str__(self) -> str:
        return self.url
