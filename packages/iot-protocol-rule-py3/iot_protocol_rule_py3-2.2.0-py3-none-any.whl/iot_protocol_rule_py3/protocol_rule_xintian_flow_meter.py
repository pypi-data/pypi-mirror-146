# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/15

@author: lxj
"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'flow_cumulative',
        'name': '累计流量',
        'length': 8,
        'de_plug': [
            {'code': 'high_low_transform', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'water_meters_forward_unit', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'flow_instantaneous',
        'name': '瞬时流量',
        'length': 8,
        'de_plug': [
            {'code': 'high_low_transform', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'instantaneous_flow_unit', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'pressure',
        'name': '压力',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'terminal_time',
        'name': '终端时间',
        'length': 10,
        'de_plug': [
            {'code': 'high_low_transform', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'hex_time', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'en_plug': [
            {'code': 'terminal_time_to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'high_low_transform', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'terminal_voltage',
        'name': '终端电压',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'terminal_unit', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'signal_strength',
        'name': '信号强度',
        'length': 2,
        'de_plug': [
            {'code': 'bcd_int', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'terminal_version',
        'name': '终端版本信息',
        'length': 10,
        'de_plug': [
            {'code': 'ascii_to_str', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'copy_data_day',
        'name': '抄录数据日',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'alarm_information',
        'name': '告警信息',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'water_meters_forward',
        'name': '水表正向计数',
        'length': 8,
        'de_plug': [
            {'code': 'high_low_transform', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'water_meters_forward_unit', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'date_history_96',
        'name': '96点历史数据',
        'length': 240,
        'de_plug': [
            {'code': 'to_total_flow_96', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'water_meters_reverse',
        'name': '水表反向计数',
        'length': 8,
        'de_plug': [
            {'code': 'high_low_transform', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'water_meters_reverse_unit', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'date_instant_96',
        'name': '96点瞬时数据',
        'length': 240,
        'de_plug': [
            {'code': 'to_instantaneous_flow_96', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'EN': {
        'code': 'EN',
        'name': '使能标志',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'IP': {
        'code': 'IP',
        'name': 'ip地址',
        'length': 8,
        'de_plug': [
            {'code': 'ip_hex_to_ip', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'P': {
        'code': 'port',
        'name': '端口号',
        'length': 4,
        'de_plug': [
            {'code': 'port_hex_to_port', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'APN': {
        'code': 'APN',
        'name': 'apn信息',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '92': {
        'name': '登录帧',
        'type': '上行',
        'default': [],
        'element': ['0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    '93': {
        'name': '心跳帧',
        'type': '上行',
        'default': [],
        'element': ['0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    'B3': {
        'name': '指定日期累积流量',
        'type': '上行',
        'default': [],
        'element': ['0008', '0009', '0010', '0011', '0012', '0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    'B4': {
        'name': '指定日期瞬时流量',
        'type': '上行',
        'default': [],
        'element': ['0008', '0009', '0013', '0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    '85': {
        'name': '终端GPRS数据信息',
        'type': '应答',
        'default': [],
        'element': ['EN', 'IP', 'P', 'APN', '0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    '86': {
        'name': '校时终端信息',
        'type': '应答',
        'default': [],
        'element': ['0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    '87': {
        'name': '终端时钟信息',
        'type': '应答',
        'default': [],
        'element': ['0004', '0005', '0006', '0007'],
        'type_dict': {}
    },
    '9C': {
        'name': '管网实时数据',
        'type': '应答',
        'default': [],
        'element': ['0001', '0002', '0003', '0009', '0004', '0005', '0006', '0007'],
        'type_dict': {}
    },

}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '05': {
        'name': '读取终端GPRS数据信息',
        'type': '下行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '06': {
        'name': '终端校时',
        'type': '下行',
        'default': [],
        'element': ['0004'],
        'type_dict': {}
    },
    '07': {
        'name': '读取终端时钟',
        'type': '下行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '1C': {
        'name': '抄取管网实时数据',
        'type': '下行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
}

# 入库的命令列表
IS_SAVE_LIST = ['B3', 'B4']

# 配置的CLASS
__CLASS__ = 'XinTianKeJiSettingInfo'


class XinTianKeJiSettingInfo(object):
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
