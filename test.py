import requests

url = 'http://127.0.0.1:5000/'

question=  {"Is the Lat Pulldown considered a strength training activity, and if so, why?"}
data = {'question': question}

requests.post(url, data)