# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/7/27

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'gate_position',
        'name': '闸位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'water_level',
        'name': '水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'total_flow',
        'name': '累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'time',
        'name': '时间',
        'length': None,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'str_date', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'action_status',
        'name': '动作状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'open_close_gate_action',
        'name': '开关闸动作',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'open_close_machine_action',
        'name': '开关机动作',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'remote_status',
        'name': '远程现地状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'alarm_type',
        'name': '报警类型',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'zero_point_water_level',
        'name': '零点水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'gate_height',
        'name': '闸门高度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'gate_width',
        'name': '闸门宽度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'status_code': {
        'code': 'status_code',
        'name': '状态码',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'value': {
        'code': 'value',
        'name': '参数值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '1': {
        'name': u'参数设置_闸位开度__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '2': {
        'name': u'参数设置_流量控制__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '3': {
        'name': u'参数设置_总量控制__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '4': {
        'name': u'闸位控制模式__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '5': {
        'name': u'远程操作_开闸__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '6': {
        'name': u'远程操作_关闸__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '7': {
        'name': u'远程操作_停止__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '8': {
        'name': u'远程操作_开关机__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '9': {
        'name': u'数据通讯_上传间隔__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '10': {
        'name': u'数据通讯_召测__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '11': {
        'name': u'数据通讯_补传__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '12': {
        'name': u'时间同步__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '13': {
        'name': u'基础信息_闸门__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '14': {
        'name': u'基础信息_流量计__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '15': {
        'name': u'数据同步_闸门基础信息__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '17': {
        'name': u'数据同步_闸门状态信息__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '99': {
        'name': u'通讯_回环测试__上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '176': {
        'name': u'闸门实时状态__上行',
        'type': '上行',
        'default': [],
        'element': ['0001', '0002', '0003', '0004', '0005'],
        'type_dict': {}
    },
    '178': {
        'name': u'闸位__上行',
        'type': '上行',
        'default': [],
        'element': ['0001', '0006'],
        'type_dict': {}
    },
    '179': {
        'name': u'开关闸通知__上行',
        'type': '上行',
        'default': [],
        'element': ['0007', '0001', '0002', '0003', '0004', '0005'],
        'type_dict': {}
    },
    '180': {
        'name': u'状态通知__上行',
        'type': '上行',
        'default': [],
        'element': ['0008', '0009', '0005'],
        'type_dict': {}
    },
    '181': {
        'name': u'报警通知__上行',
        'type': '上行',
        'default': [],
        'element': ['0010', '0001', '0002', '0003', '0005'],
        'type_dict': {}
    },
    '182': {
        'name': u'闸门__上行',
        'type': '上行',
        'default': [],
        'element': ['0011', '0012', '0013'],
        'type_dict': {}
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '1': {
        'name': u'参数设置_闸拉开度_上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '2': {
        'name': u'参数设置_流量控制__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '3': {
        'name': u'参数设置_总量控制__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '4': {
        'name': u'闸位控制模式__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '5': {
        'name': u'远程操作_开闸__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '6': {
        'name': u'远程操作_关闸__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '7': {
        'name': u'远程操作_停止__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '8': {
        'name': u'远程操作_开关机__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '9': {
        'name': u'数据通讯_上传间隔__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '10': {
        'name': u'数据通讯_召测__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '11': {
        'name': u'数据通讯_补传__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '12': {
        'name': u'时间同步__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '13': {
        'name': u'基础信息_闸门__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '14': {
        'name': u'基础信息_流量计__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '15': {
        'name': u'数据同步_闸门基础信息__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '17': {
        'name': u'数据同步_闸门状态信息__上行',
        'type': '上行',
        'default': [],
        'element': ['value'],
        'type_dict': {}
    },
    '99': {
        'name': u'通讯_回环测试__应答',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '176': {
        'name': u'闸位实时状态__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '178': {
        'name': u'闸位__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '179': {
        'name': u'开关闸__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '180': {
        'name': u'状态__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '181': {
        'name': u'报警__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    },
    '182': {
        'name': u'闸门__应答',
        'type': '应答',
        'default': [],
        'element': ['status_code'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['176', '178', '179', '180', '181', '182']

# 配置的CLASS
__CLASS__ = 'FDSettingInfo'


class FDSettingInfo(object):
    """
    获取FD配置信息
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
        获取元素列表
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
    setting_info = FDSettingInfo()
    print(setting_info.get_device_2_platform_protocol_dict('1'))
