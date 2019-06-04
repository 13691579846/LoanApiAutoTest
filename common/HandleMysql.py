"""
------------------------------------
@Time : 2019/5/30 11:36
@Auth : linux超
@File : HandleMysql.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import random
import string
import pymysql
from collections.abc import Iterable

from common.ParseConfig import do_conf
from common.RecordLog import log


class HandleMysql(object):
    def __init__(self):
        log.info('初始化数据库...')
        try:
            log.info('start connecting MySQL...')
            self._conn = pymysql.connect(host=do_conf('MySQL', 'Host'),
                                         user=do_conf('MySQL', 'User'),
                                         password=do_conf('MySQL', 'PassWord'),
                                         db=do_conf('MySQL', 'Db'),
                                         port=do_conf('MySQL', 'Port'),
                                         charset=do_conf('MySQL', 'Charset'),
                                         cursorclass=pymysql.cursors.DictCursor
                                         )
        except Exception as e:
            log.error('连接数据库失败\n错误信息如下\n'.format(e))
        else:
            log.info('连接数据库成功')
            self._cursor = self._conn.cursor()

    def get_values(self, sql, args=None, is_all=False):
        if isinstance(args, Iterable) or args is None:
            if self._conn:
                self._cursor.execute(sql, args=args)
                log.info('执行SQL语句:{}'.format(sql))
                self._conn.commit()
                if isinstance(is_all, bool):
                    if is_all:
                        values = self._cursor.fetchall()
                        log.info("拉取数据库部分数据：\n{}".format(values[0]))
                    else:
                        values = self._cursor.fetchone()
                        log.info("拉取数据库数据：\n{}".format(values))
                    return values
                else:
                    log.error('got values error: default parameter "{}" must be bool'.format(is_all))
                    raise TypeError('default parameter "{}" must be bool'.format(is_all))
            else:
                log.error('due to the db connect failed, so get values error!')
                raise ConnectionError('db connect failed get values error!')
        else:
            log.error('got values error: default parameter args "{}" must be Iterable'.format(args))
            raise TypeError('default parameter args "{}" must be Iterable'.format(args))

    def __call__(self, sql, args=None, is_all=False):
        return self.get_values(sql, args=args, is_all=is_all)

    @staticmethod
    def random_phone_num():
        """随机一个电话号码"""
        num_start = ['134', '135', '136', '137', '138',
                     '139', '150', '151', '152', '158',
                     '159', '157', '182', '187', '188',
                     '147', '130', '131', '132', '155',
                     '156', '185', '186', '133', '153',
                     '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits, 8))
        phone_number = start + end
        return phone_number

    def is_exist_phone(self, phone):
        """判断电话号码是否存在数据库中"""
        select_phone_sql = "select MobilePhone from member where MobilePhone=%s;"
        exist = self.get_values(sql=select_phone_sql, args=(phone, ))
        if exist:
            return True
        else:
            return False

    def get_not_exist_phone(self):
        """生成未注册的手机号"""
        while 1:
            phone = self.random_phone_num()
            if not self.is_exist_phone(phone):
                break
        return phone

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
        log.info('关闭数据库...')


if __name__ == '__main__':
    sql_ = "SELECT MobilePhone FROM member;"
    mysql = HandleMysql()
    print(mysql.get_values(sql_))
    print('未注册的手机号', type(mysql.get_not_exist_phone()))
    mysql.close()
