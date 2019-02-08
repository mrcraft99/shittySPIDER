#encoding=utf-8
import sys, requests
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait

file_name = ''
xpath = '//*[@id="ess_ctr16658_ModuleContent"]/table/tbody/tr[2]/td/table/tbody//a'
url = 'http://bxjg.circ.gov.cn/tabid/5253/ctl/ViewOrgList/mid/16658/OrgTypeID/1/Default.aspx?ctlmode=none'
selector = etree.HTML(r.text)

def main():
    ss = requests.Session()
    r = ss.get(url, params={})
    r.encoding = 'utf-8'
    with open ('example.html', 'w') as fin:
        fin.write(r.text)
    print(selector.xpath(xpath))

def main_browser():
    #TODO
    driver = webdriver.Chrome()
    driver.get(url)

    with open ('example.html', 'w') as fin:
        fin.write(r.text)
    print(selector.xpath(xpath))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main_browser()
    else:
        main()
