from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
# from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import Throttled
import random
import time


# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常实例对象
    :param context: 抛出异常的上下文（包含request和view对象）
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)

    if isinstance(exc, Throttled):
        # 生成时间戳和随机salt
        ts = str(int(time.time() * 1000))  # 当前时间的时间戳
        salt_length = random.randint(4, 8)  # 随机数长度为4到8位
        salt = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=salt_length))
        custom_response_data = {
            'msg': '过多请求',
            'ts': ts,
            'salt': salt,
            'code': '0'
        }
        return Response({'data': custom_response_data}, status=429)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            # if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
