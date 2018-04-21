# -*- coding:utf-8 -*-

import json
import top.api
import re
from .loggingset import create_logger
Loger = create_logger()


class TBK:
    def __init__(self):
        
        self.app_key = '24570272'
        self.secret = '8527af97d41b62c19fc2df11ff3b4633'
        self.api_url = 'gw.api.taobao.com'

        self.baseURL = 'https://uland.taobao.com/coupon/edetail?'
        
    # 获取淘口令
    def get_tpwd(self, text, link_url):
        req = top.api.TbkTpwdCreateRequest(self.api_url)
        req.set_app_info(top.appinfo(self.app_key, self.secret))
        req.text = text
        req.url = link_url
        print(text)
        print(link_url)
        try:
            resp= req.getResponse()
            print(resp)
            model = resp['tbk_tpwd_create_response']['data']['model']
            return model
        except Exception as e:
            print(e)
            return False

    # 获取跳转后地址
    def get_true_url(self, url):
        _refer = requests.get(url).url
        headers = {'Referer': _refer}
        return requests.get(urllib.parse.unquote(_refer.split('tu=')[1]), headers=headers).url.split('&ali_trackid=')[0]

    # 获取优惠券详细信息
    def get_coupon_info(self, item_id, activity_id):
        req = top.api.TbkCouponGetRequest(self.api_url)
        req.set_app_info(top.appinfo(self.app_key, self.secret))

        req.item_id = item_id
        req.activity_id = activity_id

        print('item id:', item_id)
        print('activity id:', activity_id)

        try:
            resq = req.getResponse()
            print(resq)
            model = resq['tbk_coupon_get_response']['data']
            return model
        except Exception as e:
            print(e)
            return False

    # 获取商品信息
    def get_commodity_info(self, item_id):
        req = top.api.TbkItemInfoGetRequest(self.api_url)
        req.set_app_info(top.appinfo(self.app_key, self.secret))
 
        req.fields = "num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,cat_leaf_name,cat_name,nick"
        req.platform = 1
        req.num_iids = item_id
        try:

            resp = req.getResponse()

#            reqJson = json.loads(resp)
            item_info = resp['tbk_item_info_get_response']['results']['n_tbk_item'][0]

            print('log out')
            print(item_info)
            return item_info
        except Exception as e:
            print(e)
            return False
        
    # 获取item id
    def get_item_id(self, related_url):
        match_obj = re.findall(r'.*id=(.*).*', related_url)
        if not match_obj:
            return False
        item_id = match_obj[0]
        return item_id
        
    # 将采集群发送的url,提取相关的id,并转换为券链接
    def convert_url(self, coupon_url, item_id, pid):
        # 从coupon中提取activityID
        Loger.info(coupon_url)

        match_obj = re.findall(r'.*activityId=(.*)&.*', coupon_url)
        Loger.info(match_obj)
        if not match_obj:
            Loger.info('not 1')
            match_obj = re.findall(r'.*activityId=(.*)', coupon_url)
            if not match_obj:
                Loger.info('not 2')
                match_obj = re.findall(r'.*activity_id=(.*)', coupon_url)
            else:
                Loger.info('error of convert_url')
        Loger.info(match_obj)
        activity_id = match_obj[0]

        return self.baseURL, activity_id

