import json
import xlsxwriter

import requests
from bs4 import BeautifulSoup


PAGES_COUNT = 10
OUT_FILENAME = 'out.json'
OUT_XLSX_FILENAME = 'out.xlsx'


def dump_to_json(filename, data, **kwargs):
    kwargs.setdefault('ensure_ascii', False)
    kwargs.setdefault('indent', 1)
    
    with open(OUT_FILENAME, 'w') as f:
        json.dump(data, f, **kwargs)


def dump_to_xlsx(filename, data):
    if not len(data):
        return None
    
    with xlsxwriter.Workbook(filename) as workbook:
        ws = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        headers = ['Название товара', 'Цена', 'Ссылка']
        headers.extend(data[0]['techs'].keys())

        for col, h in enumerate(headers):
            ws.write_string(0, col, h, cell_format=bold)

        for row, item in enumerate(data, start=1):
            ws.write_string(row, 0, item['name'])
            ws.write_string(row, 1, item['amount'])
            ws.write_string(row, 2, item['url'])
            for prop_name, prop_value in item['techs'].items():
                col = headers.index(prop_name)
                ws.write_string(row, col, prop_value)


def get_soup(url, **kwargs):
    response = requests.get(url, **kwargs)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
    else:
        soup = None
    return soup


def crawl_products(pages_count):
    urls = []
    fmt = 'https://parsemachine.com/sandbox/catalog/?page={page}'
    
    for page_n in range(1, 1 + pages_count):
        print('page: {}'.format(page_n))
        
        page_url = fmt.format(page=page_n)
        soup = get_soup(page_url)
        if soup is None:
            break

        for tag in soup.select('.product-card .title'):
            href = tag.attrs['href']
            url = 'https://parsemachine.com{}'.format(href)
            urls.append(url)
        
    return urls


def parse_products(urls):
    data = []
    
    for url in urls:
        print('\tproduct: {}'.format(url))
        
        soup = get_soup(url)
        if soup is None:
            break

        name = soup.select_one('#product_name').text.strip()
        amount = soup.select_one('#product_amount').text.strip()
        techs = {}
        for row in soup.select('#characteristics tbody tr'):
            cols = row.select('td')
            cols = [c.text.strip() for c in cols]
            techs[cols[0]] = cols[1]

        item = {
            'name': name,
            'amount': amount,
            'techs': techs,
            'url': url,
        }
        data.append(item)
        
    return data


def main():
    urls = crawl_products(PAGES_COUNT)
    data = parse_products(urls)
    dump_to_json(OUT_FILENAME, data)
    dump_to_xlsx(OUT_XLSX_FILENAME, data)
    


if __name__ == '__main__':
    main()
