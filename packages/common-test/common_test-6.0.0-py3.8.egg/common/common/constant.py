class Constant(object):
    #重要的
    P0 = 'critical'
    #正常用例
    P1 = 'normal'
    #不太重要
    P2 = 'minor'
    #不重要
    P3 = 'trivial'
    #未查找到内容
    DATA_NO_CONTENT = '在DataBus中未提取到内容!!!'
    RESPONSE_CODE = 'responseCode'

    #用例相关Meta
    CASE_NO = '用例编号'
    CASE_MODEL = '所属模块'
    CASE_TITLE = '用例标题'
    CASE_PRIORITY = '优先级'
    CASE_STATUS = '是否执行'
    CASE_DATA = '请求数据'
    CASE_DATA_TYPE = '数据类型'
    CASE_DATA_METHOD = '请求方式'
    CASE_EXPECTED = '预期结果'


    #数据类型：
    DATA_TYPE_JSON = 'json'
    DATA_TYPE_TEXT = 'text'
    DATA_TYPE_XML = 'xml'
    #Header类型：
    HEADER_CONTENT_TYPE_JSON = '$.common.request_headers'
    HEADER_CONTENT_TYPE_XML = '$.common.request_headers_xml'
    HEADER_CONTENT_TYPE_TEXT = '$.common.request_headers_text'
    HEADER_CONTENT_TYPE_DATA = '$.common.request_headers_data'
    HEADER_CONTENT_TYPE_FORM = '$.common.request_headers_form'





