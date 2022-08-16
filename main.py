import requests
import lxml.html

from utils import TLSAdapter


def make_request(url):
    session = requests.sessions.Session()
    session.mount('https://', TLSAdapter())
    page = session.get(url)
    if page.status_code == 404:
        print('Something went wrong. Please, check your URL address. /n 404_NOT_FOUND')
        return None
    return page


def parse(url):
    page = make_request(url)
    if page:
        tree = lxml.html.document_fromstring(page.text)
        text_original = tree.xpath('//*[@id="click_area"]/div//*[@class="original"]/text()')
        text_translate = tree.xpath('//*[@id="click_area"]/div//*[@class="translate"]/text()')
        writer(text_original, text_translate)
    else:
        return


def writer(text_original, text_translate):
    with open('text.csv', 'w', newline='') as csv_file:
        for i in range(len(text_original)):
            csv_file.write(text_original[i])
            csv_file.write(text_translate[i])


if __name__ == '__main__':
    url = input('Please, enter the URL of the song:')
    parse(url)
