# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/04/15

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'byte_count',
        'name': '字节个数',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'start_address',
        'name': '起始地址',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'register_count',
        'name': '寄存器数量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'water_quantity_carry_count',
        'name': '累计水量进位次数',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '000D': {
        'code': 'headroom',
        'name': '空高',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '000F': {
        'code': 'surface_velocity',
        'name': '表面流速',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'section_velocity',
        'name': '断面流速',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'water_depth',
        'name': '水深',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'pass_water_area',
        'name': '过水面积',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'water_quantity',
        'name': '累计水量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    '03': {
        'name': u'读寄存器响应',
        'type': '应答',
        'default': ['001'],
        'element': ['0008', '000D', '000F', '0011', '0013', '0015', '0017', '0019'],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    '03': {
        'name': u'读寄存器上行',
        'type': '上行',
        'default': ['002', '003'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'PLCHNQFluviographInfo'


class PLCHNQFluviographInfo(object):
    """
    获取PLC惠农渠水位计配置信息
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
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['default']]
        else:
            return []

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['default']]
        else:
            return []


if __name__ == '__main__':
    print(sorted(ELEMENT_DICT.keys()))
