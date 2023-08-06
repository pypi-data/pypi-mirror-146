# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/09/23

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'sectionId': {
        'code': 'sectionId',
        'name': u'断面ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'sectionName': {
        'code': 'sectionName',
        'name': u'断面名称',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'waterDepth': {
        'code': 'waterDepth',
        'name': u'水深',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'avgSpeed': {
        'code': 'avgSpeed',
        'name': u'平均水速',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'waterFlow': {
        'code': 'waterFlow',
        'name': u'实时流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'waterConsumer': {
        'code': 'waterConsumer',
        'name': u'累积水量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'reportTime': {
        'code': 'reportTime',
        'name': u'上报时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'appKey': {
        'code': 'appKey',
        'name': u'请求key',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'appSecret': {
        'code': 'appSecret',
        'name': u'请求secret',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'token': {
        'code': 'token',
        'name': u'访问令牌',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'get_token': {
        'name': u'获取token',
        'type': '应答',
        'default': [],
        'element': ['token'],
        'type_dict': {}
    },
    'get_data': {
        'name': u'获取data',
        'type': '应答',
        'default': [],
        'element': ['sectionId', 'sectionName', 'waterDepth', 'avgSpeed', 'waterFlow', 'waterConsumer', 'reportTime'],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'get_token': {
        'name': u'获取token',
        'type': '上行',
        'default': [],
        'element': ['appKey', 'appSecret'],
        'type_dict': {}
    },
    'get_data': {
        'name': u'获取data',
        'type': '上行',
        'default': [],
        'element': ['token'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['get_data']

# 配置的CLASS
__CLASS__ = 'HttpMQFlowMeter'


class HttpMQFlowMeter(object):
    """
    获取HTTP形式明渠流量计协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__is_save_list = IS_SAVE_LIST

    def get_element_dict(self):
        """
        获取元素字典
        :return:
        """
        return self.__element_dict

    def get_device_2_platform(self):
        """
        获取设备至平台协议
        :return:
        """
        return self.__device_2_platform

    def get_platform_2_device(self):
        """
        获取平台至设备协议
        :return:
        """
        return self.__platform_2_device

    def get_save_list(self):
        """
        获取入库的命令列表
        :return:
        """
        return self.__is_save_list


if __name__ == '__main__':
    pass
