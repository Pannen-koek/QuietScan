from ast import parse
import requests as re
import os 
import csv

api_key = os.getenv("API_Key_QS")
api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?keywordSearch=Java%208"
response = re.get(api_url)

print (response.json())
#parseresponse = response.json()
#for item in parseresponse:
#    print(parsepresonse['Total Results'])