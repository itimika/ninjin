# 農林水産省
# https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC002-Evt002.do

# アグリネ
# https://agrine.jp/wholesale-market.php?mrk=14300&dt=2025-04-24

import configparser
import os
from urllib.parse import quote
from scraper import Scraper
from sheet_handler import SheetHandler

def main(url, scraper, sheetHandler):
    item, yasai_name = scraper.run(url)
    if not item:
        print("次のURLからデータを取得できませんでした")
        print(url)
        return 
    
    print("{}の情報".format(yasai_name))
    print(item)
    
    sheetHandler.append_row(yasai_name, item)

if __name__ == '__main__':
    print("開始")
    config = configparser.ConfigParser()
    with open('config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
        
    id_tuples = []
    
    for section in config.sections():
        raw_ids = config.get(section, 'ids')
        # カンマ区切りで分割 → 空要素除去 → 数値変換
        id_list = [int(id.strip()) for id in raw_ids.split(',') if id.strip()]
        id_tuples.append((section, id_list))
    
    print(id_tuples)
    
    sheetHandler = SheetHandler()
    scraper = Scraper()
    
    for t in id_tuples:
        print("種別【{}】".format(t[0]))
        for id in t[1]:
            print("野菜ID：{}を取得中".format(id))
            url = "https://agrine.jp/market.php?ctg={}&itm={}&mrk=14300".format(quote(t[0]), id)
            
            main(url, scraper, sheetHandler)
    
    scraper.close()
    print("完了しました")