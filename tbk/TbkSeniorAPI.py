# -*- coding:utf-8 -*-

import json
import top.api
import re
from .loggingset import create_logger
Loger = create_logger()

class tbk():
    def __init__(self):
        
        self.appkey = '24570272'
        self.secret = '8527af97d41b62c19fc2df11ff3b4633'
        self.api_url = 'gw.api.taobao.com'

        self.baseURL = 'https://uland.taobao.com/coupon/edetail?'
        
    # 获取淘口令
    def getTpwd(self, text, link_url):
        
        req = top.api.TbkTpwdCreateRequest(self.api_url)
        req.set_app_info(top.appinfo(self.appkey, self.secret))
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
    def getTrueURL(self, url):
        _refer = requests.get(url).url
        headers = {'Referer': _refer}
        return requests.get(urllib.parse.unquote(_refer.split('tu=')[1]), headers=headers).url.split('&ali_trackid=')[0]

    # 获取商品信息
    def getCommodityInfo(self, item_id):
        req = top.api.TbkItemInfoGetRequest(self.api_url)
        req.set_app_info(top.appinfo(self.appkey, self.secret))
 
        req.fields = "num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url"
        req.platform = 1
        req.num_iids = item_id
        try:

            resp= req.getResponse()

#            reqJson = json.loads(resp)
            item_info = resp['tbk_item_info_get_response']['results']['n_tbk_item'][0]

            pic = item_info['pict_url']# 图片
            location = item_info['provcity']# 产地
            title = item_info['title']# 原始标题
            item_url = item_info['item_url']

            print(item_info)
            dic = {}
            dic['pic'] = pic
            dic['location'] = location
            dic['title'] = title
            dic['item_url'] = item_url
            
            return dic
        except Exception as e:
            print(e)
            return False
        

    # 获取item id
    def getItemID(self, relatedURL):
        matchObj = re.findall(r'.*id=(.*).*', relatedURL)
        if not matchObj:
            return False
        itemID = matchObj[0]
        return itemID
        
    #将采集群发送的url,提取相关的id,并转换为券链接
    def conver_url(self, coupon_url, itemID, pid):
        # 从coupon中提取activityID
        Loger.info(coupon_url)
        activityId = ''
        matchObj = re.findall(r'.*activityId=(.*)&.*', coupon_url)
        if not matchObj:
            matchObj = re.findall(r'.*activityId=(.*)', coupon_url)
            if not matchObj:
                matchObj = re.findall(r'.*activity_id=(.*)', coupon_url)
            else:
                Loger.info('error of conver_url')
        Loger.info(matchObj)
        activityId = matchObj[0]

        # 构造url
        finaly_url = self.baseURL + 'activityId=' + activityId + '&pid=' + pid + '&itemId=' + itemID + '&af=1'#+ '&src=pgy_pgyqf&dx=1'
                
        Loger.info(finaly_url)
        return finaly_url
