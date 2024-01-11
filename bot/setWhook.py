import requests

tg_api = ''

whook = ''

r = requests.get(f'https://api.telegra.org/bot{tg_api}/setWebhook?url=https://{whook}/')

print(r.json())
