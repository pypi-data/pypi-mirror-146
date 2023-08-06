# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/01/07

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'PW': {
        'code': 'pw',
        'name': '密码',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'make_pw', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'TP': {
        'code': 'tp',
        'name': '时间标签',
        'length': 10,
        'de_plug': [
            {'code': 'tp_time', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'make_tp', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'link_state',
        'name': '链路状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_link_state', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'water_quality_params',
        'name': '水质参数种类',
        'length': 10,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'WT',
        'name': '水温(℃)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'PH',
        'name': 'PH',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'DO',
        'name': '溶解氧(mg/L)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'EC',
        'name': '电导率(μs/cm)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'TD',
        'name': '浊度(NTU)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'COD',
        'name': '化学需氧量(mg/L)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'AN',
        'name': '氨氮(mg/L)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'TN',
        'name': '总氮(mg/L)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'TP',
        'name': '总磷(mg/L)',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_1000', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'work_state',
        'name': '工作状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_work_state', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '02': {
        'name': '链路检测',
        'type': '上行',
        'default': ['0001'],
        'element': [],
        'type_dict': {}
    },
    'C0': {
        'name': '自报实时数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            'A': {
                'name': '水质实时数据',
                'element': ['0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011'],
            }
        }
    },
    '81': {
        'name': '随机自报报警数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '02': {
        'name': '链路检测',
        'type': '响应',
        'default': ['0001'],
        'element': [],
        'type_dict': {}
    },
    'C0': {
        'name': '自报实时数据',
        'type': '响应',
        'default': [],
        'element': [],
        'type_dict': {
            'A': {
                'name': '水质参数',
                'element': ['0012'],
            }
        }
    },
    '81': {
        'name': '随机自报报警数据',
        'type': '响应',
        'default': ['0012'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['C0_A']

# 配置的CLASS
__CLASS__ = 'LTQWQMSettingInfo'


class LTQWQMSettingInfo(object):
    """
    利通区水质监测协议配置信息
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
        code_1, code_2 = command.split('_')
        if code_1 in self.__device_2_platform.keys():
            default = [self.__element_dict[item] for item in self.__device_2_platform[code_1]['default']]
            if code_2 in self.__device_2_platform[code_1]['type_dict'].keys():
                element = [self.__element_dict[item] for item in
                           self.__device_2_platform[code_1]['type_dict'][code_2]['element']]
                return default + element
            else:
                return default
        else:
            return []

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台发出报文的协议字典
        :param command:
        :return:
        """
        code_1, code_2 = command.split('_')
        if code_1 in self.__platform_2_device.keys():
            default = [self.__element_dict[item] for item in self.__platform_2_device[code_1]['default']]
            if code_2 in self.__platform_2_device[code_1]['type_dict'].keys():
                element = [self.__element_dict[item] for item in
                           self.__platform_2_device[code_1]['type_dict'][code_2]['element']]
                return default + element
            else:
                return default
        else:
            return []


if __name__ == '__main__':
    setting_info = LTQWQMSettingInfo()
    print(setting_info.get_device_2_platform_protocol_dict('C0_A'))
    print(setting_info.get_platform_2_device_protocol_dict('C0_A'))
