# Wahl des Jugendwort 2020

https://www.langenscheidt.com/jugendwort-des-jahres

Standardmäßige Proxyquelle: https://api.proxyscrape.com


### Die Seite nutzt reCAPTCHA; wie kann dann eine automatisierte Abstimmung ohne Captcha-Service erfolgen?

Die POST-Anfrage mit dem gewählten Wort und dem Alter des Wählers erwartet Informationen über das Captcha, allerdings ist dieses (scheinbar) fehlerhaft implementiert; verlangt wird nur der Token des Captchas (welcher selbst nicht überprüft wird), ohne dieses gelöst zu haben:

```python
# Generierung eines Tokens der Länge 1422
token = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1422))

...

# POST an "https://woerterbuch.langenscheidt.de/js20/top10/vote" mit folgendem Body:
{
  "age": ..., # Altersslot [1;4]
  "w": ..., # Index des Wortes (nach Auflistung)
  "consent": "1", # Zustimmung
  "g-recaptcha-response": token # Generierter Token
}            
```

