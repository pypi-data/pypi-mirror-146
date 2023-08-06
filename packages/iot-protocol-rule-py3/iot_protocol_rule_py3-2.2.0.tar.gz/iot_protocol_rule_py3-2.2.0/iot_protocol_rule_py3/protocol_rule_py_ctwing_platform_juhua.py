# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/09/02

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'current_accumulated_flow',
        'name': '当前累计流量',
        'length': 8,
        'de_plug': [
            {'code': 'high_to_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divide_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'settlement_accumulated_flow',
        'name': '结算日累积流量',
        'length': 8,
        'de_plug': [
            {'code': 'high_to_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divide_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'real_time',
        'name': '实时时间',
        'length': 14,
        'de_plug': [
            {'code': 'high_to_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'meter_state',
        'name': '表计状态',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'signal_strength',
        'name': '信号强度',
        'length': 2,
        'de_plug': [
            {'code': 'signal_transform', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'settlement_accumulated_flow_unit',
        'name': '结算日累积流量_单位',
        'length': 2,
        'de_plug': [
            {'code': 'unit_t', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'current_accumulated_flow_unit',
        'name': '当前累积流量_单位',
        'length': 2,
        'de_plug': [
            {'code': 'unit_t', 'params': ['srg_data'], 'return': ['srg_data']}
         ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divide_by_10000', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '81_1F90': {
        'name': '上报数据',
        'type': '上行',
        'default': [],
        'element': ['0001', '0006', '0002', '0007', '0003', '0004', '0005', '0008'],
        'type_dict': {}
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {}

# 入库的命令列表
IS_SAVE_LIST = ['81_1F90']

# 配置的CLASS
__CLASS__ = 'CtwingJuHuaSettingInfo'


class CtwingJuHuaSettingInfo(object):
    """
    获取 天翼使能平台迈拓水表配置信息
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
        :param command:
        :return:
        """
        if command in self.__device_2_platform.keys():
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['element']]
        else:
            return []

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台发出报文的协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
        else:
            return []


if __name__ == '__main__':
    pass
