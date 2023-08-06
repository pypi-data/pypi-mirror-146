# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/09/02

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'signalStrength',
        'name': '信号强度(CSQ)',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'rsrpValue',
        'name': 'RERP',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'snrValue',
        'name': 'SNR',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'batteryVoltage',
        'name': '电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'forwardFlow',
        'name': '正向流量',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'reverseFlow',
        'name': '反向流量',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'instantFlow',
        'name': '瞬时流量',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'sampleTime',
        'name': '采样时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'meterStatus',
        'name': '表状态',
        'length': None,
        'de_plug': [{'code': 'replace_all_f', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'pressure',
        'name': '压力',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'temperature',
        'name': '温度',
        'length': None,
        'de_plug': [{'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'valveStatus',
        'name': '阀状态',
        'length': None,
        'de_plug': [{'code': 'to_valve_status', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'forwardFlow1',
        'name': '正向流量1',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'reverseFlow1',
        'name': '反向流量1',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'instantFlow1',
        'name': '瞬时流量1',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'sampleTime1',
        'name': '采样时间1',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'meterStatus1',
        'name': '表状态1',
        'length': None,
        'de_plug': [{'code': 'replace_all_f', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'pressure1',
        'name': '压力1',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'temperature1',
        'name': '温度1',
        'length': None,
        'de_plug': [{'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'valveStatus1',
        'name': '阀状态1',
        'length': None,
        'de_plug': [{'code': 'to_valve_status', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'forwardFlow2',
        'name': '正向流量2',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'reverseFlow2',
        'name': '反向流量2',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'instantFlow2',
        'name': '瞬时流量2',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'sampleTime2',
        'name': '采样时间2',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'meterStatus2',
        'name': '表状态2',
        'length': None,
        'de_plug': [{'code': 'replace_all_f', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'pressure2',
        'name': '压力2',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'temperature2',
        'name': '温度2',
        'length': None,
        'de_plug': [{'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'valveStatus2',
        'name': '阀状态2',
        'length': None,
        'de_plug': [{'code': 'to_valve_status', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'forwardFlow3',
        'name': '正向流量3',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'reverseFlow3',
        'name': '反向流量3',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'instantFlow3',
        'name': '瞬时流量3',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'sampleTime3',
        'name': '采样时间3',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'meterStatus3',
        'name': '表状态3',
        'length': None,
        'de_plug': [{'code': 'replace_all_f', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'pressure3',
        'name': '压力3',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'temperature3',
        'name': '温度3',
        'length': None,
        'de_plug': [{'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': 'valveStatus3',
        'name': '阀状态3',
        'length': None,
        'de_plug': [{'code': 'to_valve_status', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'longitude',
        'name': '经度',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'latitude',
        'name': '纬度',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'frozenTime',
        'name': '冻结时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'forwardflow',
        'name': '正向流量',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'reverseFlow',
        'name': '反向流量',
        'length': None,
        'de_plug': [{'code': 'to_float', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'valveSet',
        'name': '阀门设置',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'meterAdd': {
        'code': 'meterAdd',
        'name': '表号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'commandId': {
        'code': 'commandId',
        'name': '命令ID',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    'ReadBigMeterInfo_PLUS': {
        'name': '水表数据上传',
        'type': '上行',
        'default': [],
        'element': ['meterAdd', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013',
                    '0014', '0015', '0016', '0017', '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0026', '0027',
                    '0028', '0029', '0030', '0031', '0032', '0033', '0034', '0035', '0036'],
        'type_dict': {}
    },
    'ReadLocationInfo_PLUS': {
        'name': '经纬度信息上传',
        'type': '上行',
        'default': [],
        'element': ['meterAdd', '0037', '0038'],
        'type_dict': {}
    },
    'FrozenData_PLUS': {
        'name': '冻结数据上传',
        'type': '上行',
        'default': [],
        'element': ['meterAdd', '0039', '0040', '0041'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    'WriteInstructions_PLUS': {
        'name': '阀门控制',
        'type': '上行',
        'default': [],
        'element': ['0042'],
        'type_dict': {}
    },
    'QueryCommand': {
        'name': '命令查询',
        'type': '上行',
        'default': [],
        'element': ['commandId'],
        'type_dict': {}
    },
    'CancelCommand': {
        'name': '命令取消',
        'type': '上行',
        'default': [],
        'element': ['commandId'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['ReadBigMeterInfo_PLUS', 'FrozenData_PLUS']

# 配置的CLASS
__CLASS__ = 'CtwingMaiTuoSettingInfo'


class CtwingMaiTuoSettingInfo(object):
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
