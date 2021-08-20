import os
import pandas as pd
import requests
from requests_html import HTML



absolute_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(absolute_path)

download_path = os.path.join(BASE_DIR, "downloads")
os.makedirs(download_path, exist_ok=True)


def url_to_html(url=None, filename="defualt.html", save=False):
    scrape_url = requests.get(url)
    if scrape_url.status_code == 200:
        html_code = scrape_url.text

        if save == True:
            file_path = os.path.join(download_path, filename)
            with open(filename, "w") as w:
                w.write(html_code)
        return html_code
    return None


def parse_html_to_text(file_name=None):
    url = f"https://www.boxofficemojo.com/year/world/{file_name}/"
    html_code = url_to_html(url)
    if html_code == None:
        return False
    html_link = HTML(html=html_code)
    table_id = "#table"
    table_element = html_link.find(table_id)
    if len(table_element) == 0:
        return False
    table_data = table_element[0].find("tr")
    table_headers = table_element[0].find("th")
    headers = [x.text for x in table_headers]
    dict_row_data = {}
    table_rows_data = []
    for row in table_data[1:]:
        rows_data = row.find("td")
        row_data = []
        for i, ro in enumerate(rows_data):
            header_name = headers[i]
            row_data.append(ro.text)

        table_rows_data.append(row_data)
    csv_path=os.path.join(download_path,f"{file_name}.csv")
    df = pd.DataFrame(table_rows_data, columns=headers)
    df.to_csv(csv_path,index=False)
    return True

def year_range_movies(from_year=None,years_no=None):
    if from_year !=None and from_year <=2021 and from_year>=1971:
        for i in range(0,years_no+1):
            done= parse_html_to_text(from_year)
            if done:
                print(f"{from_year} done!")
            from_year-=1
            
            
