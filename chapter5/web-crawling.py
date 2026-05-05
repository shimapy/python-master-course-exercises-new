import requests
from bs4 import BeautifulSoup
import csv

try:
    response = requests.get("https://www.tabnak.ir/")
    if response.status_code == 200 :   
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all('a',{'class':'title_main'})
        header = ['Title']
        with open('News_headlines.csv', 'w', encoding='utf8') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(header) 
            csvwriter.writerows(titles) 
    else:
        print("No response received") 
except Exception as e:
    print(str(e))