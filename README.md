# Wahl des Jugendwort 2020

https://www.langenscheidt.com/jugendwort-des-jahres

Standardmäßige Proxyquelle: https://api.proxyscrape.com


### Die Seite nutzt reCAPTCHA; wie kann dann eine automatisierte Abstimmung ohne Captcha-Service erfolgen?

Die POST-Anfrage mit dem gewählten Wort und dem Alter des Wählers erwartet Informationen über das Captcha, allerdings ist dieses (scheinbar) fehlerhaft implementiert; verlangt wird nur der Token des Captchas, welcher einfach auszulesen ist:

```python
# Captcha der Abstimmungsseite
r = requests.get("https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lf5zMAZAAAAAKgTZritepo-zKuRStlrPa06Ts4l&co=aHR0cHM6Ly93b2VydGVyYnVjaC5sYW5nZW5zY2hlaWR0LmRlOjQ0Mw..&hl=de&v=QVh-Tz10ahidjrORgXOS1oB0&size=normal&cb=kdrj353l3ddq")

# parsen
soup = BeautifulSoup(captcha.text, "html.parser")
token = soup.find("input", {"id": "recaptcha-token"})["value"]

...

# POST an "https://woerterbuch.langenscheidt.de/js20/top10/vote" mit folgendem Body:
{
  "age": ..., # Altersslot [1;4]
  "w": ..., # Index des Wortes (nach Auflistung)
  "consent": "1", # Zustimmung
  "g-recaptcha-response": token # Token des Captchas
}            
```

