from bs4 import BeautifulSoup
import requests
web_data = requests.get("https://www.lithuania.travel/en/category/what-is-lithuania", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"})
soup = BeautifulSoup(web_data.content, features="html.parser")
news_info = soup.findAll("p")[0]
print(news_info.text)