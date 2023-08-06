# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/21

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '000': {
        'code': 'device_code',
        'name': u'设备编码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '001': {
        'code': 'fun_code',
        'name': u'功能码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'remain_1',
        'name': u'保留1',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'remain_2',
        'name': u'保留2',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'record_count',
        'name': u'记录数量',
        'length': 2,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'update_command', 'params': ['srg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'record_format',
        'name': u'记录格式',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'update_command', 'params': ['srg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'power_supply_voltage',
        'name': u'电源电压',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'scene_state',
        'name': u'现场状态',
        'length': 2,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'protocol_version',
        'name': u'协议版本',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'param_version',
        'name': u'参数版本',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'signal_quality',
        'name': u'信号质量',
        'length': 2,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'remain_3',
        'name': u'保留3',
        'length': 6,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0000': {
        'code': 'date_time',
        'name': u'时间',
        'length': 8,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'meter_1_total_flow',
        'name': u'表1净累计',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'meter_1_positive_total_flow',
        'name': u'表1正累计',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'meter_1_negative_total_flow',
        'name': u'表1负累计',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'meter_1_instantaneous_flow',
        'name': u'表1瞬时流量',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'meter_2_total_flow',
        'name': u'表2净累计',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'meter_2_positive_total_flow',
        'name': u'表2正累计',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'meter_2_negative_total_flow',
        'name': u'表2负累计',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'meter_2_instantaneous_flow',
        'name': u'表2瞬时流量',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'pressure',
        'name': u'压力',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'temperature',
        'name': u'温度',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'water_level',
        'name': u'水位',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'switch',
        'name': u'开关量',
        'length': 8,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'frequency',
        'name': u'频率',
        'length': 8,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'instantaneous_mass_flow',
        'name': u'瞬时质量流量',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'density',
        'name': u'密度',
        'length': 8,
        'de_plug': [
            {'code': 'hex_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    '31': {
        'name': u'上报历史记录',
        'type': '上行',
        'default': ['000', '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011'],
        'element': ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011',
                    '0012', '0013', '0014',
                    '0015'],
        'type_dict': {}
    },
    '34': {
        'name': u'结束通讯',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    '31': {
        'name': u'上报历史记录',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '34': {
        'name': u'结束通讯',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['31']

# 配置的CLASS
__CLASS__ = 'FlowDLTYSettingInfo'


class FlowDLTYSettingInfo(object):
    """
    获取 大连天洋流量计 配置信息
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
        获取平台至设备协议字典
        :param command:
        :return:
        """
        if command in self.__device_2_platform.keys():
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['default']]
        else:
            return []

    def get_struct_element(self, record_format):
        """
        获取结构体要素
        :param record_format:
        :return:
        """
        element_list = [self.__element_dict['0000']]
        for index, item in enumerate(record_format):
            if item == '1':
                element_list.append(self.__element_dict[str(index + 1).zfill(4)])
            else:
                pass

        return element_list


if __name__ == '__main__':
    setting = FlowDLTYSettingInfo()
    print(setting.get_device_2_platform_protocol_dict('31'))

    print(setting.get_struct_element('0101000001010000'))
