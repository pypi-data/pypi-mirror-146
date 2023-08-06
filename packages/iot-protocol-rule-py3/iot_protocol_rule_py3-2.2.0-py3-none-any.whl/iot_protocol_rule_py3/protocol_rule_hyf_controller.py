# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/06/29

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'start_address': {
        'code': 'start_address',
        'name': '起始地址',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'register_count': {
        'code': 'register_count',
        'name': '寄存器个数',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'write_data': {
        'code': 'write_data',
        'name': '写入内容',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    # 实时参数
    '2000': {
        'code': 'equip_inside_over_temperature',
        'name': '设备机内超温',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '200C': {
        'code': 'day_night',
        'name': '白天夜晚',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    '3011': {
        'code': 'controller_func_status_1',
        'name': '控制器功能状态1',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3012': {
        'code': 'controller_func_status_2',
        'name': '控制器功能状态2',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3013': {
        'code': 'controller_func_status_3',
        'name': '控制器功能状态3',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3014': {
        'code': 'controller_func_status_4',
        'name': '控制器功能状态4',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3015': {
        'code': 'LVD_min_value',
        'name': '锂电LVD最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3016': {
        'code': 'LVD_max_value',
        'name': '锂电LVD最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3017': {
        'code': 'LVD_default_value',
        'name': '锂电LVD默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3018': {
        'code': 'LVR_min_value',
        'name': '锂电LVR最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3019': {
        'code': 'LVR_max_value',
        'name': '锂电LVR最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '301A': {
        'code': 'LVR_default_value',
        'name': '锂电LVR默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '301B': {
        'code': 'CVT_min_value',
        'name': '锂电CVT最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '301C': {
        'code': 'CVT_max_value',
        'name': '锂电CVT最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '301D': {
        'code': 'CVT_default_value',
        'name': '锂电CVT默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '301E': {
        'code': 'CVR_min_value',
        'name': '锂电CVR最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '301F': {
        'code': 'CVR_max_value',
        'name': '锂电CVR最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3020': {
        'code': 'CVR_default_value',
        'name': '锂电CVR默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3021': {
        'code': 'light_control_point_min_value',
        'name': '锂电天黑光控点最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3022': {
        'code': 'light_control_point_max_value',
        'name': '锂电天黑光控点最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3023': {
        'code': 'light_control_point_default_value',
        'name': '锂电天黑光控点默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3024': {
        'code': 'auto_reduce_power_point_min_value',
        'name': '锂电自动降功率点最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3025': {
        'code': 'auto_reduce_power_point_max_value',
        'name': '锂电自动降功率点最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3026': {
        'code': 'auto_reduce_power_point_default_value',
        'name': '锂电自动降功率点默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3027': {
        'code': 'load_electric_current_min_value',
        'name': '负载电流最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3028': {
        'code': 'load_electric_current_max_value',
        'name': '负载电流最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3029': {
        'code': 'CVT_CVR_max_allow_differential_pressure',
        'name': '锂电池CVT与CVR最大允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '302A': {
        'code': 'CVT_CVR_min_allow_differential_pressure',
        'name': '锂电池CVT与CVR最小允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '302B': {
        'code': 'LVD_LVR_min_allow_differential_pressure',
        'name': '锂电池LVD与LVR最小允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '302C': {
        'code': 'CVR_LVD&CVT_LVR_min_allow_differential_pressure',
        'name': '锂电CVR与LVD及CVT与LVR最小允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3030': {
        'code': 'slave_ID',
        'name': '从机ID',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''},
    '3031': {
        'code': 'running_days',
        'name': '运行天数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3032': {
        'code': 'current_battery_voltage_level',
        'name': '当前蓄电池电压等级',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3033': {
        'code': 'battery_status',
        'name': '蓄电池状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3034': {
        'code': 'charging_device_status',
        'name': '充电设备状态',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3035': {
        'code': 'discharge_device_status',
        'name': '放电设备状态',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3036': {
        'code': 'ambient_temperature',
        'name': '环境温度',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3037': {
        'code': 'device_internal_temperature',
        'name': '设备机内温度',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3038': {
        'code': 'overplay_times',
        'name': '过放次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3039': {
        'code': 'filling_times',
        'name': '充满次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '303A': {
        'code': 'over_voltage_protect_times',
        'name': '过压保护次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '303B': {
        'code': 'over_current_protect_times',
        'name': '过流保护次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '303C': {
        'code': 'short_circuit_protect_times',
        'name': '短路保护次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '303D': {
        'code': 'open_circuit_protect_times',
        'name': '开路保护次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '303E': {
        'code': 'hardware_protect_times',
        'name': '硬件保护次数',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '303F': {
        'code': 'charging_over_temperature_protect_times',
        'name': '充电过温保护次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3040': {
        'code': 'discharge_over_temperature_protect_times',
        'name': '放电过温保护次数',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3045': {
        'code': 'battery_remaining_electricity',
        'name': '蓄电池剩余电量',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3046': {
        'code': 'battery_voltage',
        'name': '蓄电池电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3047': {
        'code': 'battery_current',
        'name': '蓄电池电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3048': {
        'code': 'battery_power',
        'name': '蓄电池功率',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '304A': {
        'code': 'load_voltage',
        'name': '负载电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '304B': {
        'code': 'load_current',
        'name': '负载电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '304C': {
        'code': 'load_power',
        'name': '负载功率',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '304E': {
        'code': 'solar_voltage',
        'name': '太阳能电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '304F': {
        'code': 'solar_current',
        'name': '太阳能电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3050': {
        'code': 'power_generation',
        'name': '发电功率',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3052': {
        'code': 'total_charging_capacity_day',
        'name': '当日累积充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3053': {
        'code': 'total_charging_capacity',
        'name': '总累积充电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3055': {
        'code': 'total_used_electricity_quantity_day',
        'name': '当日累计用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3056': {
        'code': 'total_used_electricity_quantity',
        'name': '总累计用电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3058': {
        'code': 'history_light_duration',
        'name': '历史亮灯时长',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3059': {
        'code': 'multiple_devices_total_charging_capacity',
        'name': '多台设备级联时总累计充电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '305B': {
        'code': 'multiple_devices_total_used_electricity',
        'name': '多台设备级联时总累计用电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '305D': {
        'code': 'total_charging_capacity_month',
        'name': '当月累积充电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '305F': {
        'code': 'total_charging_capacity_year',
        'name': '当年累积充电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3061': {
        'code': 'charging_capacity_day_1',
        'name': '1天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3062': {
        'code': 'charging_capacity_day_2',
        'name': '2天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3063': {
        'code': 'charging_capacity_day_3',
        'name': '3天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3064': {
        'code': 'charging_capacity_day_4',
        'name': '4天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3065': {
        'code': 'charging_capacity_day_5',
        'name': '5天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3066': {
        'code': 'charging_capacity_day_6',
        'name': '6天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3067': {
        'code': 'charging_capacity_day_7',
        'name': '7天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3068': {
        'code': 'charging_capacity_day_8',
        'name': '8天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3069': {
        'code': 'charging_capacity_day_9',
        'name': '9天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '306A': {
        'code': 'charging_capacity_day_10',
        'name': '10天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '306B': {
        'code': 'charging_capacity_day_11',
        'name': '11天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '306C': {
        'code': 'charging_capacity_day_12',
        'name': '12天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '306D': {
        'code': 'charging_capacity_day_13',
        'name': '13天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '306E': {
        'code': 'charging_capacity_day_14',
        'name': '14天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '306F': {
        'code': 'charging_capacity_day_15',
        'name': '15天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3070': {
        'code': 'charging_capacity_day_16',
        'name': '16天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3071': {
        'code': 'charging_capacity_day_17',
        'name': '17天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3072': {
        'code': 'charging_capacity_day_18',
        'name': '18天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3073': {
        'code': 'charging_capacity_day_19',
        'name': '19天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3074': {
        'code': 'charging_capacity_day_20',
        'name': '20天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3075': {
        'code': 'charging_capacity_day_21',
        'name': '21天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3076': {
        'code': 'charging_capacity_day_22',
        'name': '22天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3077': {
        'code': 'charging_capacity_day_23',
        'name': '23天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3078': {
        'code': 'charging_capacity_day_24',
        'name': '24天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3079': {
        'code': 'charging_capacity_day_25',
        'name': '25天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '307A': {
        'code': 'charging_capacity_day_26',
        'name': '26天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '307B': {
        'code': 'charging_capacity_day_27',
        'name': '27天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '307C': {
        'code': 'charging_capacity_day_28',
        'name': '28天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '307D': {
        'code': 'charging_capacity_day_29',
        'name': '29天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '307E': {
        'code': 'charging_capacity_day_30',
        'name': '30天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '307F': {
        'code': 'charging_capacity_day_31',
        'name': '31天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3080': {
        'code': 'charging_capacity_day_32',
        'name': '32天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3081': {
        'code': 'charging_capacity_day_33',
        'name': '33天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3082': {
        'code': 'charging_capacity_day_34',
        'name': '34天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3083': {
        'code': 'charging_capacity_day_35',
        'name': '35天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3084': {
        'code': 'charging_capacity_day_36',
        'name': '36天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3085': {
        'code': 'charging_capacity_day_37',
        'name': '37天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3086': {
        'code': 'charging_capacity_day_38',
        'name': '38天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3087': {
        'code': 'charging_capacity_day_39',
        'name': '39天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3088': {
        'code': 'charging_capacity_day_40',
        'name': '40天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3089': {
        'code': 'charging_capacity_day_41',
        'name': '41天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '308A': {
        'code': 'charging_capacity_day_42',
        'name': '42天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '308B': {
        'code': 'charging_capacity_day_43',
        'name': '43天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '308C': {
        'code': 'charging_capacity_day_44',
        'name': '44天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '308D': {
        'code': 'charging_capacity_day_45',
        'name': '45天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '308E': {
        'code': 'charging_capacity_day_46',
        'name': '46天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '308F': {
        'code': 'charging_capacity_day_47',
        'name': '47天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3090': {
        'code': 'charging_capacity_day_48',
        'name': '48天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3091': {
        'code': 'charging_capacity_day_49',
        'name': '49天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3092': {
        'code': 'charging_capacity_day_50',
        'name': '50天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3093': {
        'code': 'charging_capacity_day_51',
        'name': '51天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3094': {
        'code': 'charging_capacity_day_52',
        'name': '52天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3095': {
        'code': 'charging_capacity_day_53',
        'name': '53天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3096': {
        'code': 'charging_capacity_day_54',
        'name': '54天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3097': {
        'code': 'charging_capacity_day_55',
        'name': '55天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3098': {
        'code': 'charging_capacity_day_56',
        'name': '56天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3099': {
        'code': 'charging_capacity_day_57',
        'name': '57天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '309A': {
        'code': 'charging_capacity_day_58',
        'name': '58天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '309B': {
        'code': 'charging_capacity_day_59',
        'name': '59天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '309C': {
        'code': 'charging_capacity_day_60',
        'name': '60天前充电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30A8': {
        'code': 'battery_voltage_max_day',
        'name': '当日最高蓄电池电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30A9': {
        'code': 'battery_voltage_min_day',
        'name': '当日最低蓄电池电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30AA': {
        'code': 'battery_voltage_max_1',
        'name': '1天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30AB': {
        'code': 'battery_voltage_max_2',
        'name': '2天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30AC': {
        'code': 'battery_voltage_max_3',
        'name': '3天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30AD': {
        'code': 'battery_voltage_max_4',
        'name': '4天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30AE': {
        'code': 'battery_voltage_max_5',
        'name': '5天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '30AF': {
        'code': 'battery_voltage_max_6',
        'name': '6天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B0': {
        'code': 'battery_voltage_max_7',
        'name': '7天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B1': {
        'code': 'battery_voltage_max_8',
        'name': '8天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B2': {
        'code': 'battery_voltage_max_9',
        'name': '9天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B3': {
        'code': 'battery_voltage_max_10',
        'name': '10天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B4': {
        'code': 'battery_voltage_max_11',
        'name': '11天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B5': {
        'code': 'battery_voltage_max_12',
        'name': '12天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B6': {
        'code': 'battery_voltage_max_13',
        'name': '13天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B7': {
        'code': 'battery_voltage_max_14',
        'name': '14天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B8': {
        'code': 'battery_voltage_max_15',
        'name': '15天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30B9': {
        'code': 'battery_voltage_max_16',
        'name': '16天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30BA': {
        'code': 'battery_voltage_max_17',
        'name': '17天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30BB': {
        'code': 'battery_voltage_max_18',
        'name': '18天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30BC': {
        'code': 'battery_voltage_max_19',
        'name': '19天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30BD': {
        'code': 'battery_voltage_max_20',
        'name': '20天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30BE': {
        'code': 'battery_voltage_max_21',
        'name': '21天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30BF': {
        'code': 'battery_voltage_max_22',
        'name': '22天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C0': {
        'code': 'battery_voltage_max_23',
        'name': '23天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C1': {
        'code': 'battery_voltage_max_24',
        'name': '24天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C2': {
        'code': 'battery_voltage_max_25',
        'name': '25天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C3': {
        'code': 'battery_voltage_max_26',
        'name': '26天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C4': {
        'code': 'battery_voltage_max_27',
        'name': '27天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C5': {
        'code': 'battery_voltage_max_28',
        'name': '28天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C6': {
        'code': 'battery_voltage_max_29',
        'name': '29天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C7': {
        'code': 'battery_voltage_max_30',
        'name': '30天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C8': {
        'code': 'battery_voltage_max_31',
        'name': '31天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30C9': {
        'code': 'battery_voltage_max_32',
        'name': '32天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30CA': {
        'code': 'battery_voltage_max_33',
        'name': '33天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30CB': {
        'code': 'battery_voltage_max_34',
        'name': '34天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30CC': {
        'code': 'battery_voltage_max_35',
        'name': '35天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30CD': {
        'code': 'battery_voltage_max_36',
        'name': '36天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30CE': {
        'code': 'battery_voltage_max_37',
        'name': '37天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30CF': {
        'code': 'battery_voltage_max_38',
        'name': '38天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D0': {
        'code': 'battery_voltage_max_39',
        'name': '39天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D1': {
        'code': 'battery_voltage_max_40',
        'name': '40天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D2': {
        'code': 'battery_voltage_max_41',
        'name': '41天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D3': {
        'code': 'battery_voltage_max_42',
        'name': '42天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D4': {
        'code': 'battery_voltage_max_43',
        'name': '43天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D5': {
        'code': 'battery_voltage_max_44',
        'name': '44天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D6': {
        'code': 'battery_voltage_max_45',
        'name': '45天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D7': {
        'code': 'battery_voltage_max_46',
        'name': '46天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D8': {
        'code': 'battery_voltage_max_47',
        'name': '47天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30D9': {
        'code': 'battery_voltage_max_48',
        'name': '48天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30DA': {
        'code': 'battery_voltage_max_49',
        'name': '49天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30DB': {
        'code': 'battery_voltage_max_50',
        'name': '50天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30DC': {
        'code': 'battery_voltage_max_51',
        'name': '51天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30DD': {
        'code': 'battery_voltage_max_52',
        'name': '52天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30DE': {
        'code': 'battery_voltage_max_53',
        'name': '53天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30DF': {
        'code': 'battery_voltage_max_54',
        'name': '54天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E0': {
        'code': 'battery_voltage_max_55',
        'name': '55天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E1': {
        'code': 'battery_voltage_max_56',
        'name': '56天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E2': {
        'code': 'battery_voltage_max_57',
        'name': '57天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E3': {
        'code': 'battery_voltage_max_58',
        'name': '58天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E4': {
        'code': 'battery_voltage_max_59',
        'name': '59天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E5': {
        'code': 'battery_voltage_max_60',
        'name': '60天前电池最高电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E6': {
        'code': 'battery_voltage_min_1',
        'name': '1天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E7': {
        'code': 'battery_voltage_min_2',
        'name': '2天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E8': {
        'code': 'battery_voltage_min_3',
        'name': '3天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30E9': {
        'code': 'battery_voltage_min_4',
        'name': '4天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30EA': {
        'code': 'battery_voltage_min_5',
        'name': '5天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30EB': {
        'code': 'battery_voltage_min_6',
        'name': '6天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30EC': {
        'code': 'battery_voltage_min_7',
        'name': '7天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30ED': {
        'code': 'battery_voltage_min_8',
        'name': '8天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30EE': {
        'code': 'battery_voltage_min_9',
        'name': '9天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30EF': {
        'code': 'battery_voltage_min_10',
        'name': '10天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F0': {
        'code': 'battery_voltage_min_11',
        'name': '11天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F1': {
        'code': 'battery_voltage_min_12',
        'name': '12天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F2': {
        'code': 'battery_voltage_min_13',
        'name': '13天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F3': {
        'code': 'battery_voltage_min_14',
        'name': '14天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F4': {
        'code': 'battery_voltage_min_15',
        'name': '15天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F5': {
        'code': 'battery_voltage_min_16',
        'name': '16天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F6': {
        'code': 'battery_voltage_min_17',
        'name': '17天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F7': {
        'code': 'battery_voltage_min_18',
        'name': '18天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F8': {
        'code': 'battery_voltage_min_19',
        'name': '19天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30F9': {
        'code': 'battery_voltage_min_20',
        'name': '20天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30FA': {
        'code': 'battery_voltage_min_21',
        'name': '21天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30FB': {
        'code': 'battery_voltage_min_22',
        'name': '22天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30FC': {
        'code': 'battery_voltage_min_23',
        'name': '23天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30FD': {
        'code': 'battery_voltage_min_24',
        'name': '24天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30FE': {
        'code': 'battery_voltage_min_25',
        'name': '25天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30FF': {
        'code': 'battery_voltage_min_26',
        'name': '26天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3100': {
        'code': 'battery_voltage_min_27',
        'name': '27天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3101': {
        'code': 'battery_voltage_min_28',
        'name': '28天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3102': {
        'code': 'battery_voltage_min_29',
        'name': '29天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3103': {
        'code': 'battery_voltage_min_30',
        'name': '30天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3104': {
        'code': 'battery_voltage_min_31',
        'name': '31天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3105': {
        'code': 'battery_voltage_min_32',
        'name': '32天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3106': {
        'code': 'battery_voltage_min_33',
        'name': '33天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3107': {
        'code': 'battery_voltage_min_34',
        'name': '34天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3108': {
        'code': 'battery_voltage_min_35',
        'name': '35天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3109': {
        'code': 'battery_voltage_min_36',
        'name': '36天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '310A': {
        'code': 'battery_voltage_min_37',
        'name': '37天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '310B': {
        'code': 'battery_voltage_min_38',
        'name': '38天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '310C': {
        'code': 'battery_voltage_min_39',
        'name': '39天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '310D': {
        'code': 'battery_voltage_min_40',
        'name': '40天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '310E': {
        'code': 'battery_voltage_min_41',
        'name': '41天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '310F': {
        'code': 'battery_voltage_min_42',
        'name': '42天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3110': {
        'code': 'battery_voltage_min_43',
        'name': '43天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3111': {
        'code': 'battery_voltage_min_44',
        'name': '44天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3112': {
        'code': 'battery_voltage_min_45',
        'name': '45天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3113': {
        'code': 'battery_voltage_min_46',
        'name': '46天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3114': {
        'code': 'battery_voltage_min_47',
        'name': '47天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3115': {
        'code': 'battery_voltage_min_48',
        'name': '48天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3116': {
        'code': 'battery_voltage_min_49',
        'name': '49天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3117': {
        'code': 'battery_voltage_min_50',
        'name': '50天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3118': {
        'code': 'battery_voltage_min_51',
        'name': '51天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3119': {
        'code': 'battery_voltage_min_52',
        'name': '52天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '311A': {
        'code': 'battery_voltage_min_53',
        'name': '53天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '311B': {
        'code': 'battery_voltage_min_54',
        'name': '54天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '311C': {
        'code': 'battery_voltage_min_55',
        'name': '55天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '311D': {
        'code': 'battery_voltage_min_56',
        'name': '56天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '311E': {
        'code': 'battery_voltage_min_57',
        'name': '57天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '311F': {
        'code': 'battery_voltage_min_58',
        'name': '58天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3120': {
        'code': 'battery_voltage_min_59',
        'name': '59天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3121': {
        'code': 'battery_voltage_min_60',
        'name': '60天前电池最低电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '312A': {
        'code': 'total_used_electricity_quantity_month',
        'name': '当月累计用电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '312C': {
        'code': 'total_used_electricity_quantity_year',
        'name': '当年累计用电量',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3130': {
        'code': 'used_electricity_quantity_1',
        'name': '1天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3131': {
        'code': 'used_electricity_quantity_2',
        'name': '2天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3132': {
        'code': 'used_electricity_quantity_3',
        'name': '3天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3133': {
        'code': 'used_electricity_quantity_4',
        'name': '4天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3134': {
        'code': 'used_electricity_quantity_5',
        'name': '5天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3135': {
        'code': 'used_electricity_quantity_6',
        'name': '6天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3136': {
        'code': 'used_electricity_quantity_7',
        'name': '7天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3137': {
        'code': 'used_electricity_quantity_8',
        'name': '8天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3138': {
        'code': 'used_electricity_quantity_9',
        'name': '9天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3139': {
        'code': 'used_electricity_quantity_10',
        'name': '10天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '313A': {
        'code': 'used_electricity_quantity_11',
        'name': '11天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '313B': {
        'code': 'used_electricity_quantity_12',
        'name': '12天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '313C': {
        'code': 'used_electricity_quantity_13',
        'name': '13天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '313D': {
        'code': 'used_electricity_quantity_14',
        'name': '14天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '313E': {
        'code': 'used_electricity_quantity_15',
        'name': '15天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '313F': {
        'code': 'used_electricity_quantity_16',
        'name': '16天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3140': {
        'code': 'used_electricity_quantity_17',
        'name': '17天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3141': {
        'code': 'used_electricity_quantity_18',
        'name': '18天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3142': {
        'code': 'used_electricity_quantity_19',
        'name': '19天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3143': {
        'code': 'used_electricity_quantity_20',
        'name': '20天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3144': {
        'code': 'used_electricity_quantity_21',
        'name': '21天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3145': {
        'code': 'used_electricity_quantity_22',
        'name': '22天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3146': {
        'code': 'used_electricity_quantity_23',
        'name': '23天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3147': {
        'code': 'used_electricity_quantity_24',
        'name': '24天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3148': {
        'code': 'used_electricity_quantity_25',
        'name': '25天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3149': {
        'code': 'used_electricity_quantity_26',
        'name': '26天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '314A': {
        'code': 'used_electricity_quantity_27',
        'name': '27天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '314B': {
        'code': 'used_electricity_quantity_28',
        'name': '28天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '314C': {
        'code': 'used_electricity_quantity_29',
        'name': '29天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '314D': {
        'code': 'used_electricity_quantity_30',
        'name': '30天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '314E': {
        'code': 'used_electricity_quantity_31',
        'name': '31天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '314F': {
        'code': 'used_electricity_quantity_32',
        'name': '32天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3150': {
        'code': 'used_electricity_quantity_33',
        'name': '33天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3151': {
        'code': 'used_electricity_quantity_34',
        'name': '34天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3152': {
        'code': 'used_electricity_quantity_35',
        'name': '35天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3153': {
        'code': 'used_electricity_quantity_36',
        'name': '36天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3154': {
        'code': 'used_electricity_quantity_37',
        'name': '37天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3155': {
        'code': 'used_electricity_quantity_38',
        'name': '38天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3156': {
        'code': 'used_electricity_quantity_39',
        'name': '39天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3157': {
        'code': 'used_electricity_quantity_40',
        'name': '40天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3158': {
        'code': 'used_electricity_quantity_41',
        'name': '41天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3159': {
        'code': 'used_electricity_quantity_42',
        'name': '42天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '315A': {
        'code': 'used_electricity_quantity_43',
        'name': '43天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '315B': {
        'code': 'used_electricity_quantity_44',
        'name': '44天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '315C': {
        'code': 'used_electricity_quantity_45',
        'name': '45天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '315D': {
        'code': 'used_electricity_quantity_46',
        'name': '46天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '315E': {
        'code': 'used_electricity_quantity_47',
        'name': '47天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '315F': {
        'code': 'used_electricity_quantity_48',
        'name': '48天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3160': {
        'code': 'used_electricity_quantity_49',
        'name': '49天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3161': {
        'code': 'used_electricity_quantity_50',
        'name': '50天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3162': {
        'code': 'used_electricity_quantity_51',
        'name': '51天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3163': {
        'code': 'used_electricity_quantity_52',
        'name': '52天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3164': {
        'code': 'used_electricity_quantity_53',
        'name': '53天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3165': {
        'code': 'used_electricity_quantity_54',
        'name': '54天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3166': {
        'code': 'used_electricity_quantity_55',
        'name': '55天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3167': {
        'code': 'used_electricity_quantity_56',
        'name': '56天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3168': {
        'code': 'used_electricity_quantity_57',
        'name': '57天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3169': {
        'code': 'used_electricity_quantity_58',
        'name': '58天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '316A': {
        'code': 'used_electricity_quantity_59',
        'name': '59天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '316B': {
        'code': 'used_electricity_quantity_60',
        'name': '60天前用电量',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3175': {
        'code': 'specific_time_1',
        'name': '1天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3176': {
        'code': 'specific_time_2',
        'name': '2天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3177': {
        'code': 'specific_time_3',
        'name': '3天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3178': {
        'code': 'specific_time_4',
        'name': '4天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3179': {
        'code': 'specific_time_5',
        'name': '5天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '317A': {
        'code': 'specific_time_6',
        'name': '6天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '317B': {
        'code': 'specific_time_7',
        'name': '7天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '317C': {
        'code': 'specific_time_8',
        'name': '8天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '317D': {
        'code': 'specific_time_9',
        'name': '9天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '317E': {
        'code': 'specific_time_10',
        'name': '10天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '317F': {
        'code': 'specific_time_11',
        'name': '11天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3180': {
        'code': 'specific_time_12',
        'name': '12天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3181': {
        'code': 'specific_time_13',
        'name': '13天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3182': {
        'code': 'specific_time_14',
        'name': '14天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3183': {
        'code': 'specific_time_15',
        'name': '15天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3184': {
        'code': 'specific_time_16',
        'name': '16天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3185': {
        'code': 'specific_time_17',
        'name': '17天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3186': {
        'code': 'specific_time_18',
        'name': '18天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3187': {
        'code': 'specific_time_19',
        'name': '19天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3188': {
        'code': 'specific_time_20',
        'name': '20天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3189': {
        'code': 'specific_time_21',
        'name': '21天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '318A': {
        'code': 'specific_time_22',
        'name': '22天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '318B': {
        'code': 'specific_time_23',
        'name': '23天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '318C': {
        'code': 'specific_time_24',
        'name': '24天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '318D': {
        'code': 'specific_time_25',
        'name': '25天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '318E': {
        'code': 'specific_time_26',
        'name': '26天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '318F': {
        'code': 'specific_time_27',
        'name': '27天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3190': {
        'code': 'specific_time_28',
        'name': '28天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3191': {
        'code': 'specific_time_29',
        'name': '29天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3192': {
        'code': 'specific_time_30',
        'name': '30天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3193': {
        'code': 'specific_time_31',
        'name': '31天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3194': {
        'code': 'specific_time_32',
        'name': '32天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3195': {
        'code': 'specific_time_33',
        'name': '33天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3196': {
        'code': 'specific_time_34',
        'name': '34天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3197': {
        'code': 'specific_time_35',
        'name': '35天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3198': {
        'code': 'specific_time_36',
        'name': '36天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3199': {
        'code': 'specific_time_37',
        'name': '37天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '319A': {
        'code': 'specific_time_38',
        'name': '38天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '319B': {
        'code': 'specific_time_39',
        'name': '39天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '319C': {
        'code': 'specific_time_40',
        'name': '40天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '319D': {
        'code': 'specific_time_41',
        'name': '41天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '319E': {
        'code': 'specific_time_42',
        'name': '42天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '319F': {
        'code': 'specific_time_43',
        'name': '43天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A0': {
        'code': 'specific_time_44',
        'name': '44天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A1': {
        'code': 'specific_time_45',
        'name': '45天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A2': {
        'code': 'specific_time_46',
        'name': '46天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A3': {
        'code': 'specific_time_47',
        'name': '47天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A4': {
        'code': 'specific_time_48',
        'name': '48天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A5': {
        'code': 'specific_time_49',
        'name': '49天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A6': {
        'code': 'specific_time_50',
        'name': '50天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A7': {
        'code': 'specific_time_51',
        'name': '51天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A8': {
        'code': 'specific_time_52',
        'name': '52天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31A9': {
        'code': 'specific_time_53',
        'name': '53天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31AA': {
        'code': 'specific_time_54',
        'name': '54天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31AB': {
        'code': 'specific_time_55',
        'name': '55天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31AC': {
        'code': 'specific_time_56',
        'name': '56天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31AD': {
        'code': 'specific_time_57',
        'name': '57天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31AE': {
        'code': 'specific_time_58',
        'name': '58天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31AF': {
        'code': 'specific_time_59',
        'name': '59天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '31B0': {
        'code': 'specific_time_60',
        'name': '60天前具体对应时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_date', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    # 额定参数 04
    '3000': {
        'code': 'solar_rated_voltage',
        'name': '太阳能额定电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3001': {
        'code': 'solar_rated_current',
        'name': '太阳能额定电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3002': {
        'code': 'solar_rated_power',
        'name': '太阳能额定功率',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3004': {
        'code': 'battery_rated_voltage',
        'name': '蓄电池额定电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3005': {
        'code': 'battery_rated_current',
        'name': '蓄电池额定电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3006': {
        'code': 'battery_rated_power',
        'name': '蓄电池额定功率',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3008': {
        'code': 'upload_rated_voltage',
        'name': '负载额定电压',
        'length': 4,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3009': {
        'code': 'upload_rated_current',
        'name': '负责额定电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '300A': {
        'code': 'upload_rated_power',
        'name': '负载额定功率',
        'length': 8,
        'de_plug': [
            {'code': 'HL_reverse_divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    # 读保持寄存器 03
    '8FF0': {
        'code': 'controller_func_status_1',
        'name': '控制器功能状态1',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF1': {
        'code': 'controller_func_status_2',
        'name': '控制器功能状态2',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF2': {
        'code': 'controller_func_status_3',
        'name': '控制器功能状态3',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF3': {
        'code': 'controller_func_status_4',
        'name': '控制器功能状态4',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF4': {
        'code': 'LVD_min_value',
        'name': '锂电LVD最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF5': {
        'code': 'LVD_max_value',
        'name': '锂电LVD最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF6': {
        'code': 'LVD_default_value',
        'name': '锂电LVD默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF7': {
        'code': 'LVR_min_value',
        'name': '锂电LVR最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF8': {
        'code': 'LVR_max_value',
        'name': '锂电LVR最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FF9': {
        'code': 'LVR_default_value',
        'name': '锂电LVR默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FFA': {
        'code': 'CVT_min_value',
        'name': '锂电CVT最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FFB': {
        'code': 'CVT_max_value',
        'name': '锂电CVT最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FFC': {
        'code': 'CVT_default_value',
        'name': '锂电CVT默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FFD': {
        'code': 'CVR_min_value',
        'name': '锂电CVR最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FFE': {
        'code': 'CVR_max_value',
        'name': '锂电CVR最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8FFF': {
        'code': 'CVR_default_value',
        'name': '锂电CVR默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9000': {
        'code': 'dark_light_control_point_min_value',
        'name': '锂电天黑光控点最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9001': {
        'code': 'Li_dark_light_control_point_max_value',
        'name': '锂电天黑光控点最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9002': {
        'code': 'Li_dark_light_control_point_default_value',
        'name': '锂电天黑光控点默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9003': {
        'code': 'Li_auto_reduce_power_point_min_value',
        'name': '锂电自动降功率点最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9004': {
        'code': 'Li_auto_reduce_power_point_max_value',
        'name': '锂电自动降功率点最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9005': {
        'code': 'Li_auto_reduce_power_point_default_value',
        'name': '锂电自动降功率点默认设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9006': {
        'code': 'load_electric_current_min_value',
        'name': '负载电流最小设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9007': {
        'code': 'load_electric_current_max_value',
        'name': '负载电流最大设置值',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9008': {
        'code': 'current_battery_voltage_level',
        'name': '当前蓄电池电压等级',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9009': {
        'code': 'CVT_CVR_max_allow_differential_pressure',
        'name': '锂电池CVT与CVR最大允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '900A': {
        'code': 'CVT_CVR_min_allow_differential_pressure',
        'name': '锂电池CVT与CVR最小允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '900B': {
        'code': 'LVD_LVR_min_allow_differential_pressure',
        'name': '锂电池LVD与LVR最小允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '900C': {
        'code': 'CVR_LVD&CVT_LVR_min_allow_differential_pressure',
        'name': '锂电CVR与LVD及CVT与LVR最小允许压差',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    # 读取设备参数  03（读） 06（写） 10（写）
    '9017': {
        'code': 'real_time_clock_s',
        'name': '实时时钟-秒',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9018': {
        'code': 'real_time_clock_m',
        'name': '实时时钟-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9019': {
        'code': 'real_time_clock_h',
        'name': '实时时钟-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '901A': {
        'code': 'real_time_clock_day',
        'name': '实时时钟-日',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '901B': {
        'code': 'real_time_clock_month',
        'name': '实时时钟-月',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '901C': {
        'code': 'real_time_clock_year',
        'name': '实时时钟-年',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '901D': {
        'code': 'baud_rate',
        'name': '波特率',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '901E': {
        'code': 'backlight_time',
        'name': '背光时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '901F': {
        'code': 'device_pwd',
        'name': '设备密码',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9020': {
        'code': 'slave_ID',
        'name': '从机ID',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    # 蓄电池及负载参数 03（读） 06（写） 10（写）
    '9021': {
        'code': 'battery_type',
        'name': '电池类型',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9022': {
        'code': 'low_voltage_protection',
        'name': '低压保护',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9023': {
        'code': 'low_voltage_recovery',
        'name': '低压恢复',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9024': {
        'code': 'strong_charging_voltage',
        'name': '强充电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9025': {
        'code': 'equalized_charging_voltage',
        'name': '均衡充电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9026': {
        'code': 'float_voltage',
        'name': '浮充电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9027': {
        'code': 'system_rated_voltage_level',
        'name': '系统额定电压等级',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9028': {
        'code': 'lithium_overcharge_protection',
        'name': '锂电过充保护',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9029': {
        'code': 'lithium_overcharge_recovery',
        'name': '锂电过充恢复',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '902A': {
        'code': 'lithium_battery_zero_charging',
        'name': '锂电零度充电',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '902B': {
        'code': 'MT_system_working_mode',
        'name': 'MT系统工作模式',
        'length': 4,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '902C': {
        'code': 'MT_manual_control_default_setting',
        'name': 'MT系列手动控制条件下默认设定的开/关',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '902D': {
        'code': 'MT_timed_open_period_1',
        'name': 'MT系列定时开时段_1',
        'length': 4,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '902E': {
        'code': 'MT_timed_open_period_2',
        'name': 'MT系列定时开时段_2',
        'length': 4,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '902F': {
        'code': 'timed_opening_1_second',
        'name': '定时开时刻1秒',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9030': {
        'code': 'timed_opening_1_minute',
        'name': '定时开时刻1分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9031': {
        'code': 'timed_opening_1_hour',
        'name': '定时开时刻1时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9032': {
        'code': 'timed_close_1_second',
        'name': '定时关时刻1秒',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9033': {
        'code': 'timed_close_1_minute',
        'name': '定时关时刻1分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9034': {
        'code': 'timed_close_1_hour',
        'name': '定时关时刻1时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9035': {
        'code': 'timed_opening_2_second',
        'name': '定时开时刻2秒',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9036': {
        'code': 'timed_opening_2_minute',
        'name': '定时开时刻2分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9037': {
        'code': 'timed_opening_2_hour',
        'name': '定时开时刻2时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9038': {
        'code': 'timed_close_2_second',
        'name': '定时关时刻2秒',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9039': {
        'code': 'timed_close_2_minute',
        'name': '定时关时刻2分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '903A': {
        'code': 'timed_close_2_hour',
        'name': '定时关时刻2时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '903B': {
        'code': 'timing_control_period_selection',
        'name': '定时控制时间段选择',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '903C': {
        'code': 'light_control_dark_voltage',
        'name': '光控天黑电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '903D': {
        'code': 'light_control_delay',
        'name': '光控延时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '903E': {
        'code': 'DC_timed_control_period_1_power',
        'name': 'DC系列定时控制时间段1功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '903F': {
        'code': 'DC_timed_control_period_2_power',
        'name': 'DC系列定时控制时间段2功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9040': {
        'code': 'DC_1_time',
        'name': 'DC系列第一时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9041': {
        'code': 'DC_1_power',
        'name': 'DC系列第一功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9042': {
        'code': 'DC_2_time',
        'name': 'DC系列第二时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9043': {
        'code': 'DC_2_power',
        'name': 'DC系列第二功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9044': {
        'code': 'DC_3_time',
        'name': 'DC系列第三时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9045': {
        'code': 'DC_3_power',
        'name': 'DC系列第三功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9046': {
        'code': 'DC_4_time',
        'name': 'DC系列第四时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9047': {
        'code': 'DC_4_power',
        'name': 'DC系列第四功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9048': {
        'code': 'DC_5_time',
        'name': 'DC系列第五时间',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9049': {
        'code': 'DC_5_power',
        'name': 'DC系列第五功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '904A': {
        'code': 'DC_5_load_current',
        'name': 'DC系列负载电流',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '904B': {
        'code': 'DC_auto_reduce_power',
        'name': 'DC系列自动降功',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '904C': {
        'code': 'DC_power_reduce_point',
        'name': 'DC系列降功率点',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '904D': {
        'code': 'DC_power_reduce_ratio',
        'name': 'DC系列降功比例',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '904E': {
        'code': 'DC_infrared_delay_close',
        'name': 'DC系列红外延时关闭',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '904F': {
        'code': 'DC_infrared_unmanned_power',
        'name': 'DC系列红外无人功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9052': {
        'code': 'light_control_switch',
        'name': '光控开关',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9053': {
        'code': 'light_control_daylight_voltage',
        'name': '光控天亮电压',
        'length': 4,
        'de_plug': [
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9054': {
        'code': 'dimming_brightness_ratio',
        'name': '调光亮度比例',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9055': {
        'code': 'period_1_time_hour',
        'name': '时间段1时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9056': {
        'code': 'period_1_time_minute',
        'name': '时间段1时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9057': {
        'code': 'period_1_power',
        'name': '时间段1功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9058': {
        'code': 'period_2_time_hour',
        'name': '时间段2时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9059': {
        'code': 'period_2_time_minute',
        'name': '时间段2时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '905A': {
        'code': 'period_2_power',
        'name': '时间段2功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '905B': {
        'code': 'period_3_time_hour',
        'name': '时间段3时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '905C': {
        'code': 'period_3_time_minute',
        'name': '时间段3时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '905D': {
        'code': 'period_3_power',
        'name': '时间段3功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '905E': {
        'code': 'period_4_time_hour',
        'name': '时间段4时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '905F': {
        'code': 'period_4_time_minute',
        'name': '时间段4时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9060': {
        'code': 'period_4_power',
        'name': '时间段4功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9061': {
        'code': 'period_5_time_hour',
        'name': '时间段5时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9062': {
        'code': 'period_5_time_minute',
        'name': '时间段5时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9063': {
        'code': 'period_5_power',
        'name': '时间段5功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9064': {
        'code': 'period_6_time_hour',
        'name': '时间段6时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9065': {
        'code': 'period_6_time_minute',
        'name': '时间段6时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9066': {
        'code': 'period_6_power',
        'name': '时间段6功率',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9067': {
        'code': 'end_time_hour',
        'name': '结束时间-时',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9068': {
        'code': 'end_time_minute',
        'name': '结束时间-分',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    # 开关量 05
    '0000': {
        'code': 'output_manual_control_switch',
        'name': '输出手动控制开关',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'output_manual_control_switch',
        'name': '测试键开关',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'DC_timed_control_switch',
        'name': 'DC系列定时控制模式开关',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'manual_control_charging_switch',
        'name': '手动控制充电开关',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'restore_system_default',
        'name': '恢复系统默认值',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'cls_running_day&power_consumption&history_voltage',
        'name': '清除运行天数，发电用电数，历史最低最高电压',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'cls_protect&fill_times',
        'name': '清除所有保护次数及充满次数',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'cls_Magic_system_charge_discharge_AHnumbers',
        'name': '清除Magic系统充放电AH数',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'cls_all_history_data',
        'name': '清除以上所有历史数据',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '03': {
        'name': '读保持寄存器响应',
        'type': '应答',
        'default': [],
        'element': ['8FF0', '8FF1', '8FF2', '8FF3', '8FF4', '8FF5', '8FF6', '8FF7', '8FF8', '8FF9', '8FFA', '8FFB',
                    '8FFC', '8FFD', '8FFE', '8FFF', '9000', '9001', '9002', '9003', '9004', '9005', '9006', '9007',
                    '9008', '9009', '900A', '900B', '900C', '9017', '9018', '9019', '901A', '901B', '901C', '901D',
                    '901E', '901F', '9020', '9021', '9022', '9023', '9024', '9025', '9026', '9027', '9028', '9029',
                    '902A', '902B', '902C', '902D', '902E', '902F', '9030', '9031', '9032', '9033', '9034', '9035',
                    '9036', '9037', '9038', '9039', '903A', '903B', '903C', '903D', '903E', '903F', '9040', '9041',
                    '9042', '9043', '9044', '9045', '9046', '9047', '9048', '9049', '904A', '904B', '904C', '904D',
                    '904E', '904F', '9052', '9053', '9054', '9055', '9056', '9057', '9058', '9059', '905A', '905B',
                    '905C', '905D', '905E', '905F', '9060', '9061', '9062', '9063', '9064', '9065', '9066', '9067',
                    '9068'],
        'type_dict': {}
    },
    '04': {
        'name': '读取参数响应',
        'type': '应答',
        'default': [],
        'element': ['3011', '3012', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '301A', '301B', '301C',
                    '301D', '301E', '301F', '3020', '3021', '3022', '3023', '3024', '3025', '3026', '3027', '3028',
                    '3029', '302A', '302B', '302C', '3030', '3031', '3032', '3033', '3034', '3035', '3036', '3037',
                    '3038', '3039', '303A', '303B', '303C', '303D', '303E', '303F', '3040', '3045', '3046', '3047',
                    '3048', '304A', '304B', '304C', '304E', '304F', '3050', '3052', '3053', '3055', '3056', '3058',
                    '3059', '305B', '305D', '305F', '3061', '3062', '3063', '3064', '3065', '3066', '3067', '3068',
                    '3069', '306A', '306B', '306C', '306D', '306E', '306F', '3070', '3071', '3072', '3073', '3074',
                    '3075', '3076', '3077', '3078', '3079', '307A', '307B', '307C', '307D', '307E', '307F', '3080',
                    '3081', '3082', '3083', '3084', '3085', '3086', '3087', '3088', '3089', '308A', '308B', '308C',
                    '308D', '308E', '308F', '3090', '3091', '3092', '3093', '3094', '3095', '3096', '3097', '3098',
                    '3099', '309A', '309B', '309C', '30A8', '30A9', '30AA', '30AB', '30AC', '30AD', '30AE', '30AF',
                    '30B0', '30B1', '30B2', '30B3', '30B4', '30B5', '30B6', '30B7', '30B8', '30B9', '30BA', '30BB',
                    '30BC', '30BD', '30BE', '30BF', '30C0', '30C1', '30C2', '30C3', '30C4', '30C5', '30C6', '30C7',
                    '30C8', '30C9', '30CA', '30CB', '30CC', '30CD', '30CE', '30CF', '30D0', '30D1', '30D2', '30D3',
                    '30D4', '30D5', '30D6', '30D7', '30D8', '30D9', '30DA', '30DB', '30DC', '30DD', '30DE', '30DF',
                    '30E0', '30E1', '30E2', '30E3', '30E4', '30E5', '30E6', '30E7', '30E8', '30E9', '30EA', '30EB',
                    '30EC', '30ED', '30EE', '30EF', '30F0', '30F1', '30F2', '30F3', '30F4', '30F5', '30F6', '30F7',
                    '30F8', '30F9', '30FA', '30FB', '30FC', '30FD', '30FE', '30FF', '3100', '3101', '3102', '3103',
                    '3104', '3105', '3106', '3107', '3108', '3109', '310A', '310B', '310C', '310D', '310E', '310F',
                    '3110', '3111', '3112', '3113', '3114', '3115', '3116', '3117', '3118', '3119', '311A', '311B',
                    '311C', '311D', '311E', '311F', '3120', '3121', '312A', '312C', '3130', '3131', '3132', '3133',
                    '3134', '3135', '3136', '3137', '3138', '3139', '313A', '313B', '313C', '313D', '313E', '313F',
                    '3140', '3141', '3142', '3143', '3144', '3145', '3146', '3147', '3148', '3149', '314A', '314B',
                    '314C', '314D', '314E', '314F', '3150', '3151', '3152', '3153', '3154', '3155', '3156', '3157',
                    '3158', '3159', '315A', '315B', '315C', '315D', '315E', '315F', '3160', '3161', '3162', '3163',
                    '3164', '3165', '3166', '3167', '3168', '3169', '316A', '316B', '3175', '3176', '3177', '3178',
                    '3179', '317A', '317B', '317C', '317D', '317E', '317F', '3180', '3181', '3182', '3183', '3184',
                    '3185', '3186', '3187', '3188', '3189', '318A', '318B', '318C', '318D', '318E', '318F', '3190',
                    '3191', '3192', '3193', '3194', '3195', '3196', '3197', '3198', '3199', '319A', '319B', '319C',
                    '319D', '319E', '319F', '31A0', '31A1', '31A2', '31A3', '31A4', '31A5', '31A6', '31A7', '31A8',
                    '31A9', '31AA', '31AB', '31AC', '31AD', '31AE', '31AF', '31B0', '3000', '3001', '3002', '3004',
                    '3005', '3006', '3008', '3009', '300A'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '04': {
        'name': '读取参数',
        'type': '上行',
        'default': [],
        'element': ['start_address', 'register_count'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'HYFControllerSettingInfo'


class HYFControllerSettingInfo(object):
    """
    京源协议配置信息
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
    settingInfo = HYFControllerSettingInfo()
    dd = settingInfo.get_device_2_platform_protocol_dict('04')
    dd_name = [item['name'] for item in dd]
    for item in settingInfo.get_device_2_platform_protocol_dict('03'):
        if item['name'] not in dd_name:
            print(item['name'])
