import json
import os

from common.RecordLog import log


class HandleJson(object):
    """序列化与反序列化"""
    log.info("开始解析JSON数据")

    @staticmethod
    def json_to_python(json_data):
        """json格式数据转换为python数据"""
        if isinstance(json_data, str):
            python_data = json.loads(json_data)
            log.info("获取Python数据{}".format(python_data))
            return python_data
        else:
            log.error("解析JSON数据失败:parameter:'{}' must be json formatter value".format(json_data))
            raise ValueError('parameter:"{}" must be json formatter value'.format(json_data))

    @staticmethod
    def python_to_json(python_data):
        """python数据转换为json格式数据"""
        if not isinstance(python_data, (str, int, float, bool, set)):
            json_data = json.dumps(python_data)
            return json_data
        else:
            raise ValueError('parameter:"{}" must not be str, int, float, bool, set etc')

    @staticmethod
    def file_json_to_python(filename):
        """读取文件中的json格式数据转换为python数据"""
        if os.path.isfile(filename):
            with open(filename, encoding='utf-8') as f:
                for json_data in f:
                    python_data = json.loads(json_data)
                    yield python_data
        else:
            raise FileNotFoundError('path "{}" does not exist')

    @staticmethod
    def python_to_file_json(filename, python_data):
        """python数据转换为json格式数据并写入文件"""
        if os.path.isfile(filename):
            if not isinstance(python_data, (str, int, float, bool, set)):
                with open(filename, mode='w', encoding='utf-8') as f:
                    json.dump(python_data, f)
            else:
                raise ValueError('parameter:"{}" must not be str, int, float, bool, set etc')
        else:
            raise FileNotFoundError('path "{}" does not exist')


if __name__ == '__main__':
    json_dict = '{"status": 1, "code": "10001"}'
    json_list_dict = '{"status": 1, "code": "10001", "data": [{"id": 80, "name": "linux"}]}'
    print('json格式的数据转换为python数据类型', HandleJson.json_to_python(json_dict))
    print('json格式的数据转换为python数据类型', HandleJson.json_to_python(json_list_dict))
    python_dict = {'code': 1, 'name': 'linux'}
    python_list_dict = ({'code': 1, 'name': 'linux'}, {'data': None, 'name': 'linux'})
    print('python类型的数据转换为json格式', HandleJson.python_to_json(python_dict))
    print('python类型的数据转换为json格式', HandleJson.python_to_json(python_list_dict))

    python_value = HandleJson.file_json_to_python('json_file.txt')
    print('文件中的json格式数据转换为Python数据类型')
    for value in python_value:
        print(value)
    py_value = {"status": 1, "code": "10001", "data": [{"id": 80, "name": "linux"}]}
    print('python数据类型转换为json格式数据并写入文件')
    HandleJson.python_to_file_json('python_file.txt', py_value)
