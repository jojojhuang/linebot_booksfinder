# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_soup(url):    
    html = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'})
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

# 透過關鍵字，從博客來爬下搜尋結果
def crawl_books_by_key(key, result_max):
    url  = 'https://search.books.com.tw/search/query/key/{}/cat/BKA'.format(key)    
    soup = get_soup(url)
    
    results = []
    for item in soup.select('.searchbook > .item'):
        url       = 'http:' + item.select_one('h3 > a')['href']
        name      = item.select_one('h3 > a').text.replace('\t', '').replace('\n', '')
        photo_url = item.select_one('img')['data-original'].split('=')[1].split('&')[0]
        
        try:
            authors = ','.join([author.text for author in item.select('a[rel="go_author"]')])
        except:
            authors = ''
        try:
            publisher = item.select_one('a[rel="mid_publish"]').text
        except:
            publisher = ''

        for b in item.select('.price > button'):
            b.decompose()
        price = item.select_one('.price').text.replace('\t', '').replace('\n', '').replace(' ', '')
        try:
            summary = item.select_one('p').text[:-5]
        except:
            summary = ''

        results.append({
            'url'       : url,
            'name'      : name,
            'photo_url' : photo_url,
            'authors'   : authors,
            'publisher' : publisher,
            'price'     : price,
            'summary'   : summary
        })
    if len(results) > result_max:
        results = results[:result_max]
    return results

# 從博客來爬下即時排行榜前 10 名
def crawl_top10():
    soup = get_soup('https://www.books.com.tw/web/sys_hourstop/books')
    top10 = []
    for top in soup.select('ul.clearfix > li.item')[:10]:
        no        = top.select_one('.no').text
        url       = top.select_one('a')['href']
        name      = top.select_one('img')['alt']
        photo_url = 'https:' + top.select_one('img')['src']
        authors   = top.select_one('.msg > li > a').text
        price     = top.select_one('.price_a').text

        top10.append({
            'no'        : no,
            'url'       : url,
            'name'      : name,
            'photo_url' : photo_url,
            'authors'   : authors,
            'price'     : price
        })    
    return top10