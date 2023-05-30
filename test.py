"""
   File Name :    test.py
   Description :
   Author :       Cl0udG0d
   date :         2023/2/12
"""
from json import loads
from re import findall
from time import sleep

from requests import Session, RequestException, Response
from retrying import retry

from tookit.fofaUseragent import getFakeUserAgent


class Emailnator:
    def __init__(self) -> None:
        self.client = Session()
        self.client.get("https://www.emailnator.com/", timeout=6)
        self.cookies = self.client.cookies.get_dict()
        # XSRF_TOKEN=self.__make_request(self.client)

        self.client.headers = {
            "authority": "www.emailnator.com",
            "origin": "https://www.emailnator.com",
            "referer": "https://www.emailnator.com/",
            "user-agent": getFakeUserAgent(),
            "x-xsrf-token": self.client.cookies.get("XSRF-TOKEN")[:-3] + "=",
        }

        self.email = None

    def get_mail(self):
        response = self.client.post(
            "https://www.emailnator.com/generate-email",
            json={
                "email": [
                    "domain",
                    "plusGmail",
                    "dotGmail",
                ]
            },
        )

        self.email = loads(response.text)["email"][0]
        return self.email

    def get_message(self):
        print("Waiting for message...")

        while True:
            sleep(2)
            mail_token = self.client.post("https://www.emailnator.com/message-list", json={"email": self.email})

            mail_token = loads(mail_token.text)["messageData"]

            if len(mail_token) == 2:
                print("Message received!")
                print(mail_token[1]["messageID"])
                break

        mail_context = self.client.post(
            "https://www.emailnator.com/message-list",
            json={
                "email": self.email,
                "messageID": mail_token[1]["messageID"],
            },
        )

        return mail_context.text

    def get_verification_code(self):
        message = self.get_message()
        code = findall(r';">(\d{6,7})</div>', message)[0]
        print(f"Verification code: {code}")
        return code

    def clear_inbox(self):
        print("Clearing inbox...")
        self.client.post(
            "https://www.emailnator.com/delete-all",
            json={"email": self.email},
        )
        print("Inbox cleared!")

    def __del__(self):
        if self.email:
            self.clear_inbox()

    @staticmethod
    @retry(
        wait_fixed=5000,
        stop_max_attempt_number=5,
        retry_on_exception=lambda e: isinstance(e, RequestException),
    )
    def __make_request(client: Session) -> Response:
        client.get(f'https://www.emailnator.com/', timeout=6)
        if client.cookies.get("XSRF-TOKEN") is None:
            print('retry')
            raise RequestException('Unable to get the response from server')
        return client.cookies.get("XSRF-TOKEN")

def main():
    mail_client = Emailnator()
    mail_address = mail_client.get_mail()
    print(mail_address)
    # 逻辑
    mail_content = mail_client.get_message()
    print(mail_content)
    # mail_token = findall(r';">(\d{6,7})</div>', mail_content)[0]

import math

def haversine(lat1, lon1, lat2, lon2):  # 纬度1，经度1，纬度2,经度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


if __name__ == '__main__':
    print(haversine(30.3121081,104.0448277,30.3036757,104.0450954),"K.M.")
