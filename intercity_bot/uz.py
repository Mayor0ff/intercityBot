import aiohttp
import json
from urllib.parse import urlencode

API_URL = "https://booking.uz.gov.ua/"



class Station:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def toDict(self):
        return {'title': self.title, 'id': self.id}


async def api_request(method: str, parameters: dict, type: str, lang: str = "ru"):
    async with aiohttp.ClientSession() as session:
        if type == 'get':
            url = "{}{}/{}?{}".format(API_URL, lang, method, urlencode(parameters))
            async with session.get(url) as response:
                return json.loads(await response.text())
        elif type == 'post':
            url = "{}{}/{}".format(API_URL, lang, method)
            async with session.post(url) as response:
                return json.loads(await response.text())


async def search_stations(search_request: str):
    result = await api_request('train_search/station/', {'term': search_request}, 'get')
    return list(map(lambda station: Station(station['title'], station['value']), result))