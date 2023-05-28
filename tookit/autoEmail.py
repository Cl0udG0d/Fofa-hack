from json import loads
from re import findall
from time import sleep

from requests import Session

from tookit.fofaUseragent import getFakeUserAgent


class Emailnator:
    def __init__(self) -> None:
        self.client = Session()
        self.client.get("https://www.emailnator.com/", timeout=6)
        self.cookies = self.client.cookies.get_dict()

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

def main():
    mail_client = Emailnator()
    mail_address = mail_client.get_mail()
    print(mail_address)
    # 逻辑
    mail_content = mail_client.get_message()
    mail_token = findall(r';">(\d{6,7})</div>', mail_content)[0]


if __name__ == '__main__':
    main()
