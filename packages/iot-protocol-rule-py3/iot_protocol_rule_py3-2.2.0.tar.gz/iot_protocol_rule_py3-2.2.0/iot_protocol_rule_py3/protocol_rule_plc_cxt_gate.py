# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/11/18

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
        'code': 'write_data_info',
        'name': '写数据内容',
        'length': None,
        'de_plug': [],
        'en_plug': [
            {'params': [], 'code': 'write_data_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
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
    '004': {
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
    '11F4': {
        'code': 'gate_control_word',
        'name': '闸门控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11F5': {
        'code': 'gate_set_value',
        'name': '闸门设定值',
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
    '11F6': {
        'code': 'gate_run_speed',
        'name': '闸门开启速度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11F7': {
        'code': 'gate_breakdown_reset',
        'name': '闸门故障复位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11FE': {
        'code': 'gate_back_water_level',
        'name': '闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11FF': {
        'code': 'gate_open_value',
        'name': '闸门开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1200': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1201': {
        'code': 'total_flow',
        'name': '累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1203': {
        'code': 'gate_state',
        'name': '闸门状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1204': {
        'code': 'gate_alarm',
        'name': '闸门报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1205': {
        'code': 'gate_weight',
        'name': '闸门荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1206': {
        'code': 'gate_voltage',
        'name': '闸门电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1207': {
        'code': 'gate_current',
        'name': '闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1208': {
        'code': 'electric_machinery_power',
        'name': '电机速度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1209': {
        'code': 'solar_panel_power',
        'name': '太阳能板功率',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '120A': {
        'code': 'load_power',
        'name': '负载功率',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '120B': {
        'code': 'equipment_compartment_temperature',
        'name': '设备舱温度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '120C': {
        'code': 'battery_surplus_electric_quantity',
        'name': '电池剩余电量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
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
        'element': ['11F4', '11F5', '11F6', '11F7', '11FE', '11FF', '1200', '1201', '1203', '1204', '1205', '1206', '1207', '1208', '1209',
                    '120A', '120B', '120C'],
        'type_dict': {}
    },
    '10': {
        'name': u'写寄存器响应',
        'type': '应答',
        'default': ['003', '004'],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    '03': {
        'name': u'读寄存器上行',
        'type': '上行',
        'default': ['003', '004'],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': u'写寄存器上行',
        'type': '上行',
        'default': ['002'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'PLCCXTGateInfo'


class PLCCXTGateInfo(object):
    """
    获取PLC城西滩闸门配置信息
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
