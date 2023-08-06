import json

from common.common.constant import Constant

from common.autotest.handle_allure import allure_title, allure_severity, allure_feature, allure_link, allure_story

from common.data.data_process import DataProcess

from common.data.handle_common import req_expr, convert_json


class DataPlugin(object):
    @classmethod
    def convert_json(self, _temp, _replace: bool = True):
        """
        任意的数据类型转换成Json
        :param _temp:
        :param _replace: 是否清洗数据
        :return:
        """
        content = _temp
        if isinstance(_temp, str):
            content = json.loads(content)
        else:
            content = json.dumps(_temp)
        if _replace:
            content = req_expr(content)
        return content

    @classmethod
    def json_convert_dict(self, _json, _replace: bool = True) -> dict:
        """
              Json字符串转换为字典
              :param _json:
              :param _replace: 是否清洗数据
              :return:
              """
        if _replace:
            _json = req_expr(_json)
        return convert_json(_json)

    @classmethod
    def get_key_dic(self,_data, key):
        return DataProcess.get_key_dic(_data,key)

    @classmethod
    def excel_convert_allure(self, data):
        if isinstance(data, dict):
            allure_title(DataProcess.get_key_dic(data,Constant.CASE_TITLE))
            # allure报告用例优先级
            allure_severity(DataProcess.get_key_dic(data,Constant.CASE_PRIORITY))
            # allure报告 用例模块
            allure_feature(DataProcess.get_key_dic(data,Constant.CASE_MODEL))
            if DataProcess.get_key_dic(data,Constant.CASE_LINK) is not None:
                allure_link(DataProcess.get_key_dic(data,Constant.CASE_LINK))
            if DataProcess.get_key_dic(data, Constant.CASE_STORY) is not None:
                allure_story(DataProcess.get_key_dic(data,Constant.CASE_STORY))
        if isinstance(data, list):
            allure_title(list[2])
            # allure报告用例优先级
            allure_severity(list[3])
            # allure报告 用例模块
            allure_feature(list[1])





if __name__ == '__main__':
    str1 = '{"listData": "333","strData": "test python obj 2 json"}'
    print(DataPlugin.convert_json(str1))





