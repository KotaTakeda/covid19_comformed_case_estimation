# 汎用関数を定義

# サイトにアクセス
from bs4 import BeautifulSoup

# pdfダウンロードreq
import urllib
import urllib.request as req

from urllib.parse import urljoin

# pdf から表取得 -> csv
import tabula

import csv

import pandas as pd

# matchを使う
import re

# 定数
REPOERT_COLUMNS = ['Reporting Country/ Territory/Area', 
           'Total conformed cases',
           'Total conformed new cases',
           'Total deaths',
           'Total new deaths',
           'Transmission classification',
           'Days since last reported case']

def scraping_href(site_url):
    # requestを送る who_sitrep_url -> scraping_result
    res = req.urlopen(site_url)

    soup = BeautifulSoup(res, "html.parser")
    scraping_result = soup.select("a[href]")
    return scraping_result

def extract_pdf_urls(scraping_result):
    # urlを取り出す scraping_result -> urls
    urls = [link.get('href') for link in scraping_result ]

    # hrefが相対パスになっているので絶対パスに変更する  urls ->  full_urls
    base = 'https://www.who.int/'
    full_urls = []

    for url in urls:
        url_1 = urljoin(base, url)
        full_urls.append(url_1)

    # 　pdfに限定し?以降のクエリを除去  full_urls -> urls_for_pdf
    urls_for_pdf = [url.split('?')[0] for url in full_urls if 'pdf' in url]

    # sort 
    urls_for_pdf = sorted(set(urls_for_pdf), key=urls_for_pdf.index)
    
    return urls_for_pdf


# pdf ダウンロード
def download_pdf(url):
    path_for_save = 'who_situation_reports/pdf/' + url.split('/')[-1]
    urllib.request.urlretrieve(url, path_for_save)
    return path_for_save
    
def pdf_into_csv(path_for_save_pdf):
    path_for_save_csv = path_for_save_pdf.replace('pdf','csv')
    tabula.convert_into(path_for_save_pdf, path_for_save_csv, output_format="csv", pages='all')
    return path_for_save_csv

def cast2int(x):
    if x is None:
        return ''
#     return int(x.replace(' ',''))
    return x.replace(' ','')

def write_to_master_csv(save_csv_path, master_csv_path):
    date = get_date_from_str(save_csv_path)
    
    with open(save_csv_path) as f:
        rows = [row for row in csv.reader(f)]
    df = pd.DataFrame(rows)
    
    master_df = pd.read_csv(master_csv_path,  index_col=0)
    n = len(master_df.columns)
    print('n: '.format(n))
    print(len(df.iloc[-1,1:1+n]))
    written_list = extend_list(df.iloc[-1,1:1+n].apply(cast2int).to_list(), n)
    master_df.loc[date] = written_list
    master_df.to_csv(master_csv_path)
    return written_list

def extend_list(l, l_size):
    if len(l) >= l_size:
        return l
    extra = [None]*(l_size - len(l))
    l.extend(extra)
    return l

# 現在不使用
def cleaning_csv(path_for_save_csv):
    with open(path_for_save_csv) as f:
        rows = [row for row in csv.reader(f)]
    
    df = pd.DataFrame(rows)
    cleaned_df = df.drop(index = range(40), columns = range(7,18)) # 40と7については検討
    
    # index, column 設定
    cleaned_df.columns = REPOERT_COLUMNS
    cleaned_df = cleaned_df.set_index(REPOERT_COLUMNS[0])
    
    # 各日のcsvを保存
    cleaned_df.to_csv(path_for_save_csv)
    return cleaned_df


def get_date_from_str(str):
#     '2020XXXX'の形式で書かれているのも限定
    result = re.search(r'2020....',str)
    start, end = result.start(), result.end()
    return str[start:end]
