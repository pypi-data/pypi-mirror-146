# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/12/12

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
            {'params': [], 'code': 'write_msg', 'return': ['msg_data']}
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
    '0000': {
        'code': 'gate_run',
        'name': '闸门启动',
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
    '0001': {
        'code': 'gate_stop',
        'name': '闸门停止',
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
    '0002': {
        'code': 'local_remote_choose',
        'name': '本地/远程选择',
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
    '0009': {
        'code': '1_enable',
        'name': '1#使能',
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
    '000A': {
        'code': '1_opening_set',
        'name': '1#开度设置',
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
    '000B': {
        'code': '1_alarm_reset',
        'name': '1#报警复位',
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
    '0013': {
        'code': '2_enable',
        'name': '2#使能',
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
    '0014': {
        'code': '2_opening_set',
        'name': '2#开度设置',
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
    '0015': {
        'code': '2_alarm_reset',
        'name': '2#报警复位',
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
    '001D': {
        'code': '3_enable',
        'name': '3#使能',
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
    '001E': {
        'code': '3_opening_set',
        'name': '3#开度设置',
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
    '001F': {
        'code': '3_alarm_reset',
        'name': '3#报警复位',
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
    '0022': {
        'code': 'gate_ahead_water_level',
        'name': '闸前水位',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'gate_behind_instantaneous_flow',
        'name': '闸后瞬时流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'gate_behind_water_level',
        'name': '闸后水位',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'gate_behind_total_flow',
        'name': '闸后累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002A': {
        'code': 'gate_behind_total_flow_carry_bit',
        'name': '闸后累计流量进位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': '1_opening',
        'name': '1#开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': '1_weight',
        'name': '1#荷重',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': '1_function',
        'name': '1#功能',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': '1_state',
        'name': '1#状态',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003B': {
        'code': '2_opening',
        'name': '2#开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003C': {
        'code': '2_weight',
        'name': '2#荷重',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003E': {
        'code': '2_function',
        'name': '2#功能',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003F': {
        'code': '2_state',
        'name': '2#状态',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': '3_opening',
        'name': '3#开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': '3_weight',
        'name': '3#荷重',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': '3_function',
        'name': '3#功能',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': '3_state',
        'name': '3#状态',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005A': {
        'code': 'control_mode',
        'name': '控制模式',
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
        'element': ['0000', '0001', '0002', '0009', '000A', '000B', '0013', '0014', '0015', '001D', '001E', '001F', '0022', '0024', '0026',
                    '0028', '002A', '0031', '0032', '0034', '0035', '003B', '003C', '003E', '003F', '0045', '0046', '0048', '0049', '005A'],
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
__CLASS__ = 'PLCGateInfo'


class PLCGateInfo(object):
    """
    获取PLC秦汉渠闸门配置信息
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
