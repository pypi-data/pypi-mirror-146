import json
from os import path

from common.db.handle_db import MysqlDB

from common.data.data_process import DataProcess
from common.file.ReadFile import ReadFile
from common.data.handle_common import req_expr
from common.plugin.data_bus import DataBus
from common.config.config import TEST_DATA_PATH
from common.file.handle_excel import excel_to_list


class FilePlugin(object):
    @classmethod
    def excel_to_dict(self, file_name, sheet, _replace: bool=True, file_path: str=TEST_DATA_PATH):
        """
           读取Excel中特定sheet的数据，按行将数据存入数组datalist[从第二行开始读数据】
           :param data_file:Excel文件目录
           :param sheet:需要读取的sheet名称
           :return:datalist
           """
        DataBus.save_init_data()
        data_list = excel_to_list(path.join(file_path, file_name,), sheet)
        data_list_new = []
        for case_data in data_list:
            # 如果字典数据中case_name与参数一致
            if '是' == str(DataProcess.get_key_dic(case_data, '是否执行')).strip():
                if _replace:
                    data_list_new.append(DataBus.get_data(case_data))
                else:
                    data_list_new.append(case_data)
        return data_list_new

    @classmethod
    def excel_to_list(cls, testData_path, sheet_name: str = '', _replace: bool=True):
        """
        读取excel格式的测试用例,转换成list
        :return: data_list - pytest参数化可用的数据
        """
        DataBus.save_init_data()
        if _replace:
            return DataBus.get_data(ReadFile.get_testcase(testData_path, sheet_name))
        else:
            return ReadFile.get_testcase(testData_path, sheet_name)



    @classmethod
    def load_json(self, file_name, _dict=None, _replace: bool=True, file_path: str=TEST_DATA_PATH):
        """
        把Json模版转换为JSON数据
        :param file_name:
        :param replace:
        :param _dict:
        :param file_path:
        :return:
        """
        DataBus.save_init_data()
        _path = path.join(file_path, file_name,)
        with open(_path, "r") as json_file:
            _json = json.load(json_file)
        if _replace:
            _json = DataBus.get_data(_json, _dict)
        return _json

    @classmethod
    def mysql_load_list_dict(self, _sql=None, _config=None):
        """
        把数据库中的表作为dict
        :param file_name:
        :param replace:
        :param _dict:
        :param file_path:
        :return:
        """
        if _config is None:
            _config = {"host": "10.92.80.147", "db_name": "traffic_test", "port": 3306, "user": "mysql",
                     "password": "test1234"}
        _mysql=MysqlDB(_config)
        _list =_mysql.execute(_sql).fetchall()
        _mysql.close()
        return _list

    @classmethod
    def mysql_load_dict(self, _sql=None, _config=None):
        """
        把数据库中的表作为dict
        :param file_name:
        :param replace:
        :param _dict:
        :param file_path:
        :return:
        """
        if _config is None:
            _config = {"host": "10.92.80.147", "db_name": "traffic_test", "port": 3306, "user": "mysql",
                     "password": "test1234"}
        _mysql = MysqlDB(_config)
        _list = _mysql.execute(_sql).fetchone()
        _mysql.close()
        return _list



if __name__ == '__main__':
    print(FilePlugin.mysql_load_list_dict("select req_id as req from base_test_res")[1])
    # readList = readAllList(filePath, "arrivalBindCase")
    # print(readList)
    # DataBus.set_key("env", "test")
    # DataBus.set_key("test333", "3343434")
    # print(DataBus.get_key('test333'))
    # # sheet_data = FilePlugin.excel_to_list('case_data.xls','Sheet1',False,file_path=CONFIG_PATH)
    # _list = [{'title':'AAAAA','name':'BBBBB'},{'title':'AAAAA1','name':'BBBBB2'},{'title':'AAAAA2','name':'BBBBB2'}]
    # print(FilePlugin.load_json(file_name='test.json',file_path=CONFIG_PATH)[0]['testMeta'])
    # for data in sheet_data:
    #     print(sheet_data[0])
    # print(FilePlugin.excel_to_testcase('case_data.xls',_replace=False))
    # print(req_expr('P0,P3,P2',{'P0':'critical', 'P1':'normal', 'P2':'minor', 'P3':'trivial'}))




