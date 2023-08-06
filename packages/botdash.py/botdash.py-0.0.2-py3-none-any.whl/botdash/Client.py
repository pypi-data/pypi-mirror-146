import requests
import ujson as json

class Client:
    def __init__(self, token: str, debug: bool = False):
        self.token = token
        self.debug = debug
        self.uri = "https://botdash.pro/api/v2"

    def __log(self, message: str):
        print(f"[Botdash.py Client] {message}")

    def get(self, guild_id: str, key: str):
        res = requests.get(
            f"{self.uri}/value/{key}/{guild_id}", 
            headers={
                "Authorization": self.token
            }     
        )

        if self.debug:
            self.__log(res.text)

        return json.loads(res.text)