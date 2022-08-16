import requests
import lxml.html

from utils import TLSAdapter, get_file_name


def make_request(url):
    session = requests.sessions.Session()
    session.mount('https://', TLSAdapter())
    try:
        page = session.get(url)
    except Exception:
        print(f'Invalid URL {url!r}. Perhaps you meant http://{url}')
        return
    if page.status_code == 404:
        print('Something went wrong. Please, check your URL address. \n404_NOT_FOUND')
        return None
    return page


def parse(url):
    page = make_request(url)
    if page:
        tree = lxml.html.document_fromstring(page.text)
        text_original = tree.xpath('//*[@id="click_area"]/div//*[@class="original"]/text()')
        text_translate = tree.xpath('//*[@id="click_area"]/div//*[@class="translate"]/text()')
        file_name = get_file_name(url)
        writer(text_original, text_translate, file_name)
    else:
        return


def writer(text_original, text_translate, file_name):
    with open(f'{file_name}.csv', 'w', newline='') as csv_file:
        for i in range(len(text_original)):
            csv_file.write(text_original[i])
            csv_file.write(text_translate[i])
    print(f'Done! File was saved with name "{file_name}.csv"')


if __name__ == '__main__':
    url = input('Please, enter the URL of the song:')
    parse(url)
