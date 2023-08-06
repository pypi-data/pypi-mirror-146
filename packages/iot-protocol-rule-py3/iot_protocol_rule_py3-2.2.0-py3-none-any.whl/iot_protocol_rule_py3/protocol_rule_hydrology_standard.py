# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/05/29

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'order_issue_flow_number',
        'name': u'指令下发流水号',
        'length': 4,
        'de_plug': [
            {'code': 'update_command',
             'params': ['srg_data'],
             'return': [],
             }
        ],
        'en_plug': [
            {'code': 'get_order_issue_flow_number',
             'params': ['msg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': '',
    },
    '0002': {
        'code': 'reporting_time',
        'name': u'发报时间',
        'length': 12,
        'de_plug': [
            {'code': 'hex_time',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'update_command',
             'params': ['srg_data'],
             'return': [],
             }
        ],
        'en_plug': [
            {'code': 'get_report_time',
             'params': ['msg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': '',
    },
    '0003': {
        'code': 'telemetry_station_address',
        'name': u'遥测站地址',
        'length': 14,
        'de_plug': [
            {'code': 'del_4_bit',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '0004': {
        'code': 'telemetry_station_type_code',
        'name': u'遥测站分类码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '0005': {
        'code': 'observe_time',
        'name': u'观测时间',
        'length': 14,
        'de_plug': [
            {'code': 'del_4_bit',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'hex_time',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '02': {
        'code': 'instantaneous_air_temperature',
        'name': u'瞬时气温',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '04': {
        'code': 'time_step_length_code',
        'name': u'时间步长码',
        'length': None,
        'de_plug': [
            {'code': 'update_command',
             'params': ['srg_data'],
             'return': [],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '1F': {
        'code': 'day_precipitation',
        'name': u'日降水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '20': {
        'code': 'current_precipitation',
        'name': u'当前降水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '22': {
        'code': 'precipitation_minutes_5',
        'name': u'5分钟时段降水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '26': {
        'code': 'cumulative_value_precipitation',
        'name': u'降水量累计值',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '27': {
        'code': 'instantaneous_flow',
        'name': u'瞬时流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '30': {
        'code': 'total_outbound_flow',
        'name': u'总出库流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '37': {
        'code': 'instantaneous_flow_rate',
        'name': u'当前瞬时流速',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '38': {
        'code': 'power_supply_voltage',
        'name': u'电源电压',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '39': {
        'code': 'instantaneous_river_water_level_tide_level',
        'name': u'瞬时河道水位、潮位',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '45': {
        'code': 'telemetry_station_status_and_alarm_info',
        'name': u'遥测站状态及报警信息',
        'length': None,
        'de_plug': [
            {'code': 'hex_bin',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '46': {
        'code': 'ph',
        'name': u'pH值',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '49': {
        'code': 'turbidity',
        'name': u'浊度',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    '80': {
        'code': 'total_residual_chlorine',
        'name': u'总余氯',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'F0': {
        'code': 'observe_time',
        'name': u'观测时间',
        'length': None,
        'de_plug': [
            {'code': 'hex_time',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'F4': {
        'code': 'rainfall_every_5_minutes_within_1_hour',
        'name': u'1小时内每5分钟时段雨量',
        'length': None,
        'de_plug': [
            {'code': 'hex_float_2',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'F5': {
        'code': '1_hour_5_minute_relative_water_level_1',
        'name': u'1h内5min时段相对水位1',
        'length': None,
        'de_plug': [
            {'code': 'hex_float_4',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FF23': {
        'code': '12_groups_instantaneous_flow',
        'name': u'12组瞬时流量',
        'length': None,
        'de_plug': [
            {'code': 'hex_float_10',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FF2B': {
        'code': '12_groups_total_flow',
        'name': u'12组累计流量',
        'length': None,
        'de_plug': [
            {'code': 'hex_float_12',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FF9F': {
        'code': 'total_flow',
        'name': u'累计流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FF11': {
        'code': 'cumulative_bit',
        'name': u'累计位',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FFA0': {
        'code': 'instantaneous_flow_1',
        'name': u'瞬时流量1',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FFA1': {
        'code': 'instantaneous_flow_2',
        'name': u'瞬时流量2',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FFA2': {
        'code': 'total_flow_1',
        'name': u'累计流量1',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FFA3': {
        'code': 'total_flow_2',
        'name': u'累计流量2',
        'length': None,
        'de_plug': [
            {'code': 'int_float',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FFA4': {
        'code': 'alarm_1',
        'name': u'报警1',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    },
    'FFA5': {
        'code': 'alarm_2',
        'name': u'报警2',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': '',
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '2F': {
        'name': u'链路维持报上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '30': {
        'name': u'遥测站测试报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '31': {
        'name': u'均匀时段水文信息报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['04', '39'],
        'type_dict': {}
    },
    '32': {
        'name': u'遥测站定时报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['02', '20', '22', '27', '30', '37', '38', '39', '45', '46', '49', '80', 'FF11', 'FFA0', 'FFA1', 'FFA2', 'FFA3', 'FFA4', 'FFA5'],
        'type_dict': {}
    },
    '33': {
        'name': u'遥测站加时报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['39', '45', '38'],
        'type_dict': {}
    },
    '34': {
        'name': u'遥测站小时报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['1F', '20', '26', '27', '38', '45', '39', 'F4', 'F5', 'FF23', 'FF2B', 'FF9F'],
        'type_dict': {}
    },
    '35': {
        'name': u'遥测站人工置数报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '36': {
        'name': u'遥测站图片报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '37': {
        'name': u'中心站查询遥测站实时数据应答',
        'type': '应答',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '39': {
        'name': u'中心站查询遥测站人工置数应答',
        'type': '应答',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '44': {
        'name': u'中心站查询水泵电机实时工作数据应答',
        'type': '应答',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '45': {
        'name': u'中心站查询遥测站软件版本应答',
        'type': '应答',
        'default': ['0001', '0002', '0003'],
        'element': [],
        'type_dict': {}
    },
    '46': {
        'name': u'中心站查询遥测站状态和报警信息应答',
        'type': '应答',
        'default': ['0001', '0002', '0003'],
        'element': [],
        'type_dict': {}
    },
    '4A': {
        'name': u'中心站设置遥测站时钟应答',
        'type': '应答',
        'default': ['0001', '0002', '0003'],
        'element': [],
        'type_dict': {}
    },
    '50': {
        'name': u'中心站查询遥测站事件记录应答',
        'type': '应答',
        'default': ['0001', '0002', '0003'],
        'element': [],
        'type_dict': {}
    },
    '51': {
        'name': u'中心站查询遥测站时钟应答',
        'type': '应答',
        'default': ['0001', '0002', '0003'],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '30': {
        'name': u'遥测站测试报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '31': {
        'name': u'均匀时段水文信息报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '32': {
        'name': u'遥测站定时报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '33': {
        'name': u'遥测站加时报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '34': {
        'name': u'遥测站小时报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '35': {
        'name': u'遥测站人工置数报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '36': {
        'name': u'遥测站图片报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '37': {
        'name': u'中心站查询遥测站实时数据上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '39': {
        'name': u'中心站查询遥测站人工置数上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '44': {
        'name': u'中心站查询水泵电机实时工作数据上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '45': {
        'name': u'中心站查询遥测站软件版本上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '46': {
        'name': u'中心站查询遥测站状态和报警信息上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '4A': {
        'name': u'中心站设置遥测站时钟上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '50': {
        'name': u'中心站查询遥测站事件记录上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '51': {
        'name': u'中心站查询遥测站时钟上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['31', '32', '33', '34']

# 配置的CLASS
__CLASS__ = 'HydrologyStandardSettingInfo'


class HydrologyStandardSettingInfo(object):
    """
    获取水文监测配置信息
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
    pass
