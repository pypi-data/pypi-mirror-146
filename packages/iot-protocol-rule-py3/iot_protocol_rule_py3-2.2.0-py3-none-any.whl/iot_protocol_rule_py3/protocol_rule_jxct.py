# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/15

@author: lxj
"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'humidity',
        'name': '湿度',
        'length': 8,
        'de_plug': [{'code': 'data_decode', 'params': ['msg_data'], 'return': ['msg_data']}
                    ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'temperature',
        'name': '温度',
        'length': 8,
        'de_plug': [{'code': 'data_decode', 'params': ['msg_data'], 'return': ['msg_data']}
                    ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '03': {
        'name': '主动上报',
        'type': '上行',
        'default': [],
        'element': ['0001', '0002'],
        'type_dict': {}
    }

}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {

}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'JxctSettingInfo'


class JxctSettingInfo(object):
    """
    获取全渠道测控一体化协议配置信息
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
