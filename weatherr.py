'''import requests
import json
import win32com.client as wincom

speak = wincom.Dispatch("SAPI.SpVoice")

text = f"Please Enter the name of the place:- "
speak.Speak(text)
place=input("Place:- ")
url=f"https://api.weatherapi.com/v1/current.json?key=f46e7a65af84410a8ab174512242701&q={place}"

r=requests.get(url)
dec=json.loads(r.text)
a=dec["current"]["temp_c"]

print(f"Current emperture in {place} is {a} degree celcius. \nThank you")
text = f"current emperture in {place} is {a} degree celcius. \nThank you"
speak.Speak(text)

'''
