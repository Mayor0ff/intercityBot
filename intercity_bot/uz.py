import aiohttp
import aiofiles
import json
import time
import random
import os
from urllib.parse import urlencode
from intercity_bot.user import User

API_URL = "https://booking.uz.gov.ua/"



class Station:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def toDict(self):
        return {'title': self.title, 'id': self.id}


class Train:
    def __init__(self, num, category, travel_time, from_station, to_station):
        self.num = num
        self.category = category
        self.travel_time = travel_time
        self.from_station = from_station
        self.to_station = to_station


class CaptchaException(Exception):
    pass


class UnknownException(Exception):
    pass


async def api_request(method: str, parameters: dict, type: str, user: User, lang: str = "ru"):
    cookies = {'_gv_sessid': user.cookie_session, '_gv_lang': 'ru'}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        if type == 'get':
            url = "{}{}/{}?{}".format(API_URL, lang, method, urlencode(parameters))
            async with session.get(url) as response:
                if '_gv_sessid' in response.cookies:
                    if user.cookie_session != response.cookies['_gv_sessid'].value:
                        user.update_cookie_session(response.cookies['_gv_sessid'].value)
                
                return json.loads(await response.text())
        elif type == 'post-urlencode':
            url = "{}{}/{}".format(API_URL, lang, method)
            async with session.post(url, data=parameters) as response:
                if '_gv_sessid' in response.cookies:
                    if user.cookie_session != response.cookies['_gv_sessid'].value:
                        user.update_cookie_session(response.cookies['_gv_sessid'].value)

                return json.loads(await response.text())


async def search_stations(user: User, search_request: str):
    result = await api_request('train_search/station/', {'term': search_request}, 'get', user)
    return list(map(lambda station: Station(station['title'], station['value']), result))


async def search_trains(user: User, station_from_id: int, station_to_id: int, date: str, time: str = '00:00', captcha: str = None):
    parameters = {'from': station_from_id, 'to': station_to_id, 'date': date, 'time': time}
    if type(captcha) is str:
        parameters['captcha'] = captcha

    result = await api_request('train_search/', parameters, 'post-urlencode', user)

    if 'error' in result:
        if result['error'] == 1:
            raise CaptchaException()
        else:
            raise UnknownException()

    return list(map(
        lambda t: Train(
            t['num'], t['category'], t['travelTime'], 
            t['from'], t['to']
        ), 
        result['data']['list']
    ))


async def get_train_carriages(user: User, station_from_id: int, station_to_id: int, date: str, train_num: str, carriage_type: str = None, captcha: str = None):
    parameters = {'from': station_from_id, 'to': station_to_id, 'date': date, 'train': train_num}
    if type(carriage_type) is str:
        parameters['wagon_type_id'] = carriage_type
    if type(captcha) is str:
        parameters['captcha'] = captcha

    result = await api_request('train_wagons/', parameters, 'post-urlencode', user)

    if 'error' in result:
        if result['error'] == 1:
            raise CaptchaException()
        else:
            raise UnknownException()

    return result


async def get_carriage(user: User, station_from_id: int, station_to_id: int, date: str, train_num: str, carriage_num: int, carriage_type: str, carriage_class: int, captcha: str = None):
    parameters = {'from': station_from_id, 'to': station_to_id, 'date': date, 'train': train_num, 'wagon_num': carriage_num, 'wagon_type': carriage_type, 'wagon_class': carriage_class}
    if type(captcha) is str:
        parameters['captcha'] = captcha

    result = await api_request('train_wagon/', parameters, 'post-urlencode', user)

    if 'error' in result:
        if 'captcha' in result:
            raise CaptchaException()
        else:
            raise UnknownException()

    return result


async def get_captcha(user: User):
    cookies = {'_gv_sessid': user.cookie_session, '_gv_lang': 'uk'}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get("{}{}".format(API_URL, 'captcha/')) as response:
            random.seed(time.time())
            script_dir = os.path.dirname(__file__)
            filename = "{}/captcha/{}.gif".format(script_dir, random.randint(0, 999_999_999))

            async with aiofiles.open(filename, "wb") as file:
                await file.write(await response.read())
                await file.close()

            return filename