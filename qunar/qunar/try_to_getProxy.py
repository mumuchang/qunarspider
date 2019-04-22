from datetime import datetime, timedelta
class ProxyModel(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = self.computeTime(data['ttl'])
        self.proxy = 'http://'+ '%s:%s' % (self.ip, self.port)
        #代理是否已经被拉入黑名单了
        self.blacked = False

    def computeTime(self,milisec):
        secs = milisec/1000
        now = datetime.now()
        expire = now + timedelta(seconds=secs)
        print("过期时间",expire)
        return expire

    @property
    def is_expiring(self):
        now = datetime.now()
        # print(now,self.expire_str,(self.expire_str - now))
        if (self.expire_str - now) < timedelta(seconds=10):
            print("过期")
            return True
        else:
            return False