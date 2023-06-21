from io import BytesIO
import pycurl
import constants
import json

class Request():
    def __init__(self) -> None:
        pass

    def get_json(self, city_date):
        city, date = city_date

        url = f'{constants.Server.URL.value}:{constants.Server.PORT.value}'
        data = f'city={city}&date={date}'

        respone = BytesIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.WRITEFUNCTION, respone.write)
        c.perform()
        c.close()

        return respone.getvalue().decode()

if __name__ == "__main__":
    req = Request()
    print(req.get_json(('Wroclaw', '2023-07-12')))
