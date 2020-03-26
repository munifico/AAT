import requests
import re
from bs4 import BeautifulSoup


def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=107301&idx_cd=1073&freq=Y&period=1997:2019"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    td_datas = soup.select("#tr_107301_1 > td")

    treasury_3year = {}
    start_year = 1997

    for number, td_data in enumerate(td_datas):
        treasury_3year[start_year+number] = td_data.text

    print(treasury_3year)

if __name__ == "__main__":
    get_3year_treasury()