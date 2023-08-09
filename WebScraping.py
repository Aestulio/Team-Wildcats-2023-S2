import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table_to_dataframe(url, table_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': table_class})

    if table is None:
        return None


    data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.get_text(strip=True))
        data.append(row_data)

    headers = data[0]
    data = data[1:]

    df = pd.DataFrame(data, columns=headers)
    return df

table_class = 'tablesaw'

start_year = 2017
end_year = 2023
stat_types = ['Advanced_Stats', 'Averages'] # as they appear in the URL

# Base URLs
leagues = [
    {"name": "Japanese-BLeague", "url": "https://basketball.realgm.com/international/league/105/Japanese-BLeague/stats", "format": 1},
    {"name": "French-Jeep-Elite", "url": "https://basketball.realgm.com/international/league/12/French-Jeep-Elite/stats", "format": 1},
    {"name": "German-BBL", "url": "https://basketball.realgm.com/international/league/15/German-BBL/stats", "format": 1},
    {"name": "Spanish-ACB", "url": "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats", "format": 1},
    {"name": "Turkish-BSL", "url": "https://basketball.realgm.com/international/league/7/Turkish-BSL/stats", "format": 1},
    {"name": "gleague", "url": "https://basketball.realgm.com/dleague/stats", "format": 2}
]

for league in leagues:
    for type in stat_types:
        big_dataframe = pd.DataFrame()
        for year in range(start_year, end_year + 1):
            print(year, league["name"])
            
            page_num = 1
            while True:
                if league["format"] == 1:
                    url = f'{league["url"]}/{year}/{type}/Qualified/All/points/All/desc/{page_num}/Regular_Season'
                elif league["format"] == 2:
                    url = f'{league["url"]}/{year}/{type}/Qualified/points/All/desc/{page_num}/Regular_Season'
                
                print("\t", type, page_num)
                resulting_dataframe = scrape_table_to_dataframe(url, table_class)
                if resulting_dataframe is None or resulting_dataframe.empty:
                    break

                resulting_dataframe['year'] = year
                page_num += 1
                big_dataframe = pd.concat([big_dataframe, resulting_dataframe], ignore_index=True)
        big_dataframe.to_csv(f'{league["name"]}_{type}.csv', index=False)