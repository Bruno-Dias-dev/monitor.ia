import requests 
import panda as pd

url = "https://grupocontem2-my.sharepoint.com/:x:/g/personal/bdias_grupocontem_com_br/IQAGOtELhnlgTJDP5fKTJw4OARuQhvTlUzKV1ljEx8YH5jk?e=u03WBe.xls"


response = requests.get(url)

print(response.status_code)
print(response.url)