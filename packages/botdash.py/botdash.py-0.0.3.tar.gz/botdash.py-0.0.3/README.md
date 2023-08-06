# BotDash.py

https://botdash.pro

---

## Get started

```py
from botdash import Client

dash = Client("TOKEN_HERE")
val = dash.get("GUILD_ID_HERE", "DATABASE_ID_HERE").value # .data works too

print(val)
```