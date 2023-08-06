# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/06/17

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'water_level',
        'name': '水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'remote_local_mode',
        'name': '远程现地模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'open_value_1',
        'name': '1#开度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'weight_1',
        'name': '1#荷重',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'open_value_set_1',
        'name': '1#开度设定',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'upper_limit_1',
        'name': '1#上限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'lower_limit_1',
        'name': '1#下限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'open_value_2',
        'name': '2#开度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'weight_2',
        'name': '2#荷重',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'open_value_set_2',
        'name': '2#开度设定',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'upper_limit_2',
        'name': '2#上限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'lower_limit_2',
        'name': '2#下限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'control_no',
        'name': '控制序号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'control_type',
        'name': '控制方式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'control_value',
        'name': '控制值',
        'length': None,
        'de_plug': [],
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
        'default': [],
        'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012'],
        'type_dict': {}
    },
    '10': {
        'name': u'写寄存器响应',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    '03': {
        'name': u'读寄存器上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': u'写寄存器上行',
        'type': '上行',
        'default': [],
        'element': ['013', '014', '015'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'PLCZhongDianGateInfo'


class PLCZhongDianGateInfo(object):
    """
    获取PLC中电闸门配置信息
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


if __name__ == '__main__':
    print(sorted(ELEMENT_DICT.keys()))
