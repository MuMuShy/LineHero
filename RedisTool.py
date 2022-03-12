
import redis
from dotenv import load_dotenv
load_dotenv()
from urllib.parse import urlparse
import os

environment = os.getenv("ENVIRONMENT")
url = urlparse(os.environ.get("REDIS_TLS_URL"))

class RedisTool():
    def __init__(self):
        self.connect()
        self._redis.ping()
    
    def connect(self):
        self._redis = redis.Redis(
            host=url.hostname,
            port=url.port,
            password=url.password,
            ssl=True,
            ssl_cert_reqs=None
            )
    
    def setKey(self,key,value):
        try:
            self._redis.ping()
        except:
            self.connect()
        self._redis.set(key,value)
    
    def getValue(self,key):
        try:
            self._redis.ping()
        except:
            self.connect()
        value = self._redis.get(key)
        return value
    
    def removeKey(self,key):
        try:
            self._redis.ping()
        except:
            self.connect()
        self._redis.delete(key)




if __name__ == "__main__":
    #r = Redis()
    # r.setKey("list","dddd")
    # print(r.getKey("list"))
    r = RedisTool()
    r.setKey("hello","word")
    print(r.getValue("123"))
    value = r.getValue("hello")
    if value is not None:
        value = value.decode()
    print("word" == str(value))
    r.removeKey("word")
    r.removeKey("hello")
    value = r.getValue("hello")
    if value is not None:
        value = value.decode()
    print("word" == str(value))