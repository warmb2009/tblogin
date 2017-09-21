# -*- coding:utf-8 -*-

import re
from tbk.TbkItemConvert import *
from tbk.TbkItemConvert import TbkItemConvertCoupon
from tbk.loggingset import create_logger
Loger = create_logger()

#正则表达式获取券链接和商品链接
def get_url(text):
    matchObj = re.findall( r'(.*)领券(.*)抢购(.*https?://[ -~]+.*id=\d{11,12})(.*)', text)
    print(matchObj)
    if matchObj:
        return matchObj
    else:
        matchObj = re.findall( r'(.*)领券(.*)抢购(.*https?://[ -~]+[A-Za_z])(.*)', text)
        if matchObj:
            return matchObj
        else:
            return False
    
def printdic(dic):
    for key in dic.keys():
        Loger.info((key, '-',dic[key]))

def testCommodity(url):
    Loger.info(url)
    f_url = url[0:26]
    Loger.info(f_url)
    if f_url == 'https://s.click.taobao.com':
        url = decodeURL(url)
    return url
#将从QQ群获取的内容转换为券链接和商品链接
def convert(text, pid):
    links = get_url(text)
    if links:
        #获取简单数据
        link = links[0]
        
        title = link[0].strip()
        price = ''
        coupon = link[1].strip()[1:]#优惠券
        commodity = link[2].strip()[1:]#商品
        content = link[3].strip()

        commodity = testCommodity(commodity)
        
        #获取推广链接及商品图片
        promotion_text, img_src = get(commodity)
        
        #将商品加入定向计划 调用全局变量, 传入商品url
        TICC = TbkItemConvertCoupon()
        my_coupon_url, itemID = TICC.conver_url(coupon, commodity, pid)
        
        dic = {}
        dic['itemid'] = itemID
        dic['title'] = title
        dic['price'] = price
        dic['coupon'] = my_coupon_url
        dic['commodity'] = promotion_text
        dic['content'] = content
        dic['imageurl'] = img_src

        printdic(dic)
        return dic
    else:
        return False

    
