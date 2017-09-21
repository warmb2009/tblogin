# -*- coding:utf-8 -*-

import top.api


class Tpwd():
    def __init__():
        
        self.appkey = '24570272'
        self.secret = '8527af97d41b62c19fc2df11ff3b4633'
        self.url = 'gw.api.taobao.com'     


    def getTpwd(text, link_url):
        
        req = top.api.TbkTpwdCreateRequest(self.url)
        req.set_app_info(top.appinfo(self.appkey, self.secret))


        req.text = text
        req.url = link_url

 
        try:
            resp= req.getResponse()
            print(resp)
        except Exception,e:
            print(e)

    
