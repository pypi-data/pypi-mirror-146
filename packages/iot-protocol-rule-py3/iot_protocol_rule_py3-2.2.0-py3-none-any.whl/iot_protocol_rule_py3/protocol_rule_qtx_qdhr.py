# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/01/07

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'ADDR': {
        'code': 'addr',
        'name': '地址',
        'length': 10,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'PW': {
        'code': 'pw',
        'name': '密码',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_pw', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'TP': {
        'code': 'tp',
        'name': '时间标签',
        'length': 10,
        'de_plug': [
            {'code': 'tp_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'make_tp', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'link_state',
        'name': '链路状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'terminal_clock',
        'name': '终端时钟',
        'length': 12,
        'de_plug': [
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'make_terminal_clock', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'version_no',
        'name': '版本号',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'current_user_no',
        'name': '当前用户号',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'current_use_water',
        'name': '当前用水量',
        'length': 8,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'total_water',
        'name': '累计水量',
        'length': 10,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'current_remnant_water',
        'name': '当前剩余水量',
        'length': 8,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'calculate_water_meter_base',
        'name': '计量水表底数',
        'length': 10,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'reserve_1',
        'name': '备用1',
        'length': 10,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'electric',
        'name': '电度',
        'length': 8,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'a_phase_voltage',
        'name': 'A相电压',
        'length': 4,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'b_phase_voltage',
        'name': 'B相电压',
        'length': 4,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'c_phase_voltage',
        'name': 'C相电压',
        'length': 4,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'a_phase_current',
        'name': 'A相电流',
        'length': 6,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'b_phase_current',
        'name': 'B相电流',
        'length': 6,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'c_phase_current',
        'name': 'C相电流',
        'length': 6,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'a_phase_state',
        'name': 'A相状态字',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'b_phase_state',
        'name': 'B相状态字',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'c_phase_state',
        'name': 'C相状态字',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'simulate_1',
        'name': '模拟量1',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'simulate_2',
        'name': '模拟量2',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'lock_state',
        'name': '锁机状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'calculate_mode',
        'name': '计量方式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'calculate_water_meter_communicate_flg',
        'name': '计量水表通讯正常标识',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'water_meter_2_base',
        'name': '水表2水表底数',
        'length': 10,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'water_meter_3_base',
        'name': '水表3水表底数',
        'length': 10,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'water_meter_4_base',
        'name': '水表4水表底数',
        'length': 10,
        'de_plug': [
            {'code': 'bcd_int_than_divided_by_10', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'reserve_2',
        'name': '备用2',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'alarm_state',
        'name': '报警状态',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'terminal_state',
        'name': '终端状态',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'work_state',
        'name': '工作状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_work_state', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'pump_mode',
        'name': '水泵方式',
        'length': 1,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_pump_mode', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'pump_no',
        'name': '水泵序号',
        'length': 1,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'handle_ret',
        'name': '执行结果',
        'length': 1,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '02': {
        'name': '链路检测',
        'type': '响应',
        'default': ['ADDR'],
        'element': ['0001'],
        'type_dict': {}
    },
    '11': {
        'name': '设置遥测终端时钟',
        'type': '响应',
        'default': ['ADDR'],
        'element': ['0002', 'PW', 'TP'],
        'type_dict': {}
    },
    '93': {
        'name': '遥控关闭水泵',
        'type': '上行',
        'default': ['ADDR'],
        'element': ['0034', '0033'],
        'type_dict': {}
    },
    'B0': {
        'name': '查询遥测终端实时值',
        'type': '上行',
        'default': ['ADDR'],
        'element': ['0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017',
                    '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0026', '0027', '0028', '0029', '0030'],
        'type_dict': {}
    },
    'C0': {
        'name': '自报实时数据',
        'type': '响应',
        'default': ['ADDR'],
        'element': ['0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017',
                    '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0026', '0027', '0028', '0029', '0030'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '02': {
        'name': '链路检测',
        'type': '上行',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '11': {
        'name': '设置遥测终端时钟',
        'type': '上行',
        'default': [],
        'element': ['0002', 'PW', 'TP'],
        'type_dict': {}
    },
    '93': {
        'name': '遥控关闭水泵',
        'type': '上行',
        'default': [],
        'element': ['0032', '0033', 'PW', 'TP'],
        'type_dict': {}
    },
    'B0': {
        'name': '查询遥测终端实时值',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'C0': {
        'name': '自报实时数据',
        'type': '响应',
        'default': [],
        'element': ['0031'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['C0']

# 配置的CLASS
__CLASS__ = 'QTXQDHRSettingInfo'


class QTXQDHRSettingInfo(object):
    """
    青铜峡-青岛恒润 协议配置信息
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
