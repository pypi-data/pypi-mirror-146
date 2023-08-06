# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/08/24

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'METER_TYPE': {
        'code': 'meter_type',
        'name': '水表类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'METER_ADDRESS': {
        'code': 'meter_address',
        'name': '水表地址',
        'length': 10,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'MANUFACTURER_CODE': {
        'code': 'manufacturer_code',
        'name': '厂商代码',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'CONTROL_CODE': {
        'code': 'control_code',
        'name': '控制码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0000': {
        'code': 'result_code',
        'name': '结果码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'timestamp',
        'name': '时间戳',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'imsi',
        'name': 'IMSI',
        'length': 30,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'ascii_to_str', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'imei',
        'name': 'IMEI',
        'length': 30,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'ascii_to_str', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'software_version',
        'name': '软件版本',
        'length': 6,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_software_version', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'pulse_equivalent',
        'name': '脉冲当量',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'temperature',
        'name': '温度',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divide_by_100', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'send_no',
        'name': '发送序号',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'report_data_mark',
        'name': '上报数据标志',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'voltage_threshold',
        'name': '电压阈值',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divide_by_100', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'open_close_valve_time',
        'name': '开关阀时间',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_open_close_valve_time', 'params': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'real_time_accumulated_flow',
        'name': '实时累计流量',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_accumulated_flow', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divide_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'daily_accumulated_flow',
        'name': '日结累计流量',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_accumulated_flow', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divide_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'daily_reverse_accumulated_flow',
        'name': '日结累计逆流量',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_accumulated_flow', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divide_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'daily_highest_flow_speed',
        'name': '日最高流速',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'daily_highest_flow_speed_timestamp',
        'name': '日最高流速时间戳',
        'length': 6,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 't_water_consumption_data_count',
        'name': '周期用水量数据个数',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 't_water_consumption_data_list',
        'name': '周期用水量数据列表',
        'length': None,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_t_water_consumption_data_list', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'meter_state',
        'name': '水表状态',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'rsrp',
        'name': '信号强度RSRP',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'minus_140', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'snr',
        'name': '信噪比SNR',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_snr', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'ecl',
        'name': '覆盖等级ECL',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'community_id',
        'name': '小区ID',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'csq',
        'name': '信号等级CSQ',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'cell_id',
        'name': 'CELL_ID',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'rssi',
        'name': 'RSSI',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'minus_140', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'frequency_point',
        'name': '频点',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'time_zone',
        'name': '时区',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_time_zone', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'tau_time',
        'name': 'TAU 时间',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'cover_level_0_send_count',
        'name': '覆盖等级0发送次数',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'cover_level_1_send_count',
        'name': '覆盖等级1发送次数',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'cover_level_2_send_count',
        'name': '覆盖等级2发送次数',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'un_send_count',
        'name': '未发送次数',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'high_to_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'already_run_days',
        'name': '已运行天数',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    'B1': {
        'name': '数据周期上报',
        'type': '上行',
        'default': [],
        'element': ['0000', '0001'],
        'type_dict': {}
    },
    'B2': {
        'name': '告警立即上报',
        'type': '应答',
        'default': [],
        'element': ['0000', '0001'],
        'type_dict': {}
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '31': {
        'name': '数据周期上报',
        'type': '上行',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'MANUFACTURER_CODE', 'CONTROL_CODE'],
        'element': ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015',
                    '0016', '0017', '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0026', '0027', '0028', '0029', '0030',
                    '0031', '0032', '0033', '0034'],
        'type_dict': {}
    },
    '32': {
        'name': '告警立即上报',
        'type': '上行',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'MANUFACTURER_CODE', 'CONTROL_CODE'],
        'element': ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0019'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['31', '32']

# 配置的CLASS
__CLASS__ = 'OneNETNingBoSettingInfo'


class OneNETNingBoSettingInfo(object):
    """
    移动OneNET平台_宁波水表协议配置信息
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
