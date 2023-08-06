# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/07/05

@author: gw
"""

# 元素列表
ELEMENT_DICT = {
    '001': {
        'code': 'equipment_manufacturer',
        'name': '设备厂家',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'hardware_version',
        'name': '硬件版本',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'cpu_number',
        'name': 'CPU编号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'equip_type',
        'name': '设备类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'equip_number',
        'name': '设备编号',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'baud_rate',
        'name': '波特率',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'internal_clock',
        'name': '内部时钟',
        'length': 8,
        'de_plug': [],
        'en_plug': [{'params': ['srg_data'], 'code': 'internal_clock_set', 'return': ['srg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'memory_data_number',
        'name': '存贮器中的数据条数',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'time_zero',
        'name': '计时起点（Unix时间值）',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'offline_collection_period',
        'name': '离线采集周期',
        'length': 8,
        'de_plug': [],
        'en_plug': [{'params': ['srg_data'], 'code': 'collection_period_set', 'return': ['srg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'self_reported_switch',
        'name': '自报开关',
        'length': 2,
        'de_plug': [],
        'en_plug': [{'params': ['srg_data'], 'code': 'reported_switch_set', 'return': ['srg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'warm_up_time',
        'name': '通讯预热时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'day_time_report',
        'name': '每天平安报时间',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'sleep_time',
        'name': '无操作自动休眠时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'sensor_warm_up_time',
        'name': '传感器预热时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'latest_boot_time',
        'name': '最近开机时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'communication_time_delay',
        'name': '通讯延时',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'ID_24',
        'name': '24字节唯一识别ID号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'channel_and_sensor_info',
        'name': '通道诊断信息及传感器参数结构',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'rain_gauge_resolution',
        'name': '雨量计分辨率',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'rain_gauge_self_reported_resolution',
        'name': '雨量计自报辨率',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'device_running_time',
        'name': '设备上电运行时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'next_startup_time',
        'name': '下次启动时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'none_automatic_sleep_time',
        'name': '无操作自动休眠时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'channel_temperature_resistance_type',
        'name': '通道温度电阻类型',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'channel_excitation_type',
        'name': '通道激励类型',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'current_voltage_channel_type',
        'name': '电流电压通道类型',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'heartbeat_interval',
        'name': '心跳间隔',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'registration_packet',
        'name': '注册包',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'heartbeat_packet',
        'name': '心跳包',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'offline_package',
        'name': '下线包',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'ip/port_main',
        'name': '主IP/域名:端口',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'ip/port_prepare',
        'name': '备IP/域名:端口',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'APN',
        'name': '接入点APN',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'centre_number',
        'name': '中心号码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'collects_parameters_1',
        'name': '通道1采集参数',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'collects_parameters_2',
        'name': '通道2采集参数',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'collects_parameters_3',
        'name': '通道3采集参数',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'collects_parameters_4',
        'name': '通道4采集参数',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'data_time',
        'name': '时间',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'data_time_t', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'read_memory_start_time',
        'name': '读存储器起始时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'read_memory_index_number',
        'name': '读存储器索引号',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'read_memory_end_time',
        'name': '读存储器结束时间',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'channel_1_data_1',
        'name': '通道1数据1',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'channel_1_data_2',
        'name': '通道1数据2',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'channel_2_data_1',
        'name': '通道2数据1',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '049': {
        'code': 'channel_2_data_2',
        'name': '通道2数据2',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '050': {
        'code': 'channel_3_data_1',
        'name': '通道3数据1',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '051': {
        'code': 'channel_3_data_2',
        'name': '通道3数据2',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '052': {
        'code': 'channel_4_data_1',
        'name': '通道4数据1',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '053': {
        'code': 'channel_4_data_2',
        'name': '通道4数据2',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'high_to_low_hex', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'hex_float', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '054': {
        'code': 'illegal_function',
        'name': '非法功能',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '非法功能',
        'srg_data': '非法功能'
    },
    '055': {
        'code': 'illegal_address',
        'name': '非法地址',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '非法地址',
        'srg_data': '非法地址'
    },
    '056': {
        'code': 'illegal_data',
        'name': '非法数据',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '非法数据',
        'srg_data': '非法数据'
    },
    '057': {
        'code': 'equipment_failure',
        'name': '设备故障',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '设备故障',
        'srg_data': '设备故障'
    },
    '058': {
        'code': 'identify_successful',
        'name': '确认成功',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '确认成功',
        'srg_data': '确认成功'
    },
    '059': {
        'code': 'device_busy',
        'name': '设备忙',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '设备忙',
        'srg_data': '设备忙'
    },
    '060': {
        'code': 'check_error',
        'name': '校验错误',
        'length': 0,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '校验错误',
        'srg_data': '校验错误'
    },
}

# 平台至设备协议配置
DEVICE_2_PLATFORM = {
    '01': {
        'name': '非法功能',
        'type': '上行',
        'default': [],
        'element': ['054'],
        'type_dict': {}
    },
    '02': {
        'name': '非法地址',
        'type': '上行',
        'default': [],
        'element': ['055'],
        'type_dict': {}
    },
    '03': {
        'name': '非法数据',
        'type': '上行',
        'default': [],
        'element': ['056'],
        'type_dict': {}
    },
    '04': {
        'name': '设备故障',
        'type': '上行',
        'default': [],
        'element': ['057'],
        'type_dict': {}
    },
    '05': {
        'name': '确认帧',
        'type': '上行',
        'default': [],
        'element': ['058'],
        'type_dict': {}
    },
    '06': {
        'name': '设备忙',
        'type': '上行',
        'default': [],
        'element': ['059'],
        'type_dict': {}
    },
    '08': {
        'name': '校验错误',
        'type': '上行',
        'default': [],
        'element': ['060'],
        'type_dict': {}
    },
    '09': {
        'name': '内存为空',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '0A': {
        'name': '读取参数返回',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '06': {
                'name': '读取参数返回',
                'element': [],
            }
        }
    },
    '0B': {
        'name': '读取数据返回',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '0D': {
        'name': '实时自报数据返回',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '0F': {
        'name': '离线采集数据返回',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': '离线自报数据返回',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '11': {
        'name': '定时自报数据返回',
        'type': '上行',
        'default': ['041', '008', '046', '047', '048', '049', '050', '051', '052', '053', ],
        'element': [],
        'type_dict': {
            '01': {
                'name': '模块时间',
                'element': ['041'],
            },
            '03': {
                'name': '电池电压',
                'element': ['008'],
            },
            'B0': {
                'name': '通道1数据1',
                'element': ['046'],
            },
            'B8': {
                'name': '通道1数据2',
                'element': ['047'],
            },
            'B1': {
                'name': '通道2数据1',
                'element': ['048'],
            },
            'B9': {
                'name': '通道2数据2',
                'element': ['049'],
            },
            'B2': {
                'name': '通道3数据1',
                'element': ['050'],
            },
            'BA': {
                'name': '通道3数据2',
                'element': ['051'],
            },
            'B3': {
                'name': '通道4数据1',
                'element': ['052'],
            },
            'BB': {
                'name': '通道4数据2',
                'element': ['053'],
            },
        }
    },
    '13': {
        'name': '诊断数据及传感器资料返回',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
}

# 设备至平台协议配置
PLATFORM_2_DEVICE = {
    '80': {
        'name': '读取参数',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '05': {
                'name': '设备编号',
                'element': [],
            },
            '06': {
                'name': '波特率',
                'element': [],
            },
            '07': {
                'name': '内部时钟',
                'element': [],
            }
        }
    },
    '81': {
        'name': '读取数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '82': {
        'name': '设置参数',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '0B': {
                'name': '定时采集周期',
                'element': ['011'],
            },
            '0C': {
                'name': '自报开关',
                'element': ['012'],
            },
            '07': {
                'name': '内部时钟',
                'element': ['007'],
            }}
    },
    '83': {
        'name': '数据采集',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '84': {
        'name': '清空存贮器',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '86': {
        'name': '使设备进入深度睡眠模式',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '87': {
        'name': '使设备保持在线模式',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '89': {
        'name': '读传感器信息',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'A2': {
        'name': '开启透明模式',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'A3': {
        'name': '关闭透明模式',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'A5': {
        'name': '重启',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'A8': {
        'name': '读取诊断数据及传感器资料',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },

}

# 入库的命令列表
IS_SAVE_LIST = ['11']

# 配置的CLASS
__CLASS__ = 'NGNSettingInfo'


class NGNSettingInfo(object):
    """
    获取NewSkyWell协议配置信息
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

    def get_device_2_platform_protocol_dict(self, command, data_type):
        """
        获取设备至平台协议字典
        :param protocol:
        :return:
        """
        if command in self.__device_2_platform.keys():
            if data_type in self.__device_2_platform[command]['type_dict'].keys():
                return [self.__element_dict[item] for item in
                        self.__device_2_platform[command]['type_dict'][data_type]['element']]
            else:
                return []
        else:
            return []

    def get_device_2_platform_protocol_dict_(self, command):
        """
        获取设备至平台协议字典
        :param protocol:
        :return:
        """
        if command in self.__device_2_platform.keys():
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['element']]
        else:
            return []

    def get_platform_2_device_protocol_dict(self, command, data_type):
        """
        获取平台至设备协议字典
        :param protocol:
        :return:
        """
        if command in self.__platform_2_device.keys():
            if data_type in self.__platform_2_device[command]['type_dict'].keys():
                return [self.__element_dict[item] for item in
                        self.__platform_2_device[command]['type_dict'][data_type]['element']]
            else:
                return []
        else:
            return []


if __name__ == '__main__':
    pass
