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
        'code': 'meterId',
        'name': u'仪表编号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2': {
        'code': 'meterNum',
        'name': u'表号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3': {
        'code': 'customerName',
        'name': u'用户姓名',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4': {
        'code': 'lastValue',
        'name': u'最新用量止码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5': {
        'code': 'switchFlag',
        'name': u'阀门状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '6': {
        'code': 'readValueDate',
        'name': u'最新抄表时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '7': {
        'code': 'meterTime',
        'name': u'最新表内时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8': {
        'code': 'areaName',
        'name': u'小区名称',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9': {
        'code': 'customerAddr',
        'name': u'用户地址/装表地址',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10': {
        'code': 'createDate',
        'name': u'仪表建档时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11': {
        'code': 'cTaskId',
        'name': u'客户端阀控任务ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '12': {
        'code': 'sTaskId',
        'name': u'服务端阀控任务ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '13': {
        'code': 'meter_no',
        'name': u'表号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '14': {
        'code': 'result',
        'name': u'任务执行状态码',
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
    '16': {
        'code': 'customer_id',
        'name': u'客户/厂家编号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '17': {
        'code': 'meter_type',
        'name': u'仪表类型',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '18': {
        'code': 'read_type',
        'name': u'抄读方式',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '19': {
        'code': 'cur_page',
        'name': u'请求页码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '20': {
        'code': 'page_size',
        'name': u'单页请求条数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '21': {
        'code': 'client_type',
        'name': u'客户端类型',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '22': {
        'code': 'meter_array',
        'name': u'表号数组',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '23': {
        'code': 'task_body',
        'name': u'任务数组',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '24': {
        'code': 'meter_num',
        'name': u'仪表表号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '25': {
        'code': 'task_id',
        'name': u'任务ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'meterRead': {
        'name': u'批量查询',
        'type': '应答',
        'default': [],
        'element': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'type_dict': {}
    },
    'meterReadSingle': {
        'name': u'远程抄表（单表）',
        'type': '应答',
        'default': [],
        'element': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'type_dict': {}
    },
    'setTask': {
        'name': u'远程控制',
        'type': '应答',
        'default': [],
        'element': ['11', '12', '13', '14', '15'],
        'type_dict': {}
    },
    'taskStatusQuery': {
        'name': u'任务查询',
        'type': '应答',
        'default': [],
        'element': ['11', '12', '13', '14', '15'],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'meterRead': {
        'name': u'远程抄表_批量',
        'type': '上行',
        'default': [],
        'element': ['16', '17', '18', '19', '20', '21'],
        'type_dict': {}
    },
    'meterReadSingle': {
        'name': u'远程抄表_单表',
        'type': '上行',
        'default': [],
        'element': ['16', '17', '18', '22', '21'],
        'type_dict': {}
    },
    'setTask': {
        'name': u'远程控制',
        'type': '上行',
        'default': [],
        'element': ['16', '17', '21', '23'],
        'type_dict': {}
    },
    'taskStatusQuery': {
        'name': u'任务查询',
        'type': '上行',
        'default': [],
        'element': ['16', '17', '24', '25', '21'],
        'type_dict': {}
    }
}

IS_SAVE_LIST = ['meterRead']
# 配置的CLASS
__CLASS__ = 'LongiNbWaterMeterSettingInfo'


class LongiNbWaterMeterSettingInfo(object):
    """
    获取明牛协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__root_url = 'http://www.nxlggmeter.com:40875/api/longi/'
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
