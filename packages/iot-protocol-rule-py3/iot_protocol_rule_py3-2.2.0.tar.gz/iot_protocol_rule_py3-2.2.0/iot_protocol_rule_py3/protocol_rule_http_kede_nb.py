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
    '1': {
        'code': 'wsImei',
        'name': u'水表imei',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2': {
        'code': 'wsImsi',
        'name': u'水表imsi',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3': {
        'code': 'createDate',
        'name': u'上传时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4': {
        'code': 'wsCsq',
        'name': u'信号质量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5': {
        'code': 'wsBatteryvoltage',
        'name': u'电池电压',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '6': {
        'code': 'wsCumulativeamount',
        'name': u'累计水量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '7': {
        'code': 'valveStatus',
        'name': u'阀门状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8': {
        'code': 'uuid',
        'name': u'命令id',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9': {
        'code': 'key',
        'name': u'验证key值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10': {
        'code': 'imei',
        'name': u'设备的imei号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11': {
        'code': 'valveControlType',
        'name': u'开关阀',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'list': {
        'name': u'批量查询',
        'type': '应答',
        'default': [],
        'element': ['1', '2', '3', '4', '5', '6', '7'],
        'type_dict': {}
    },
    'valveControl': {
        'name': u'远程控制',
        'type': '应答',
        'default': [],
        'element': ['8', ],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'list': {
        'name': u'远程抄表_批量',
        'type': '上行',
        'default': [],
        'element': ['9'],
        'type_dict': {}
    },
    'valveControl': {
        'name': u'远程控制',
        'type': '上行',
        'default': [],
        'element': ['9', '10', '11'],
        'type_dict': {}
    }
}

IS_SAVE_LIST = ['list']
# 配置的CLASS
__CLASS__ = 'KedeNbWaterMeterSettingInfo'


class KedeNbWaterMeterSettingInfo(object):
    """
    获取明牛协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__root_url = 'http://39.103.139.179:21001/static/kddz/kd_WatermeterCollectionrecord/'
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

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param protocol:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
        else:
            return []


if __name__ == '__main__':
    print(ELEMENT_DICT.keys())
