# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/08/24

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'imei',
        'name': 'imei',
        'length': 16,
        'de_plug': [{'return': ['msg_data'], 'code': 'imei_transform', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'default_key',
        'name': '默认密钥',
        'length': 32,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': '_',
        'name': '备用',
        'length': 20,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'new_key',
        'name': '新密钥',
        'length': 32,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'mother_key_number',
        'name': '母钥编号',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'daily_freezing_time',
        'name': '日冻结时间',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'daily_frozen_meter_base_flow',
        'name': '日冻结表底数流量',
        'length': 8,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_1000', 'params': ['msg_data']}
                    ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'current_positive_accumulated_flow',
        'name': '当前正向累计流量',
        'length': 8,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_1000', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'current_reverse_accumulated_flow',
        'name': '当前反向累计流量',
        'length': 8,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_1000', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'before_positive_accumulated_flow',
        'name': '前一日日结正向累计流量',
        'length': 8,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_1000', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'before_reverse_accumulated_flow',
        'name': '前一日日结反向累计流量',
        'length': 8,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_1000', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'before_instantaneous_flow',
        'name': '前一日瞬时量',
        'length': 192,
        'de_plug': [{'return': ['msg_data'], 'code': 'b_instantaneous_flow', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'meter_clock',
        'name': '水表时钟',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_10', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'version',
        'name': '版本号',
        'length': 10,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'valve_status',
        'name': '阀门状态',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'before_max_flow_rate',
        'name': '前一日最大流速',
        'length': 4,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_1000', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'before_max_flow_rate_time',
        'name': '前一日最大流速发生时间',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'report_base_time',
        'name': '上报基准时间',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'report_interval',
        'name': '上报时间间隔',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'mass_flow_alarm_threshold',
        'name': '大流量告警阀值',
        'length': 4,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'mass_flow_alarm_duration_time',
        'name': '大流量告警持续时间',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'small_flow_alarm_threshold',
        'name': '小流量告警阀值',
        'length': 4,
        'de_plug': [{'return': ['msg_data'], 'code': 'high_to_low', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_10', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'small_flow_alarm_duration_time',
        'name': '小流量告警持续时间',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'long_time_water_usage_threshold',
        'name': '长时间用水时间阀值',
        'length': 2,
        'de_plug': [],
        'en_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'low_battery_voltage_alarm_threshold',
        'name': '电池低电压告警阀值',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_10', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'high_pressure_alarm_threshold',
        'name': '高压告警阀值',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'low_pressure_alarm_threshold',
        'name': '低压告警阀值',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'main_clock',
        'name': '主站时钟',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [{'return': ['msg_data'], 'code': 'time_str_to_bcd', 'params': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'heavy_traffic_alarm',
        'name': '大流量告警',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'heavy_traffic_alarm_value',
        'name': '大流量告警发生值',
        'length': 4,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'heavy_traffic_alarm_time',
        'name': '大流量告警发生时间',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'low_traffic_alarm',
        'name': '小流量告警',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'low_traffic_alarm_value',
        'name': '小流量告警发生值',
        'length': 4,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']},
                    {'return': ['msg_data'], 'code': 'divide_by_10', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'low_traffic_alarm_time',
        'name': '小流量告警发生时间',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': 'reflux_alarm',
        'name': '反流告警',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'magnetic_interference_alarm',
        'name': '磁干扰告警',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'battery_low_voltage_alarm',
        'name': '电池低电压告警',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'data_tamper_alarm',
        'name': '数据被篡改',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'internal_error',
        'name': '内部错误',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'remote_module_separation_alarm',
        'name': '远传模块分离',
        'length': 2,
        'de_plug': [{'return': ['msg_data'], 'code': 'hex_to_int', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'frame_id',
        'name': '帧ID',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': 'switch_valve',
        'name': '开关阀',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0044': {
        'code': 'mass_flow_alarm_threshold',
        'name': '大流量报警阀值',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': 'mass_flow_duration',
        'name': '大流量持续时间',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': 'low_flow_alarm_threshold',
        'name': '小流量报警阀值',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': 'small_flow_duration',
        'name': '小流量持续时间',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': 'start_date',
        'name': '开始日期',
        'length': 6,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': 'end_date',
        'name': '结束日期',
        'length': 6,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0050': {
        'code': 'data_points',
        'name': '数据点个数',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': 'data_point_data',
        'name': '数据点数据',
        'length': 260,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': 'result',
        'name': '执行结果',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': 'report_time',
        'name': '上报时间',
        'length': 12,
        'de_plug': [{'return': ['msg_data'], 'code': 'time_bcd_to_str', 'params': ['msg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0054': {
        'code': '_',
        'name': '备用',
        'length': 18,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    'C0AF': {
        'name': '设备上线',
        'type': '上行',
        'default': [],
        'element': ['0001', '0002', '0003'],
        'type_dict': {}
    },
    'C0A0': {
        'name': '数据上报',
        'type': '上行',
        'default': [],
        'element': ['0006', '0007', '0008', '0009', '0010', '0011', '0012', '0003', '0013', '0014', '0015', '0016',
                    '0017', '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0026', '0027', '0028',
                    '0003', '0001'],
        'type_dict': {}
    },
    'C0A1': {
        'name': '告警立即上报',
        'type': '上行',
        'default': [],
        'element': ['0053', '0030', '0031', '0032', '0033', '0034', '0035', '0036', '0037', '0038', '0014', '0039',
                    '0040', '0041', '0003', '0001'],
        'type_dict': {}
     },
    # '40A2': {
    #     'name': '控制开关阀应答',
    #     'type': '应答',
    #     'default': [],
    #     'element': ['0042', '0052', '0003', '0001'],
    #     'type_dict': {}
    # },
    # 'C0A3': {
    #     'name': '限值设置应答',
    #     'type': '应答',
    #     'default': [],
    #     'element': ['0042', '0052', '0003', '0001'],
    #     'type_dict': {}
    # }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '40AF': {
        'name': '设备上线应答',
        'type': '应答',
        'default': [],
        'element': ['0052', '0004', '0005', '0001', '0003'],
        'type_dict': {}
    },
    '40A0': {
        'name': '数据上报应答',
        'type': '应答',
        'default': [],
        'element': ['0052', '0029', '0003', '0001'],
        'type_dict': {}
    },
    '40A1': {
        'name': '告警立即上报应答',
        'type': '应答',
        'default': [],
        'element': ['0052', '0003', '0001'],
        'type_dict': {}
    },
    # 'C0A2': {
    #     'name': '控制开关阀',
    #     'type': '下行',
    #     'default': [],
    #     'element': ['0042', '0043', '0054', '0001'],
    #     'type_dict': {}
    # },
    # '40A3': {
    #     'name': '限值设置',
    #     'type': '下行',
    #     'default': [],
    #     'element': ['0042', '0044', '0045', '0046', '0047', '0025', '0019', '0020', '0026','0027', '0028', '0003',
    #                 '0001'],
    #     'type_dict': {}
    # }
}

# 入库的命令列表
IS_SAVE_LIST = ['C0A0', 'C0A1']

# 配置的CLASS
__CLASS__ = 'OneNETXintianSettingInfo'


class OneNETXintianSettingInfo(object):
    """
    移动OneNET平台_北京慧怡水表协议配置信息
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
    tmp = OneNETXintianSettingInfo()
    for e in tmp.get_platform_2_device_protocol_dict('40A3'):
        print(e['name'])
