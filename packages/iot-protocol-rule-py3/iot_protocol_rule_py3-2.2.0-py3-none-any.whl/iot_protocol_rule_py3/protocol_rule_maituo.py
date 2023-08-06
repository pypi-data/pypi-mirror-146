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
        'code': 'water',
        'name': u'水表读数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2': {
        'code': 'meterId',
        'name': u'表号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3': {
        'code': 'userId',
        'name': u'用户编码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4': {
        'code': 'valveStatus',
        'name': u'阀门状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5': {
        'code': 'pressure',
        'name': u'压力',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '6': {
        'code': 'reverseWater',
        'name': u'水表反向累计流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '7': {
        'code': 'temperature',
        'name': u'温度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8': {
        'code': 'voltage',
        'name': u'电压',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9': {
        'code': 'meterStatus',
        'name': u'表计状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10': {
        'code': 'imei',
        'name': u'采集器号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11': {
        'code': 'flowrate',
        'name': u'瞬时流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '12': {
        'code': 'datetime',
        'name': u'数据采集时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '13': {
        'code': 'result',
        'name': u'结果',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '14': {
        'code': 'message',
        'name': u'结果描述',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '15': {
        'code': 'message',
        'name': u'任务执行状态信息',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'count': {
        'code': 'count',
        'name': u'请求数量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'type': {
        'code': 'type',
        'name': u'请求类型',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'data': {
        'code': 'data',
        'name': u'水表/用户编号列表',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'checkCode': {
        'code': 'checkCode',
        'name': u'验证码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'datetime': {
        'code': 'datetime',
        'name': u'历史时间戳',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'valve': {
        'code': 'valve',
        'name': u'开关标志',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'findQueryLastData': {
        'name': u'获取当前数据（单表）',
        'type': '应答',
        'default': [],
        'element': ['2', '1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        'type_dict': {}
    },
    'findQueryLastDataByDatetime': {
        'name': u'获取历史数据（单表）',
        'type': '应答',
        'default': [],
        'element': ['2', '1', '3', '4', '5', '6', '7', '8', '9', '11', '12'],
        'type_dict': {}
    },
    'updateOperateValveStatus': {
        'name': u'阀门开关操作',
        'type': '应答',
        'default': [],
        'element': ['13', '14', '4', '3', '2'],
        'type_dict': {}
    },

}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'findQueryLastData': {
        'name': u'获取当前数据',
        'type': '上行',
        'default': [],
        'element': ['count', 'type', 'data', 'checkCode'],
        'type_dict': {}
    },
    'findQueryLastDataByDatetime': {
        'name': u'获取历史数据（单表）',
        'type': '上行',
        'default': [],
        'element': ['count', 'type', 'data', 'datetime', 'checkCode'],
        'type_dict': {}
    },
    'updateOperateValveStatus': {
        'name': u'阀门开关操作',
        'type': '上行',
        'default': [],
        'element': ['count', 'type', 'data', 'valve', 'checkCode'],
        'type_dict': {}
    }
}

IS_SAVE_LIST = ['findQueryLastData']
# 配置的CLASS
__CLASS__ = 'MaiTuoSettingInfo'


class MaiTuoSettingInfo(object):
    """
    获取明牛协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__root_url = 'http://58.240.47.50:8090/EnergyManager/interface/'
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
