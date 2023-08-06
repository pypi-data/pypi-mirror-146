# coding=utf-8
import redis
from redis.client import Redis
from oyeahz_base.utils import oyeahz_utils
from oyeahz_base.logger.xlogger import logger


# 获取redis实例
def get_redis(host: str, port: int) -> Redis:
    redis.StrictRedis(host=host, port=port, db=0)


# 通过本地配置获取Redis实例
def get_redis_by_local_key(key: str) -> Redis:
    redis = None
    try:
        host = oyeahz_utils.get_local_config(key, 'host')
        port = oyeahz_utils.get_local_config(key, 'port')
        redis = get_redis(host, port)
    except Exception as obj:
        logger.error(obj)
    return redis
