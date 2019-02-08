#encoding=utf-8
import time, random, sys, argparse
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

import itchat_util

debug = False
interval = 3600
company2item_set = defaultdict(set)

def main():
    itchat_util.init()
    scrap_once(init=True)
    if debug:
        return
    while True:
        scrap_once()
        time.sleep(interval)

def scrap_once(init=False):
    chrome_options = Options()
    if not debug:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # url = 'http://bxjg.circ.gov.cn/web/site0/tab6757/' #TODO get iframe src here
    url = 'http://bxjg.circ.gov.cn/tabid/5253/ctl/ViewOrgList/mid/16658/OrgTypeID/1/Default.aspx?ctlmode=none'
    driver.get(url)
    xpath = '//*[@id="ess_ctr16658_ModuleContent"]/table/tbody/tr[2]/td/table/tbody/tr[position()>=2]//td//a'
    links = driver.find_elements_by_xpath(xpath)
    for link in links:
        link.click()
        # driver.switch_to.window(link.get_attribute("target")) # failed ?
        driver.switch_to.window(driver.window_handles[1])
        xpath1 = '//*[@id="ess_ctr16658_ModuleContent"]/table/tbody/tr[1]/td'
        e = driver.find_elements_by_xpath(xpath1)[0]
        company = e.text
        new_list = list()
        xpath2 = '//*[@id="zoom"]/table/tbody/tr[position()>=2]/td[1]'
        xpath3 = '//*[@id="zoom"]/table/tbody/tr[position()>=2]/td[3]'
        name_elements = driver.find_elements_by_xpath(xpath2)
        type_elements = driver.find_elements_by_xpath(xpath3)
        for n, t in zip(name_elements, type_elements):
            item = n.text + '(' + t.text + ')'
            if item not in company2item_set[company]:
                new_list.append(item)
                company2item_set[company].add(item)
        if debug or (not init and new_list):
            msg = '【自动】' + company + ' 刚刚发布了 '
            msg += ','.join(new_list)
            itchat_util.send_msg_friend(msg, 'Z.')
            print('new item: {}'.format(new_list))
            if debug:
                break
        time.sleep(2 * random.random())
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, default=False)
    args = parser.parse_args()
    debug = args.debug
    main()

