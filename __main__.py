import random
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

WORD = "Schabernack"
INDEX = 0  # Index of the word
ATTEMPTS = 100000
WORKERS = 700
SOCKS4_LIST_URL = "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4"


class Voter:
    successCounter = 0
    errorCounter = 0

    def __init__(self, proxy):
        self.proxy = proxy
        self.proxyDict = {
            "http": "socks4://" + proxy,
            "https": "socks4://" + proxy
            }
        self.headers = {
            'Host': 'woerterbuch.langenscheidt.de',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '461',
            'Origin': 'null',
            'Connection': 'keep-alive',
            'Cookie': 'js20=eyJ0b3AxMEFnZUlkeCI6MiwidG9wMTBXb3JkSWR4IjowLCJ0b3AxMENvbnNlbnQiOjEsInZvdGVkVG9wMTAiOjAsInZvdGVkVG9wMTBXb3JkIjoiU2NoYWJlcm5hY2sifQ==; js20.sig=W0UAPnkamc9lOvQRdLP4hJNhdRs',
            # the cookie (signed) is of the format base64("{"top10AgeIdx":<age>,"top10WordIdx":<index>,"top10Consent":1,"votedTop10":<index>,"votedTop10Word":<word>}"); we don't change it since it seems to be only used for validation, not information 
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
            }
        self.data = None

    def prepare(self):
        captcha = requests.get(
            "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lf5zMAZAAAAAKgTZritepo-zKuRStlrPa06Ts4l&co=aHR0cHM6Ly93b2VydGVyYnVjaC5sYW5nZW5zY2hlaWR0LmRlOjQ0Mw..&hl=de&v=QVh-Tz10ahidjrORgXOS1oB0&size=normal&cb=kdrj353l3ddq",
            proxies=self.proxyDict)
        soup = BeautifulSoup(captcha.text, "html.parser")
        token = soup.find("input", {"id": "recaptcha-token"})["value"]
        self.data = {
            "age": 1,
            "w": str(INDEX),
            "consent": "1",
            "g-recaptcha-response": token
            # the voting mechanism doesn't care whether we've solved the captcha or not, sending the captcha's token is enough
            }

    def vote(self):
        r = requests.post("https://woerterbuch.langenscheidt.de/js20/top10/vote", data=self.data, headers=self.headers,
                          proxies=self.proxyDict)
        return "Ehre für's Voten!" in r.text


def vote(proxies):
    try:
        v = Voter(random.choice(proxies))
        v.prepare()
        if v.vote():
            Voter.successCounter += 1
            print("Voted successfully. (" + str(Voter.successCounter) + "/" + str(
                Voter.successCounter + Voter.errorCounter) + ") [" + v.proxy + "]")
            return
    except:
        pass
    Voter.errorCounter += 1
    print("Couldn't vote.      (" + str(Voter.successCounter) + "/" + str(
        Voter.successCounter + Voter.errorCounter) + ") [" + v.proxy + "]")


proxyReq = requests.get(SOCKS4_LIST_URL)
proxies = list(filter(None, proxyReq.text.split("\r\n")))

executor = ThreadPoolExecutor(max_workers=WORKERS)

for i in range(ATTEMPTS):
    executor.submit(vote, proxies)
