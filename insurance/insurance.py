#encoding=utf-8
import requests, time, random, argparse, threading
from lxml import etree

class InsuranceScraper(threading.Thread):
    def __init__(self, debug=False):
        threading.Thread.__init__(self)
        self.item_set = set()
        self.urls = []
        self.xpath = ''
        self.interval = 3600
        self.debug = debug

    def clean_func(self):
        return []

    def scrap_once(self, init=False):
        ss = requests.Session()
        for url in self.urls:
            r = ss.get(url, params={})
            r.encoding = 'utf-8'
            selector = etree.HTML(r.text)
            new_set = set(self.clean_func(selector.xpath(self.xpath)))
            diff_set = new_set - self.item_set
            if self.debug or (not init and diff_set):
                print('new item: {}'.format(new_set))
            self.item_set |= diff_set
            time.sleep(2 + 2 * random.random())

    def run(self):
        self.scrap_once(init=True)
        while True:
            self.scrap_once()
            if self.debug:
                break
            time.sleep(self.interval)


class TaikangScraper(InsuranceScraper):
    def __init__(self, debug):
        super(TaikangScraper, self).__init__(debug)
        self.xpath = '/html/body/div[4]/div[2]/ol//p/text()'
        url_tpl = 'http://tkyl.pension.taikang.com/cms/static/xxplnew/jbxx/cpxx/plcptk/zstk/list{}.html'
        pages = ['_' + str(x) for x in range(2, 5)]
        pages = [''] + pages
        for i in pages:
            self.urls.append(url_tpl.format(i))

    def clean_func(self, l):
        return [s.strip().strip('条款') for s in l]

class NCIScraper(InsuranceScraper):
    def __init__(self, debug):
        super(NCIScraper, self).__init__(debug)
        self.xpath = '/html/body/div[3]/div/div[1]/div[2]/table/tbody' \
                    '//tr/td[position()>=2 and position()<4]/text()'
        url_tpl = 'http://www.newchinalife.com/Channel/{}'
        pages = [2871650, 2871506, 2871366, 2871179, 2871110]
        for i in pages:
            self.urls.append(url_tpl.format(i))

    def clean_func(self, l):
        idx = 0
        res = []
        while idx < len(l) - 1:
            res.append(l[idx] + '-' + l[idx+1])
            idx += 2
        return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, default=False)
    args = parser.parse_args()
    scrapers = [TaikangScraper(args.debug), NCIScraper(args.debug),]
    for scraper in scrapers:
        scraper.start()
    for scraper in scrapers:
        scraper.join()
