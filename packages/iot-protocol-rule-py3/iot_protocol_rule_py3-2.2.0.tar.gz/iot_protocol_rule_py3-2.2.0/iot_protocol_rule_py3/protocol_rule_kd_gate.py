# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/23

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'electric',
        'name': u'电机电流',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'voltage',
        'name': u'电池电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'controlModel',
        'name': u'控制模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'currentCombats',
        'name': u'闸门当前开度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'waterLevelBefore',
        'name': u'上游水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'waterLevelAfter',
        'name': u'下游水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'instantaneousFlow',
        'name': u'瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'addupFlow',
        'name': u'累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'reportDate',
        'name': u'采样时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'deviceId': {
        'code': 'deviceId',
        'name': u'设备号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'type': {
        'code': 'type',
        'name': u'控制模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'setData': {
        'code': 'setData',
        'name': u'设定数据',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'getData': {
        'name': u'获取闸门最新数据',
        'type': '应答',
        'default': [],
        'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009'],
        'type_dict': {}
    }
}
# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'getData': {
        'name': u'获取闸门数据',
        'type': '上行',
        'default': [],
        'element': ['deviceId'],
        'type_dict': {}
    },
    'sluiceControl': {
        'name': u'闸门控制',
        'type': '上行',
        'default': [],
        'element': ['deviceId', 'type', 'setData'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['getData']

# 配置的CLASS
__CLASS__ = 'KDSettingInfo'


class KDSettingInfo(object):
    """
    获取科鼎配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__element_list = ['electric', 'voltage', 'controlModel', 'currentCombats', 'waterLevelBefore', 'waterLevelAfter', 'instantaneousFlow', 'addupFlow', 'reportDate']
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

    def get_element_list(self):
        """
        获取元素列表
        :return:
        """
        return self.__element_list

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
    setting = KDSettingInfo()
    print(setting.get_element_list())
