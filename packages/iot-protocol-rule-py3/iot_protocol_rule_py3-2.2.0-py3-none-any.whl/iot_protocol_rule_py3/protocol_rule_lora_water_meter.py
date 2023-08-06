# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/06/11

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    'alarm_type': {
        'code': 'alarm_type',
        'name': u'报警类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'device_type': {
        'code': 'device_type',
        'name': u'设备类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'error_sign': {
        'code': 'error_sign',
        'name': u'错误标识',
        'length': 2,
        'de_plug': [
            {'code': 'check_device_response',
             'params': [],
             'return': [],
             }
        ],
        'en_plug': [
            {'code': 'check_platform_response',
             'params': [],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'current_type': {
        'code': 'current_type',
        'name': u'当前类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''

    },
    'unread_num': {
        'code': 'unread_num',
        'name': u'未读数量',
        'length': 2,
        'de_plug': [
            {'code': 'hex_int',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'read_num': {
        'code': 'read_num',
        'name': u'已读位置',
        'length': 2,
        'de_plug': [
            {'code': 'hex_int',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'call_type': {
        'code': 'call_type',
        'name': u'召测类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'position': {
        'code': 'position',
        'name': u'指定位置',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex',
             'params': ['msg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '01': {
        'code': 'software_version_number',
        'name': u'软件版本号',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '02': {
        'code': 'hardware_version_number',
        'name': u'硬件版本号',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '03': {
        'code': 'valve_1_status',
        'name': u'终端设备阀一状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '04': {
        'code': 'valve_2_status',
        'name': u'终端设备阀二状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '05': {
        'code': 'wife_signal_strength',
        'name': u'终端设备无线信号强度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '06': {
        'code': 'device_current_time',
        'name': u'终端设备当前时间',
        'length': None,
        'de_plug': [
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'hex_time',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'syn_device_time',
             'params': ['srg_data'],
             'return': [],
             }
        ],
        'en_plug': [
            {'code': 'current_time_hex',
             'params': [],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': '',
    },
    '07': {
        'code': 'device_collect_time',
        'name': u'终端设备采集时间',
        'length': None,
        'de_plug': [
            {'code': 'replace_A',
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
        'srg_data': ''
    },
    '08': {
        'code': 'battery_voltage',
        'name': u'终端设备电池电压',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '09': {
        'code': 'reset_number',
        'name': u'终端设备复位次数',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0A': {
        'code': 'pressure',
        'name': u'终端设备压力',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0B': {
        'code': 'soil_temperature',
        'name': u'终端设备土壤温度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0C': {
        'code': 'soil_humidity',
        'name': u'终端设备土壤湿度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0D': {
        'code': 'air_temperature',
        'name': u'终端设备空气温度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0E': {
        'code': 'air_humidity',
        'name': u'终端设备空气湿度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0F': {
        'code': 'light_intensity',
        'name': u'终端设备光照强度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10': {
        'code': 'signal_intensity',
        'name': u'网关GPRS信号强度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11': {
        'code': 'work_voltage_lower_limit_alarm',
        'name': u'设备工作电压低于下限报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '12': {
        'code': 'work_voltage_lower_limit',
        'name': u'设备工作电压下限',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '13': {
        'code': 'pressure_upper_limit_alarm',
        'name': u'设备压力高于上限报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '14': {
        'code': 'pressure_upper_limit',
        'name': u'设备压力上限',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '15': {
        'code': 'valve_1_connect_status_alarm',
        'name': u'阀门1连接状态报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '16': {
        'code': 'valve_1_switch_status_alarm',
        'name': u'阀门1开关状态报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '17': {
        'code': 'valve_2_connect_status_alarm',
        'name': u'阀门2连接状态报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '18': {
        'code': 'valve_2_switch_status_alarm',
        'name': u'阀门2开关状态报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '19': {
        'code': 'collect_cycle',
        'name': u'采集周期',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1A': {
        'code': 'storage_cycle',
        'name': u'存储周期',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1B': {
        'code': 'report_cycle',
        'name': u'上报周期',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1C': {
        'code': 'lora_software_version_number',
        'name': u'LORA软件版本号',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1D': {
        'code': 'lora_config_mode',
        'name': u'LORA配置模式',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1E': {
        'code': 'valve_1_switch_error_alarm',
        'name': u'阀门1开关异常报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '1F': {
        'code': 'valve_2_switch_error_alarm',
        'name': u'阀门2开关异常报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '20': {
        'code': 'gateway_lora_info',
        'name': u'网关LORA信息',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '21': {
        'code': 'lora_wife_channel',
        'name': u'终端LORA无线通道',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '22': {
        'code': 'instantaneous_flow',
        'name': u'瞬时流量',
        'length': None,
        'de_plug': [
            {'code': 'hex_int',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '23': {
        'code': 'total_flow',
        'name': u'累计流量',
        'length': None,
        'de_plug': [
            {'code': 'hex_int',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'divided_by_10',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '24': {
        'code': 'lora_claa_mode',
        'name': u'终端LORA_CLAA_MODE',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '25': {
        'code': 'greenhouse_run_time',
        'name': u'大棚设备运行时间',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '26': {
        'code': 'greenhouse_run_overtime_alarm',
        'name': u'大棚设备运行超时报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '27': {
        'code': 'greenhouse_limit_switch_alarm',
        'name': u'大棚设备限位开关报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '28': {
        'code': 'gps_longitude',
        'name': u'网关GPS经度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '29': {
        'code': 'gps_latitude',
        'name': u'网关GPS纬度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2A': {
        'code': 'terminal_receive_snr',
        'name': u'终端接收信噪比',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2B': {
        'code': 'gateway_receive_snr',
        'name': u'网关接收信噪比',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2C': {
        'code': 'send_voltage',
        'name': u'终端设备发射电压',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2D': {
        'code': 'gateway_activate_gps',
        'name': u'网关激活GPS',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2E': {
        'code': 'lora_data_rate',
        'name': u'终端LORADATARATE',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2F': {
        'code': 'lora_power',
        'name': u'终端LORAPOWER',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30': {
        'code': 'sim_ccid',
        'name': u'SIM卡CCID',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31': {
        'code': 'control_voltage_lower_limit_alarm',
        'name': u'设备控制电压低于下限报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '32': {
        'code': 'control_voltage_lower_limit',
        'name': u'设备控制电压下限',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '33': {
        'code': 'valve_forbid_status_alarm',
        'name': u'阀门禁止状态报警位',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '34': {
        'code': 'short_circuit_alarm',
        'name': u'短路报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '35': {
        'code': 'forbid_control_valve_flag',
        'name': u'禁止控阀标志位',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '36': {
        'code': 'water_status',
        'name': u'水流状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '37': {
        'code': 'inclinometer_x_angle',
        'name': u'测斜仪X轴角度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '38': {
        'code': 'inclinometer_y_angle',
        'name': u'测斜仪Y轴角度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '39': {
        'code': 'inclinometer_z_angle',
        'name': u'测斜仪Z轴角度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3A': {
        'code': 'inclinometer_x_frequency',
        'name': u'测斜仪X轴震动频率',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3B': {
        'code': 'inclinometer_y_frequency',
        'name': u'测斜仪Y轴震动频率',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3C': {
        'code': 'inclinometer_z_frequency',
        'name': u'测斜仪Z轴震动频率',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3D': {
        'code': 'inclinometer_x_amplitude',
        'name': u'测斜仪X轴震动幅度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3E': {
        'code': 'inclinometer_y_amplitude',
        'name': u'测斜仪Y轴震动幅度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3F': {
        'code': 'inclinometer_z_amplitude',
        'name': u'测斜仪Z轴震动幅度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '40': {
        'code': 'current_quantity_of_heat',
        'name': u'当前热量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '41': {
        'code': 'thermal_power',
        'name': u'热功率',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '42': {
        'code': 'supply_water_temperature',
        'name': u'供水温度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '43': {
        'code': 'back_water_temperature',
        'name': u'回水温度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '44': {
        'code': 'total_work_time',
        'name': u'累计工作时间',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '45': {
        'code': 'settlement_date_quantity_of_heat',
        'name': u'结算日热量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '46': {
        'code': 'inclinometer_sensor_temperature',
        'name': u'测斜仪传感器温度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '47': {
        'code': 'battery_voltage_status',
        'name': u'电池电压状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '48': {
        'code': 'sensor_serial_number',
        'name': u'传感器序列号',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '49': {
        'code': 'sensor_hardware_version',
        'name': u'传感器固件版本',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4A': {
        'code': 'moisture_temperature',
        'name': u'墒情温度',
        'length': None,
        'de_plug': [
            {'code': 'hex_moisture_temperature',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4B': {
        'code': 'moisture_water_rate',
        'name': u'墒情含水率',
        'length': None,
        'de_plug': [
            {'code': 'hex_moisture_water_rate',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4C': {
        'code': 'moisture_water_calculate_value',
        'name': u'墒情水分计算值',
        'length': None,
        'de_plug': [
            {'code': 'hex_moisture_water_calculate_value',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4D': {
        'code': 'connect_mode',
        'name': u'连接方式',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4E': {
        'code': 'air_pressure',
        'name': u'气压',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4F': {
        'code': 'wind_speed',
        'name': u'风速',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '50': {
        'code': 'wind_direction',
        'name': u'风向（偏离北度数）',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '51': {
        'code': 'total_rain',
        'name': u'累计雨量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '52': {
        'code': 'sensor_status',
        'name': u'传感器状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '53': {
        'code': 'magnetic_attack',
        'name': u'磁攻击',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '54': {
        'code': 'app_address_mark',
        'name': u'App地址标记',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '55': {
        'code': 'sim_card_number',
        'name': u'Sim卡号',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '56': {
        'code': 'valve_1_instantaneous_flow',
        'name': u'阀门1瞬时流量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '57': {
        'code': 'valve_2_instantaneous_flow',
        'name': u'阀门2瞬时流量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '58': {
        'code': 'valve_1_total_flow',
        'name': u'阀门1累计流量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '59': {
        'code': 'valve_2_total_flow',
        'name': u'阀门2累计流量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5A': {
        'code': 'valve_1_pressure',
        'name': u'阀门1压力',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5B': {
        'code': 'valve_2_pressure',
        'name': u'阀门2压力',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5C': {
        'code': 'valve_1_pressure_upper_limit_alarm',
        'name': u'阀门1压力高于上限报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5D': {
        'code': 'valve_2_pressure_upper_limit_alarm',
        'name': u'阀门2压力高于上限报警',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5E': {
        'code': 'adxl_345',
        'name': u'ADXL345状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5F': {
        'code': 'imei',
        'name': u'IMEI',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '60': {
        'code': 'valve_1_degree',
        'name': u'阀门1开度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '61': {
        'code': 'valve_2_degree',
        'name': u'阀门2开度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '62': {
        'code': 'inclinometer_x_displacement',
        'name': u'X轴位移',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '63': {
        'code': 'inclinometer_y_displacement',
        'name': u'Y轴位移',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '64': {
        'code': 'inclinometer_z_displacement',
        'name': u'Z轴位移',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '65': {
        'code': 'sensor_length',
        'name': u'传感器长度',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '70': {
        'code': 'structure_data',
        'name': u'结构体数据',
        'length': None,
        'de_plug': [],
        'en_plug': [
            {'name': 'structure_hex',
             'params': ['srg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '81': {
        'code': 'terminal_address',
        'name': u'终端地址',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '82': {
        'code': 'valve_1_control',
        'name': u'阀门1控制',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '83': {
        'code': 'valve_2_control',
        'name': u'阀门2控制',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '84': {
        'code': 'restart_device',
        'name': u'重启设备',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '85': {
        'code': 'set_device_type',
        'name': u'设置设备类型',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '86': {
        'code': 'set_gateway_ip_address',
        'name': u'设置网关GPRSL连接目的IP地址',
        'length': None,
        'de_plug': [
            {'code': 'hex_ip_port',
             'params': ['msg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [
            {'code': 'ip_port_hex',
             'params': ['srg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '87': {
        'code': 'set_gateway_connect_priority',
        'name': u'设置网关网络连接优先',
        'length': None,
        'de_plug': [
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '88': {
        'code': 'set_gateway_ethernet_address',
        'name': u'设置网关以太网口连接目的IP地址',
        'length': None,
        'de_plug': [
            {'code': 'hex_ip_port',
             'params': ['msg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [
            {'code': 'ip_port_hex',
             'params': ['srg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '89': {
        'code': 'roller_blind_control',
        'name': u'卷帘控制',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8A': {
        'code': 'wind_control_1',
        'name': u'放风控制1',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8B': {
        'code': 'wind_control_2',
        'name': u'放风控制2',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8C': {
        'code': 'terminal_irrigate_plan',
        'name': u'终端灌溉计划',
        'length': None,
        'de_plug': [
            {'code': 'hex_plan',
             'params': ['msg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8D': {
        'code': 'set_gateway_ethernet_local_ip_address',
        'name': u'设置网关以太网口本地IP地址',
        'length': None,
        'de_plug': [
            {'code': 'hex_ip',
             'params': ['msg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [
            {'name': 'ip_hex',
             'params': ['srg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '8E': {
        'code': 'set_gateway_ethernet_subnet_mask',
        'name': u'设置网关以太网口子网掩码',
        'length': None,
        'de_plug': [
            {'code': 'hex_ip',
             'params': ['msg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [
            {'code': 'ip_hex',
             'params': ['srg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '8F': {
        'code': 'set_gateway_ethernet_default_gateway_address',
        'name': u'设置网关以太网口默认网关地址',
        'length': None,
        'de_plug': [
            {'code': 'hex_ip',
             'params': ['msg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [
            {'code': 'ip_hex',
             'params': ['srg_data'],
             'return': ['msg_data'],
             }
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '90': {
        'code': 'water_meter_control_status',
        'name': u'水表阀门控制/状态',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '91': {
        'code': 'water_meter_id_set_get',
        'name': u'水表ID设置/获取',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '92': {
        'code': 'sport_threshold',
        'name': u'运动阀值',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '93': {
        'code': 'sport_time',
        'name': u'运动时间',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '94': {
        'code': 'static_threshold',
        'name': u'静止阀值',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '95': {
        'code': 'static_time',
        'name': u'静止时间',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '96': {
        'code': 'absolute_relative_zero_point_set',
        'name': u'绝对/相对零点设置',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '97': {
        'code': 'restore_factory_setting',
        'name': u'恢复出厂设置',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '98': {
        'code': 'piping_info',
        'name': u'管道信息',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '99': {
        'code': 'pulse_coefficient',
        'name': u'脉冲系数',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9A': {
        'code': 'valve_type',
        'name': u'阀门类型',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9B': {
        'code': 'offset',
        'name': u'偏移量',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9C': {
        'code': 'network_mode',
        'name': u'网络模式',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9D': {
        'code': 'pressure_lower_limit_alarm',
        'name': u'压力下限',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'number_transform',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FD': {
        'code': 'factory_test_result',
        'name': u'工厂测试结果',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FE': {
        'code': 'log_switch',
        'name': u'LOG开关',
        'length': None,
        'de_plug': [
            {'code': 'replace_FF',
             'params': ['srg_data'],
             'return': ['srg_data'],
             },
            {'code': 'replace_A',
             'params': ['srg_data'],
             'return': ['srg_data'],
             }
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '0001': {
        'name': u'网关注册上行',
        'type': '上行',
        'default': [],
        'element': ['01', '02', '09', '19', '1A', '1B', '30', '85'],
        'type_dict': {}
    },
    '0002': {
        'name': u'网关状态心跳上行',
        'type': '上行',
        'default': [],
        'element': ['06', '10', '08'],
        'type_dict': {}
    },
    '0003': {
        'name': u'实时数据上报上行',
        'type': '上行',
        'default': [],
        'element': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F', '20',
                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30',
                    '31', '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F', '40',
                    '41', '42', '43', '44', '45', '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F', '50',
                    '51', '52', '53', '54', '55', '56', '57', '58', '59', '5A', '5B', '5C', '5D', '5E', '5F', '60',
                    '61', '62', '63', '64', '65', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                    '8C', '8D', '8E', '8F', '90', '91', 'FD', 'FE'],
        'type_dict': {}
    },
    '0004': {
        'name': u'警情上报上行',
        'type': '上行',
        'default': ['alarm_type'],
        'element': ['11', '13', '15', '16', '17', '18', '1E', '1F', '26', '27', '31', '33', '34', '5C', '5D'],
        'type_dict': {}
    },
    '0005': {
        'name': u'终端注册上行',
        'type': '上行',
        'default': ['device_type'],
        'element': ['01', '02', '06', '08', '09', '10', '19', '1A', '1B', '2F', '1C', '1D'],
        'type_dict': {}
    },
    '0006': {
        'name': u'终端通用下行控制应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0007': {
        'name': u'终端通用信息召测应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0009': {
        'name': u'网关连接心跳上行',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '000A': {
        'name': u'网关应答',
        'default': ['error_sign'],
        'type': '应答',
        'element': [],
        'type_dict': {}
    },
    '000B': {
        'name': u'网关通用下行控制应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '000C': {
        'name': u'网关通用信息召测应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '000F': {
        'name': u'灌溉计划设置应答',
        'type': '应答',
        'default': ['error_sign', 'current_type'],
        'element': [],
        'type_dict': {}
    },
    '0010': {
        'name': u'灌溉计划召测应答',
        'type': '应答',
        'default': ['error_sign', 'unread_num', 'read_num'],
        'element': [],
        'type_dict': {}
    },
    '0011': {
        'name': u'网关数据上报上行',
        'type': '应答',
        'default': [],
        'element': ['06', '0D', '0E', '0F', '22', '23', '28', '29', '4A', '4B', '4C', '4E', '4F', '50', '51'],
        'type_dict': {}
    },
    '0012': {
        'name': u'网关合法终端设置应答',
        'type': '应答',
        'default': ['error_sign', 'current_type'],
        'element': [],
        'type_dict': {}
    },
    '0013': {
        'name': u'网关合法终端召测应答',
        'type': '应答',
        'default': ['error_sign', 'unread_num', 'read_num'],
        'element': [],
        'type_dict': {}
    },
    '0018': {
        'name': u'实时数据上报上行',
        'type': '上行',
        'default': [],
        'element': ['4A', '4B', '4C'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '0001': {
        'name': u'网关注册应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0002': {
        'name': u'网关状态心跳应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0003': {
        'name': u'实时数据上报应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0004': {
        'name': u'警情上报应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0005': {
        'name': u'终端注册应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0006': {
        'name': u'终端通用下行控制上行（需要响应）',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '0007': {
        'name': u'终端通用信息召测上行',
        'type': '上行',
        'default': ['call_type'],
        'element': [],
        'type_dict': {}
    },
    '0008': {
        'name': u'终端通用下行控制上行（不需响应）',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '0009': {
        'name': u'网关连接心跳应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '000B': {
        'name': u'网关通用下行控制上行（需要响应）',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '000C': {
        'name': u'网关通用信息召测上行',
        'type': '上行',
        'default': ['call_type'],
        'element': [],
        'type_dict': {}
    },
    '000D': {
        'name': u'网关通用下行控制上行（不需响应）',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '000F': {
        'name': u'灌溉计划设置上行',
        'type': '上行',
        'default': ['current_type'],
        'element': [],
        'type_dict': {}
    },
    '0010': {
        'name': u'灌溉计划召测上行',
        'type': '上行',
        'default': ['position'],
        'element': [],
        'type_dict': {}
    },
    '0011': {
        'name': u'网关数据上报应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    },
    '0012': {
        'name': u'网关合法终端设置上行',
        'type': '上行',
        'default': ['current_type'],
        'element': [],
        'type_dict': {}
    },
    '0013': {
        'name': u'网关合法终端召测上行',
        'type': '上行',
        'default': ['position'],
        'element': [],
        'type_dict': {}
    },
    '0018': {
        'name': u'墒情数据上报应答',
        'type': '应答',
        'default': ['error_sign'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['0001', '0002', '0003', '0004', '0005', '0011', '0018']

# 错误响应
ERROR_RESPONSE = [
    {
        'code': 'error_sign',
        'name': u'错误标志',
        'default': '01',
    },
    {
        'code': 'error_type',
        'name': u'错误类型',
        'default': '01',
    }
]

# 配置的CLASS
__CLASS__ = 'LORASettingInfo'


class LORASettingInfo(object):
    """
    获取LORA配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__is_save_list = IS_SAVE_LIST
        self.__error_response = ERROR_RESPONSE

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
        获取平台发出报文的协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['default']]
        else:
            return []

    def get_error_response(self):
        """
        获取生成错误响应解析
        :return:
        """
        return self.__error_response


if __name__ == '__main__':
    set = LORASettingInfo()
    print(set.get_platform_2_device_protocol_dict('0001'))
