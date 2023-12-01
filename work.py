import requests

url = "https://horoscopeapi-horoscope-v1.p.rapidapi.com/daily"

querystring = {"date":"today","sign":"Aries"}

headers = {
	"X-RapidAPI-Key": "769ff93f38msh7faf739a504ff1bp1c3148jsn049de2287d5d",
	"X-RapidAPI-Host": "horoscopeapi-horoscope-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.text)


# import requests
# from requests.structures import CaseInsensitiveDict
#
# url = "https://divineapi.com/api/1.0/get_daily_horoscope.php"
#
# headers = CaseInsensitiveDict()
# headers["Content-Type"] = "application/x-www-form-urlencoded"
#
# data = "api_key=YOUR_API_KEY&date=YYYY-MM-DD&sign=aries"
#
#
# resp = requests.post(url, headers=headers, data=data)
#
# print(resp.status_code)