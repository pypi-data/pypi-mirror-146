# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/09/10

@author: gw
"""
import hashlib
import random
import string
import time

# 元素字典
ELEMENT_DICT = {
    'deviceName': {
        'code': 'deviceName',
        'name': u'设备名称',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'timesOn': {
        'code': 'timesOn',
        'name': u'开阀次数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'timesOff': {
        'code': 'timesOff',
        'name': u'关阀次数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'commStatus': {
        'code': 'commStatus',
        'name': u'在线状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'csq': {
        'code': 'csq',
        'name': u'csq',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'val': {
        'code': 'val',
        'name': u'开关状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'valflagUpdate': {
        'code': 'valflagUpdate',
        'name': u'开关状态同步',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'powerType': {
        'code': 'powerType',
        'name': u'电池类型',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'powerLevel': {
        'code': 'powerLevel',
        'name': u'电池电量级别',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'ioport': {
        'code': 'ioport',
        'name': u'雨量开关状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'txt': {
        'code': 'txt',
        'name': u'阀门当前状态文字描述',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'logCfg': {
        'code': 'logCfg',
        'name': u'工作模式的文字描述',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'paraCfg': {
        'code': 'paraCfg',
        'name': u'工作模式参数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'paraCfgflagUpdate': {
        'code': 'paraCfgflagUpdate',
        'name': u'工作模式同步的标识',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'programCfg': {
        'code': 'programCfg',
        'name': u'程序配置信息',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'programCfgflagUpdate': {
        'code': 'programCfgflagUpdate',
        'name': u'程序同步的标识',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'userright': {
        'code': 'userright',
        'name': u'userright',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'token': {
        'code': 'token',
        'name': u'通用令牌',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'username': {
        'code': 'username',
        'name': u'用户名',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'password': {
        'code': 'password',
        'name': u'用户密码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'uuid': {
        'code': 'uuid',
        'name': u'设备id',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'deviceIndex': {
        'code': 'deviceIndex',
        'name': u'设备索引',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'action': {
        'code': 'action',
        'name': u'控制状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'getAppDetail': {
        'name': u'获取变量实时数据',
        'type': '应答',
        'default': [],
        'element': ['deviceName', 'timesOn', 'timesOff', 'commStatus', 'csq', 'val', 'valflagUpdate', 'powerType',
                    'powerLevel', 'ioport', 'deviceIndex', 'txt', 'logCfg', 'paraCfg', 'paraCfgflagUpdate',
                    'programCfg', 'programCfgflagUpdate', 'userright'],
        'type_dict': {}
    },

}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'login': {
        'name': u'获取TOKEN上行',
        'type': '上行',
        'default': [],
        'element': ['username', 'password'],
        'type_dict': {}
    },
    'getDeviceList': {
        'name': u'获取阀控器列表',
        'type': '上行',
        'default': [],
        'element': ['username', 'token'],
        'type_dict': {}
    },
    'getAppDetail': {
        'name': u'获取变量实时数据上行',
        'type': '上行',
        'default': [],
        'element': ['username', 'token', 'uuid'],
        'type_dict': {}
    },
    'operateDevice': {
        'name': u'控制变量上行',
        'type': '上行',
        'default': [],
        'element': ['username', 'token', 'uuid', 'action'],
        'type_dict': {}
    }
}

IS_SAVE_LIST = ['getAppDetail']
# 配置的CLASS
__CLASS__ = 'XingLianYunKeSettingInfo'


class XingLianYunKeSettingInfo(object):
    """
    获取明牛协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__root_url = 'http://101.37.67.158:9083/api/'
        self.__element_dict = ELEMENT_DICT
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__is_save_list = IS_SAVE_LIST

    def get_root_url(self):
        """
        获取请求根路径
        :return:
        """
        return self.__root_url

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

    def get_random(self):
        """
        获取随机6位字母与数字的字符串
        :return:
        """
        return ''.join(random.sample(string.ascii_lowercase + string.digits, 6))

    def get_timestamp(self):
        """
        获取当前时间戳
        :return:
        """
        return str(int(round(time.time() * 1000)))

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
        else:
            return []

    def get_device_2_platform_protocol_dict(self, command):
        """
        获取设备至平台协议字典
        :param protocol:
        :return:
        """
        if command in self.__device_2_platform.keys():
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['element']]
        else:
            return []


if __name__ == '__main__':
    print(ELEMENT_DICT.keys())
