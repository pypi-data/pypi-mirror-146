# -*- coding: utf-8 -*-
"""
--------------------------------------------------
    File Name       : protocol_rule_electromagnetic_water_meter.py
    Description     ：
    Author          : mxm
    Created on      : 2020/4/15
    Updated on      : 2020/4/15
--------------------------------------------------
"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'ADDRESS',
        'name': u'模块地址',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'NAME',
        'name': u'模块标识',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'FTOTAL',
        'name': u'正向累积值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'RTOTAL',
        'name': u'反向累积值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'FLOW',
        'name': u'瞬时流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'SPEED',
        'name': u'瞬时流速',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'TUB',
        'name': u'流体电导比',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'ALARM',
        'name': u'报警',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'CSQ',
        'name': u'GPRS 模块信号强度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'TIME',
        'name': u'GPRS 模块采集数据时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'PRESS',
        'name': u'流量计当前管道压力',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'HFLOW',
        'name': u'热量值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'HTOTAL',
        'name': u'热量总量值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'CFLOW',
        'name': u'冷量值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'CTOTAL',
        'name': u'冷量总量值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'ReportData': {
        'name': u'数据上报上行',
        'type': u'上行',
        'default': [],
        'element': [str(index).zfill(3) for index in range(1,12)],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {}

# 入库的命令列表
IS_SAVE_LIST = ['ReportData']

# 配置的CLASS
__CLASS__ = 'EWMSettingsInfo'

class EWMSettingsInfo(object):
    """
    电磁水表配置信息
    """
    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__is_save_list = IS_SAVE_LIST

    def get_element_dict(self):
        """
        获取元素解析字典
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

    def get_device_2_platform_protocol_dict(self):
        """
        设备到平台的协议
        :return:
        """
        return [self.__element_dict[item] for item in self.__device_2_platform['ReportData']['element']]

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


if __name__ == '__main__':
    pass
    setting = EWMSettingsInfo()
    print(setting.get_element_list())
