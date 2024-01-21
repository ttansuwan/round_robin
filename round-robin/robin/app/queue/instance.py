import requests

class Instance:
    def __init__(self, url: str) -> None:
        self.url = url
        self.is_alive = True

    def forward(self, payload: dict):
        try:
            print(self.url)
            response = requests.post(self.url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            self.is_alive = False
            return None
        