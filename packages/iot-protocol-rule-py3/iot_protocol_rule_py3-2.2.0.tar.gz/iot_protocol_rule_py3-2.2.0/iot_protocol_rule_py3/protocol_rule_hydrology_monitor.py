# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/05/29

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'order_issue_flow_number',
        'name': u'指令下发流水号',
        'length': 4,
        'de_plug': [
            {'code': 'update_command',
             'params': ['srg_data'],
             'return': [],
             }
        ],
        'en_plug': [
            {'code': 'get_order_issue_flow_number',
             'params': ['msg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': '',
    },
    '0002': {
        'code': 'reporting_time',
        'name': u'发报时间',
        'length': 12,
        'de_plug': [
            {'code': 'hex_time',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'update_command',
             'params': ['srg_data'],
             'return': [],
             }
        ],
        'en_plug': [
            {'code': 'get_report_time',
             'params': ['msg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': '',
    },
    '0003': {
        'code': 'telemetry_station_address',
        'name': u'遥测站地址',
        'length': 14,
        'de_plug': [
            {'code': 'del_4_byte',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '0004': {
        'code': 'telemetry_station_type_code',
        'name': u'遥测站分类码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '0005': {
        'code': 'observe_time',
        'name': u'观测时间',
        'length': 14,
        'de_plug': [
            {'code': 'del_4_byte',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'hex_time',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FF0E': {
        'code': 'day_depth',
        'name': u'日地下水埋深',
        'length': 38,
        'de_plug': [
            {'code': 'hex_float_6',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FF03': {
        'code': 'day_water_temperature',
        'name': u'日水温',
        'length': 26,
        'de_plug': [
            {'code': 'hex_float_4',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '38': {
        'code': 'power_supply_voltage',
        'name': u'电源电压',
        'length': 6,
        'de_plug': [
            {'code': 'hex_float_4',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '32': {
        'name': u'遥测站定时自报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['FF0E', 'FF03', '38'],
        'type_dict': {}
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '32': {
        'name': u'遥测站定时自报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
}

# 入库的命令列表
IS_SAVE_LIST = ['32']

# 配置的CLASS
__CLASS__ = 'HydrologyMonitorSettingInfo'


class HydrologyMonitorSettingInfo(object):
    """
    获取水文监测配置信息
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

    def get_device_2_platform_protocol_dict(self, command):
        """
        获取设备至平台协议字典
        :param protocol:
        :return:
        """
        if command in self.__device_2_platform.keys():
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['default']]
        else:
            return []

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param protocol:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['default']]
        else:
            return []


if __name__ == '__main__':
    pass
