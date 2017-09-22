# -*- coding:utf-8 -*-
import sys
import random
import time
import re
import top.api
import json
import os
import pickle
from .loggingset import create_logger
Loger = create_logger()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import urllib, requests
from urllib import request, parse
from . import wxqr
from pyvirtualdisplay import Display

__all__ = ['get']

_g = None
Loger.info('test the tbk')
#模拟登陆淘宝联盟,并根据发送的商品url,将商品加入计划,并进一步获取商品信息
class TbkItemConvertCommodity():
    def __init__(self):
        Loger.info('数据初始化')
        self.login_url = 'http://pub.alimama.com'
        self.cookies_path = '/home/jeroen/temp/tbk.pkl'
        self.test_url = ''
        self.browser = None

        self.wait_time = 60
        self.wait_short_time = 30
        self.wait_exshort_time = 20
        self.appkdy = '24570272'
        self.secret = '8527af97d41b62c19fc2df11ff3b4633'
        self.api_url = 'gw.api.taobao.com'
        
        self.sended_commodity_url = ''
        
        # 无界面设置
        self.initDisplay()
        self.get(self.login_url)
        
    def get(self, url):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        self.browser.set_window_size(1600, 800)
        hasCookies = False
        if os.path.exists(self.cookies_path):
            self.browser.get(url)
            time.sleep(3)
            hasCookies = True
            old_cookies = pickle.load(open(self.cookies_path, "rb"))
            for cookie in old_cookies:
                self.browser.add_cookie(cookie)
            Loger.info('使用缓存数据登陆')
        time.sleep(2)
        Loger.info('开始加载页面')
        self.browser.get(url)


        Loger.info('登入帐号中.....')

        if hasCookies is False:
            self.loginWithNoCookies()
        else:
            self.loginWithCookies()
        
    def loginWithNoCookies(self):
        Loger.info('无cookies登入')
        try:
            # 等待进入界面
            WebDriverWait(self.browser, self.wait_time).until(
                EC.presence_of_element_located((By.NAME, 'taobaoLoginIfr')))
        except Exception as err:
            Loger.error(err)
            Loger.warn('等待超时')
        self.browser.get_screenshot_as_file('/home/jeroen/image/temp/index.png')
        self.browser.switch_to_frame('taobaoLoginIfr')
        element = self.browser.find_element_by_tag_name('img')
        jpg_link = element.get_attribute('src')
        qr_file_path = 'qrcode.png'
        # 存储二维码登陆图片
        request.urlretrieve(jpg_link, qr_file_path)
        # 显示二维码
        Loger.info('显示二维码')
        qr = wxqr.QRCode()
        qr.showCmdQRCode(qr_file_path)

        try:
            # 等待登陆
            WebDriverWait(self.browser, self.wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'logined-title')))
        except Exception as err:
            self.loginWithNoCookies()
            return

        Loger.info('登陆成功')
        Loger.info('获取cookies信息')
        cookie = self.browser.get_cookies()
        pickle.dump(cookie, open(self.cookies_path, "wb"))
        Loger.info('存储登陆页面')
        self.browser.get_screenshot_as_file('/home/jeroen/image/temp/login_success.png')
    #带cookies登陆网站
    def loginWithCookies(self):        
        try:
            Loger.info('cookie验证....')
            # 等待登陆
            WebDriverWait(self.browser, self.wait_exshort_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'logined-title')))
        except Exception as err:
            self.browser.get_screenshot_as_file('/home/jeroen/image/temp/login_with_cookie.png')
            Loger.info('cookies过期,重新登陆')
            self.loginWithNoCookies()
        Loger.info('登入cookie成功')

    #界面初始设置
    def initDisplay(self):
        display = Display(visible = 0, size = (1600, 900))
        display.start()

    def getItemWithRefresh(self, itemUrl):
        self.browser.get(self.login_url)
        self.getItem(itemUrl)
        
    def getItem(self, itemUrl):
        self.browser.get(self.login_url)
        Loger.info('开始搜索产品')
        #确定搜索输入框
        input_el = self.browser.find_element_by_class_name('search-inp')
        input_el.clear()
        time.sleep(1)
        input_el.send_keys(itemUrl)
        #点击搜索按钮
        btn_el = self.browser.find_element_by_class_name('search-btn')
        btn_el.click()
        Loger.info('搜索产品中.....')
        try:
            #等待页面进入搜索结果页面
            WebDriverWait(self.browser, self.wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-result-wrap')))
        except Exception as err:
            self.getItemWithRefresh(itemUrl)
            return
        Loger.info('产品搜索完毕')
        time.sleep(1)
        #获取产品名称
        el = self.browser.find_element_by_class_name('search-result-wrap')
        a_el = el.find_element_by_class_name('color-m')
        span_el = a_el.find_element_by_tag_name('span')
        Loger.info(('产品名称', span_el.text))

        #获取产品图片
        item_img_el = self.browser.find_element_by_class_name('pic-box')
        img_el = item_img_el.find_element_by_tag_name('img')
        
        img_osrc = img_el.get_attribute('src')
        Loger.info(('原始图片:', img_osrc))
        img_src = img_osrc[:-5] + '.jpg'

        Loger.info('查看是否有优惠券')
        have_coupon = True
        #查看是否有优惠券
        try:
            test = self.browser.find_element_by_class_name('tag-coupon')
        except Exception as err:
            have_coupon = False
        
        #点击立即推广按钮
        box_btn_el = self.browser.find_element_by_class_name('box-btn-left')#获取推广按钮
        time.sleep(random.randint(3, 4))
        Loger.info('滚动页面到底部')
        self.browser.execute_script("window.scrollBy(0,document.body.scrollHeight)","")  #向下滚动到页面底部
        
        box_btn_el.click()
        
        Loger.info('进入推广页面...')
        #等待推广页面刷新
        try:
            WebDriverWait(self.browser, self.wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, 'dialog-ft')))
        except Exception as err:
            self.getItemWithRefresh(itemUrl)
            return
        
        #重定向推广模式
        Loger.info('重新定向推广模式')
        radio_el = self.browser.find_elements_by_name('gcid')[2]
        if not radio_el.is_selected():
            radio_el.click()
    
        #点击推广页面确认按钮
        enter_div_el = self.browser.find_element_by_class_name('dialog-ft')
        enter_el = enter_div_el.find_element_by_tag_name('button')
        Loger.info('确认推广模式,获取推广链接')
        time.sleep(2)
        enter_el.click()

        promotion_text = ''
        if have_coupon:
            try:
                Loger.info('使用有优惠券定位')
                WebDriverWait(self.browser, self.wait_short_time).until(EC.presence_of_element_located((By.ID, 'clipboard-target-1')))
                #获取推广链接
                value_el = self.browser.find_element_by_id('clipboard-target-1')
                promotion_text = value_el.get_attribute('value')
                Loger.info(('商品推广链接:',  promotion_text))

                #关闭推广窗口
                close_div_el = self.browser.find_element_by_class_name('dialog-ft')
                close_el = close_div_el.find_elements_by_tag_name('button')[0]
                Loger.info(close_el.text)
                close_el.click()

            except Exception as err:
                self.getItemWithRefresh(itemUrl)
                return
        else:
            try:
                Loger.info('使用无优惠券定位')
                WebDriverWait(self.browser, self.wait_short_time).until(EC.presence_of_element_located((By.ID, 'code-clipboard')))
            
                #获取推广链接
                textarea_el = self.browser.find_element_by_class_name('textarea')
                promotion_text = textarea_el.text
                Loger.info(('商品推广链接:', promotion_text))

                #关闭推广窗口
                close_div_el = self.browser.find_element_by_class_name('dialog-ft')
                close_el = close_div_el.find_elements_by_tag_name('button')[1]
                close_el.click()

            except Exception as err:
                self.getItemWithRefresh(itemUrl)
        self.browser.get(self.login_url)
        return promotion_text, img_src

    #获取产品图片Url
    def getItemImage(self, itemID):
        req = top.api.TbkItemInfoGetRequest(url)
        req.set_app_info(top.appinfo(appkey,secret))
 
        req.fields = "num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url"
        req.platform = 1
        req.num_iids = itemID
        try:
            resp = req.getResponse()

            respObj = json.load(resp)
            imageUrl = respObj['tbk_item_info_get_response']['results']['n_tbk_item'][0]['small_images']

        except Exception as e:
            Loger.warn(e)
            
    def get_real_taobao(url):
        _refer = requests.get(url).url
        headers = {'Referer': _refer}
        return requests.get(urllib.parse.unquote(_refer.split('tu=')[1]), headers=headers).url.split('&ali_trackid=')[0]
    

    def close(self):
        Loger.warn('关闭链接转换')
        self.browser.quit()

