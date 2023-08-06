 #   Copyright (C) 2017-2022  Gavin W
 #   This program is free software: you can redistribute it and/or modify
 #   it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation, either version 3 of the License, or
 #   (at your option) any later version.

 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.

 #   You should have received a copy of the GNU General Public License
 #   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
from cgi import print_form
from rediscluster import RedisCluster
import redis

class RedisHelper:
    def stats(self):
        ret = self.rc.info()
        return ret

    def get_all_keys(self):
        data_keys = self.rc.keys()
        return data_keys

    def type(self,key):
        return self.rc.type(key)

    def connect(self, ip_port, password, db_sn):
        print("connect to redis" + ip_port)
        try:
            ipport = ip_port.split(":")
            if len(password) > 0:
                self.rc = redis.StrictRedis(host=ipport[0],port=ipport[1],db=db_sn,password=password,decode_responses=True)
            else:
                self.rc = redis.StrictRedis(host=ipport[0],port=ipport[1],db=db_sn,decode_responses=True)
            self.rc.client_list()
            return 0
        except redis.ConnectionError as err:
            print(str(err))
            return str(err)

    def connect_cluster(self, ipports, password, db_sn):
        try:
            servers = ipports.split(",")
            list_server = []
            for i in servers:
                ipport = i.split(":")
                list_server.append({"host":ipport[0], "port":ipport[1]})
            print(list_server)
            if len(password) > 0:
                self.rc = RedisCluster(startup_nodes=list_server,password=password,decode_responses=True)
            else:
                self.rc = RedisCluster(startup_nodes=list_server,decode_responses=True)
            self.rc.client_list()
            return 0
        except Exception as err:
            print(str(err))
            return str(err)
    
    def close(self):
        if self.rc is not None:
            self.rc.close()
    
    def scan_iter(self, key):
        vals = self.rc.scan_iter(key)
        return vals

    def scan(self, vfrom, key, count):
        vals = self.rc.scan(vfrom, key, count)
        return vals

    def set(self, key, value, time):
        try:
            if time == 0:
                setRet = self.rc.set(key, value)
            else:
                setRet = self.rc.set(key, value, time)
            return setRet
        except Exception as err:
            print(str(err))
            return str(err)

    def hset(self, key, field, value):
        try:
            setRet = self.rc.hset(key, field, value)
            return setRet
        except Exception as err:
            print(str(err))
            return str(err)
    
    def hmset(self, key, mappings):
        try:
            setRet = self.rc.hmset(key, mappings)
            return setRet
        except Exception as err:
            print(str(err))
            return str(err)

    def lpush(self, key, values):
        try:
            setRet = self.rc.lpush(key, values)
            return setRet
        except Exception as err:
            print(str(err))
            return str(err)

    def hgetall(self, key):
        vals = self.rc.hgetall(key)
        return vals
    
    def lrange(self, key, f,t):
        vals = self.rc.lrange(key,f,t)
        return vals

    def zrange(self, key, f,t):
        vals = self.rc.zrange(key,f,t)
        return vals

    def smembers(self, key):
        vals = self.rc.smembers(key)
        return vals

    def get_multi(self, keys):
        vals = self.rc.mget(keys)
        return vals

    def get(self, key):
        vals = self.rc.get(key)
        return vals

    def delete_multi(self, keys):
        try:
            for k in keys:
                self.rc.delete(k)
            return 1
        except Exception as err:
            print(str(err))
            return str(err)
            
    def xrange(self, key):
        vals = self.rc.xrange(key,"-","+")
        return vals

    def flush(self):
        self.rc.flushall

    def __init__(self):
        self.rc = None