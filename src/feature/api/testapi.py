import requests as re
import os 
import json 

api_key = os.getenv("API_Key_QS")
api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?keywordSearch=Discord"
response = re.get(api_url)

parseresponse = response.json()
pretty_response = json.dumps(parseresponse, indent=4)

#print(pretty_response)


#for item in parseresponse:
    #for item in item[4]:
        #print(item['cve']['CVE_data_meta']['ID'])
    #print(item['publishedDate'])
    #print(item['lastModifiedDate'])
    #print(item['summary'])
    
for item in parseresponse:
    if isinstance(item, list) or isinstance(item, dict):
        for sub_item in item[6]:
            print(sub_item['cve']['id'])
        print(item['publishedDate'])
        print(item['lastModifiedDate'])
        print(item['summary'])
    else:
        print("Invalid item type:", type(item))