if _g is None:
    _g = TbkItemConvertCommodity()

def get(url):
    return _g.getItem(url)

def decodeURL(url):
    return _g.get_real_taobao(url)
#def init():
#    return _g.__init__()


#获取淘宝优惠券链接
class TbkItemConvertCoupon():
    def __init__(self):
        self.baseURL = 'http://uland.taobao.com/coupon/edetail?'

    #根据相关Id转为需要的淘抢购id
    def conver(self, activityId, itemId, pid):
        url = self.baseURL + 'activityId=' + activityId + '&pid=' + pid + '&itemId=' + itemId + '&src=pgy_pgyqf&dx=1'
        return url

    #将采集群发送的url,提取相关的id,并转换为券链接
    def conver_url(self, coupon_url, commodity_url, pid):
        #从coupon中提取activityID
        Loger.info(coupon_url)
        activityId = ''
        matchObj = re.findall(r'.*activityId=(.*)&.*', coupon_url)
        if len(matchObj) == 0:
            matchObj = re.findall(r'.*activityId=(.*)', coupon_url)
        if len(matchObj) == 0:
            matchObj = re.findall(r'.*activity_id=(.*)', coupon_url)
        Loger.info(matchObj)
        activityId = matchObj[0]
        #从commodity中提取itemID
        matchObj = re.findall(r'.*id=(.*).*', commodity_url)
        itemID = matchObj[0]

        finaly_url = self.conver(activityId, itemID, pid)
        Loger.info(finaly_url)
        return finaly_url, itemID
