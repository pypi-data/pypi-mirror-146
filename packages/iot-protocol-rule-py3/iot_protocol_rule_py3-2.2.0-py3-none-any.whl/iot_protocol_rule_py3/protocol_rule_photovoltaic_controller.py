# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/06/29

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'start_address': {
        'code': 'start_address',
        'name': '寄存器起始地址',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'data_count': {
        'code': 'data_count',
        'name': '数据数量',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0000': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'solar_module_voltage',
        'name': '太阳能组件电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'solar_charging_current',
        'name': '太阳能充电电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'output_current',
        'name': '负载端输出电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'battery_capacity',
        'name': '蓄电池电量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'real_time_power_generation',
        'name': '实时发电功率',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'total_power_generation',
        'name': '累计发电总功率',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '03': {
        'name': '上报',
        'type': '上行',
        'default': [],
        'element': ['0000', '0001', '0002', '0003', '0004', '0005', '0006'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '03': {
        'name': '读寄存器',
        'type': '上行',
        'default': [],
        'element': ['start_address', 'data_count'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'PVControllerSettingInfo'


class PVControllerSettingInfo(object):
    """
    京源协议配置信息
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
