# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/08/10

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'serial_number',
        'name': '序列号',
        'type': 'element',
        'length': 38,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'software_version',
        'name': '软件版本',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'hardware_version',
        'name': '硬件版本',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'reset_number',
        'name': '复位次数',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'heartbeat_type',
        'name': '心跳类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'reserve',
        'name': '保留',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'connect_mode',
        'name': '连接方式',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'device_time',
        'name': '设备时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'report_cycle',
        'name': '上报周期',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'collect_cycle',
        'name': '采集周期',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'storage_cycle',
        'name': '存储周期',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'signal_strength',
        'name': '信号强度',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'save_data',
        'name': '存储数据',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'not_report_data',
        'name': '未报数据',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'device_energy',
        'name': '设备能量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'reserve',
        'name': '保留',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'collect_time',
        'name': '采集时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date_check', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'channel_number',
        'name': '通道数',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'address',
        'name': '地址',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_address', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'save_type',
        'name': '存储类型',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'channel_0',
        'name': '通道0',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'channel_1',
        'name': '通道1',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'channel_2',
        'name': '通道2',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'channel_3',
        'name': '通道3',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'channel_4',
        'name': '通道4',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'channel_5',
        'name': '通道5',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'channel_6',
        'name': '通道6',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'channel_7',
        'name': '通道7',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'channel_8',
        'name': '通道8',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'channel_9',
        'name': '通道9',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'channel_10',
        'name': '通道10',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'channel_11',
        'name': '通道11',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'channel_12',
        'name': '通道12',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'channel_13',
        'name': '通道13',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'channel_14',
        'name': '通道14',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'channel_15',
        'name': '通道15',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'alarm_time',
        'name': '报警时间',
        'type': 'default',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date_check', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'alarm_type',
        'name': '报警类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'alarm_address',
        'name': '报警设备地址',
        'type': 'default',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_address', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'channel_no',
        'name': '通道号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'alarm_event',
        'name': '报警事件',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'channel_data_value',
        'name': '通道数据值',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '043': {
        'code': 'channel_data_change_value',
        'name': '通道数据变化值',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'alarm_limit_value',
        'name': '报警限值',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'device_address',
        'name': '设备地址',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_address', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'device_clock',
        'name': '设备时钟',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date_check', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'alarm_data_value',
        'name': '报警数值',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'error_status',
        'name': '异常状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '049': {
        'code': 'sequence',
        'name': '序号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '050': {
        'code': 'current_status',
        'name': '当前状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '051': {
        'code': 'event_time',
        'name': '事件时间',
        'type': 'default',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date_check', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '052': {
        'code': 'event_type',
        'name': '事件类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []},
            {'return': [], 'code': 'update_command', 'params': ['msg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'check_event_report', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '053': {
        'code': 'event_address',
        'name': '事件设备地址',
        'type': 'default',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_address', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '054': {
        'code': 'control_channel',
        'name': '控制通道',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '055': {
        'code': 'control_event',
        'name': '控制事件',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['msg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '056': {
        'code': 'control_mode',
        'name': '控制方式',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '057': {
        'code': 'control_user',
        'name': '控制用户',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '058': {
        'code': 'remnant_electric',
        'name': '用户剩余电量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '059': {
        'code': 'remnant_water',
        'name': '用户剩余水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '060': {
        'code': 'remnant_time',
        'name': '用户剩余时间',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '061': {
        'code': 'remnant_money',
        'name': '用户剩余金额',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '062': {
        'code': 'total_electric',
        'name': '当前累计电量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '063': {
        'code': 'total_water',
        'name': '当前累计水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '064': {
        'code': 'groundwater_level',
        'name': '当前地下水位',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '065': {
        'code': 'action_status',
        'name': '动作状态',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '066': {
        'code': 'action_type',
        'name': '动作类型',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '067': {
        'code': 'action_time',
        'name': '动作时间',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '068': {
        'code': 'set_degree',
        'name': '设置开度',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '069': {
        'code': 'current_degree',
        'name': '当前开度',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '070': {
        'code': 'run_time',
        'name': '运行时间',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '071': {
        'code': 'record_time',
        'name': '记录时间',
        'type': 'default',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date_check', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '072': {
        'code': 'record_type',
        'name': '记录类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '073': {
        'code': 'record_address',
        'name': '记录设备地址',
        'type': 'default',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '074': {
        'code': 'open_user',
        'name': '开启用户',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '075': {
        'code': 'open_time',
        'name': '开启时间',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '076': {
        'code': 'open_mode',
        'name': '开启方式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '077': {
        'code': 'close_user',
        'name': '关闭用户',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '078': {
        'code': 'close_time',
        'name': '关闭时间',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '079': {
        'code': 'close_mode',
        'name': '关闭方式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '080': {
        'code': 'use_water',
        'name': '用水',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '081': {
        'code': 'use_electric',
        'name': '用电',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '082': {
        'code': 'use_time',
        'name': '用时',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '083': {
        'code': 'use_money',
        'name': '用钱',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '084': {
        'code': 'water_head',
        'name': '水位差',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '085': {
        'code': 'water_pressure',
        'name': '出水压力',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '086': {
        'code': 'device_type',
        'name': '设备类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '087': {
        'code': 'device_serial_number',
        'name': '设备序列号',
        'type': 'element',
        'length': 14,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '088': {
        'code': 'software_version',
        'name': '软件版本',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '089': {
        'code': 'hardware_version',
        'name': '硬件版本',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '090': {
        'code': 'collect_cycle',
        'name': '采集周期',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '091': {
        'code': 'storage_cycle',
        'name': '存储周期',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '092': {
        'code': 'report_cycle',
        'name': '上报周期',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '093': {
        'code': 'app_type',
        'name': '应用类型',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '094': {
        'code': 'alarm_channel',
        'name': '报警通道',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '095': {
        'code': 'alarm_params',
        'name': '报警参数',
        'type': 'element',
        'length': 64,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '096': {
        'code': 'mark',
        'name': '标示',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '097': {
        'code': 'update_bit',
        'name': '更新位',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '098': {
        'code': 'network_param',
        'name': '网络参数',
        'type': 'element',
        'length': 16,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '099': {
        'code': 'report_param',
        'name': '上报参数',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '100': {
        'code': 'success_flag',
        'name': '成功标识',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '101': {
        'code': 'syn_sign',
        'name': '同步标示',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'check_equip_status', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '102': {
        'code': 'index_no',
        'name': '索引号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '103': {
        'code': 'channel_no',
        'name': '通道号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '104': {
        'code': 'address_vacancy',
        'name': '地址空位',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '105': {
        'code': 'water_meter_no',
        'name': '水表号',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '106': {
        'code': 'switch',
        'name': '开关',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '107': {
        'code': 'center_no',
        'name': '中心序号',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '108': {
        'code': 'fun_type',
        'name': '功能类型',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '109': {
        'code': 'address_type',
        'name': '地址类型',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '110': {
        'code': 'address_length',
        'name': '地址长度',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '111': {
        'code': 'address_string',
        'name': '地址字符串',
        'type': 'element',
        'length': 40,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_ip', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'ip_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '112': {
        'code': 'port',
        'name': '端口号',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_port', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'port_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '113': {
        'code': 'channel_index',
        'name': '通道索引',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '114': {
        'code': 'channel_status',
        'name': '通道状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '115': {
        'code': 'channel_type',
        'name': '通道类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '116': {
        'code': 'power_supply_mode',
        'name': '供电方式',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '117': {
        'code': 'device_index',
        'name': '设备索引',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '118': {
        'code': 'magnification',
        'name': '放大倍数',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '119': {
        'code': 'factory_calibration_parameter_a',
        'name': '出厂校正参数a',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '120': {
        'code': 'factory_calibration_parameter_b',
        'name': '出厂校正参数b',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '121': {
        'code': 'decimal_digits',
        'name': '小数位数',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '122': {
        'code': 'engineering_unit',
        'name': '工程单位',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '123': {
        'code': 'nonlinear_index',
        'name': '非线性索引',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '124': {
        'code': 'sensor_calibration_parameter_a',
        'name': '传感器校正参数a',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '125': {
        'code': 'sensor_calibration_parameter_b',
        'name': '传感器校正参数b',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '126': {
        'code': 'scene_calibration_parameter_a',
        'name': '现场校正参数a',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '127': {
        'code': 'scene_calibration_parameter_b',
        'name': '现场校正参数b',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '128': {
        'code': 'range_upper_limit',
        'name': '量程上限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '129': {
        'code': 'range_lower_limit',
        'name': '量程下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '130': {
        'code': 'control_status',
        'name': '控制状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '131': {
        'code': 'control_error',
        'name': '控制错误',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '132': {
        'code': 'water_pump_no',
        'name': '水泵序号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '133': {
        'code': 'high_pool_collect_device_address',
        'name': '高位水池采集设备地址',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '134': {
        'code': 'high_pool_collect_water_level_channel',
        'name': '高位水池采集水位通道',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '135': {
        'code': 'high_pool_upper_limit',
        'name': '高位水池上限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '136': {
        'code': 'high_pool_lower_limit',
        'name': '高位水池下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '137': {
        'code': 'high_pool_rise_speed',
        'name': '高位水池上升速度',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '138': {
        'code': 'low_pool_upper_limit',
        'name': '低位水池上限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '139': {
        'code': 'low_pool_lower_limit',
        'name': '低位水池下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '140': {
        'code': 'low_pool_rise_speed',
        'name': '低位水池上升速度',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '141': {
        'code': 'piping_pressure_upper_limit',
        'name': '管道压力上限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '142': {
        'code': 'piping_pressure_lower_limit',
        'name': '管道压力下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '143': {
        'code': 'water_pump_run_low_water_level',
        'name': '泵启动低位水位',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '144': {
        'code': 'high_data_update_timeout',
        'name': '高位数据更新超时',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '145': {
        'code': 'sequence_no',
        'name': '序号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '146': {
        'code': 'use_status',
        'name': '使用状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '147': {
        'code': 'alarm_type',
        'name': '报警类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '148': {
        'code': 'alarm_mode',
        'name': '报警方式',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '149': {
        'code': 'output_no',
        'name': '输出序号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '150': {
        'code': 'alarm_condition',
        'name': '报警条件',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '151': {
        'code': 'alarm_upper_limit',
        'name': '报警上限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '152': {
        'code': 'alarm_lower_limit',
        'name': '报警下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '153': {
        'code': 'water_meter_address_1',
        'name': '水表1地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '154': {
        'code': 'water_meter_address_2',
        'name': '水表2地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '155': {
        'code': 'water_meter_address_3',
        'name': '水表3地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '156': {
        'code': 'water_meter_address_4',
        'name': '水表4地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '157': {
        'code': 'water_meter_address_5',
        'name': '水表5地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '158': {
        'code': 'water_meter_address_6',
        'name': '水表6地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '159': {
        'code': 'water_meter_address_7',
        'name': '水表7地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '160': {
        'code': 'water_meter_address_8',
        'name': '水表8地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '161': {
        'code': 'water_meter_address_9',
        'name': '水表9地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '162': {
        'code': 'water_meter_address_10',
        'name': '水表10地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '163': {
        'code': 'water_meter_address_11',
        'name': '水表11地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '164': {
        'code': 'water_meter_address_12',
        'name': '水表12地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '165': {
        'code': 'water_meter_valve_1',
        'name': '水表1阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '166': {
        'code': 'water_meter_valve_2',
        'name': '水表2阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '167': {
        'code': 'water_meter_valve_3',
        'name': '水表3阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '168': {
        'code': 'water_meter_valve_4',
        'name': '水表4阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '169': {
        'code': 'water_meter_valve_5',
        'name': '水表5阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '170': {
        'code': 'water_meter_valve_6',
        'name': '水表6阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '171': {
        'code': 'water_meter_valve_7',
        'name': '水表7阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '172': {
        'code': 'water_meter_valve_8',
        'name': '水表8阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '173': {
        'code': 'water_meter_valve_9',
        'name': '水表9阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '174': {
        'code': 'water_meter_valve_10',
        'name': '水表10阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '175': {
        'code': 'water_meter_valve_11',
        'name': '水表11阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '176': {
        'code': 'water_meter_valve_12',
        'name': '水表12阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '177': {
        'code': 'water_meter_valve_13',
        'name': '水表13阀门控制',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '178': {
        'code': 'id',
        'name': '升级程序ID',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '179': {
        'code': 'size',
        'name': '升级程序分包大小',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '180': {
        'code': 'count',
        'name': '升级程序分包数量',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '181': {
        'code': 'current_index',
        'name': '升级程序当前包序号',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '182': {
        'code': 'current_size',
        'name': '升级程序当前包大小',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '183': {
        'code': 'data',
        'name': '升级程序数据',
        'type': 'element',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '184': {
        'code': 'user_count',
        'name': '黑名单数量',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '185': {
        'code': 'user_card_number',
        'name': '黑名单用户卡号',
        'type': 'element',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '186': {
        'code': 'set_type',
        'name': '黑名单设置类型',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '187': {
        'code': 'user_card_number',
        'name': '黑名单用户卡号',
        'type': 'element',
        'length': 16,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '188': {
        'code': 'threshold_value',
        'name': '报警阈值',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '189': {
        'code': 'water_electric',
        'name': '水电比',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex_normal', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '190': {
        'code': 'area_number',
        'name': 'ESAM区域号',
        'type': 'element',
        'length': 14,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '191': {
        'code': 'user_card_number',
        'name': '用户卡号',
        'type': 'element',
        'length': 16,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '192': {
        'code': 'recharge_money',
        'name': '用户充值金额',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '193': {
        'code': 'reserve',
        'name': '保留',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '194': {
        'code': 'tripping_operation',
        'name': '跳闸操作',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '195': {
        'code': 'channel_16',
        'name': '通道16',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '196': {
        'code': 'device_type',
        'name': '设备类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '197': {
        'code': 'account_balance',
        'name': '账户余额(m³)',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_10', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '198': {
        'code': 'recharge_money',
        'name': '充值金额(m³)',
        'type': 'element',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '199': {
        'code': 'recharge_money',
        'name': '充值金额(m³)',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_10', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '200': {
        'code': 'liquidometer_probe_height',
        'name': '液位计探头高度',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex_normal', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '201': {
        'code': 'report_cycle',
        'name': '上报周期',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '202': {
        'code': 'report_level',
        'name': '上报级别',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '203': {
        'code': 'output_type',
        'name': '输出类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '204': {
        'code': 'output_keep_time',
        'name': '输出保持时间',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '205': {
        'code': 'channel_is_open',
        'name': '通道是否对外开放',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '206': {
        'code': 'status_feedback_input_channel',
        'name': '状态反馈的输入通道',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '207': {
        'code': 'actuator_power_supply_mode',
        'name': '执行器供电方式',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '208': {
        'code': 'connect_device_index_no',
        'name': '连接设备的索引号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '209': {
        'code': 'status_feedback_time_lapse_trigger_time',
        'name': '状态反馈延时触发时间',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '210': {
        'code': 'fw_address',
        'name': '转发地址',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'address_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '211': {
        'code': 'fw_time',
        'name': '转发时间',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'get_current_time', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '212': {
        'code': 'fw_channel',
        'name': '转发通道',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '213': {
        'code': 'fw_data',
        'name': '转发数据',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '214': {
        'code': 'set_value',
        'name': '设定值',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_hex_normal', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '215': {
        'code': 'device_id',
        'name': '设备地址',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_device_address', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'device_address_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '216': {
        'code': 'register_state_1',
        'name': '寄存器状态1',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '217': {
        'code': 'register_state_2',
        'name': '寄存器状态2',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '218': {
        'code': 'register_state_3',
        'name': '寄存器状态3',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '219': {
        'code': 'write_register_address',
        'name': '写寄存器地址',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['srg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '220': {
        'code': 'write_register_value',
        'name': '写寄存器值',
        'type': 'element',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['srg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '221': {
        'code': 'upgrade_result',
        'name': '升级结果',
        'type': 'element',
        'length': 10,
        'de_plug': [
            {'return': [], 'code': 'check_upgrade_result', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '222': {
        'code': 'channel_16',
        'name': '通道16',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '223': {
        'code': 'channel_17',
        'name': '通道17',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '224': {
        'code': 'channel_18',
        'name': '通道18',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '225': {
        'code': 'channel_19',
        'name': '通道19',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '226': {
        'code': 'channel_20',
        'name': '通道20',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '227': {
        'code': 'channel_21',
        'name': '通道21',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '228': {
        'code': 'channel_22',
        'name': '通道22',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '229': {
        'code': 'channel_23',
        'name': '通道23',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '230': {
        'code': 'channel_24',
        'name': '通道24',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '231': {
        'code': 'channel_25',
        'name': '通道25',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '232': {
        'code': 'channel_26',
        'name': '通道26',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '233': {
        'code': 'channel_27',
        'name': '通道27',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '234': {
        'code': 'channel_28',
        'name': '通道28',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '235': {
        'code': 'channel_29',
        'name': '通道29',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '236': {
        'code': 'channel_30',
        'name': '通道30',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '237': {
        'code': 'channel_31',
        'name': '通道31',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '238': {
        'code': 'channel_32',
        'name': '通道32',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '239': {
        'code': 'channel_33',
        'name': '通道33',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '240': {
        'code': 'channel_34',
        'name': '通道34',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '241': {
        'code': 'channel_35',
        'name': '通道35',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '242': {
        'code': 'channel_36',
        'name': '通道36',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '243': {
        'code': 'channel_37',
        'name': '通道37',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '244': {
        'code': 'channel_38',
        'name': '通道38',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '245': {
        'code': 'channel_39',
        'name': '通道39',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '246': {
        'code': 'channel_40',
        'name': '通道40',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '247': {
        'code': 'channel_41',
        'name': '通道41',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '248': {
        'code': 'channel_42',
        'name': '通道42',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '249': {
        'code': 'channel_43',
        'name': '通道43',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '250': {
        'code': 'channel_44',
        'name': '通道44',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '251': {
        'code': 'channel_45',
        'name': '通道45',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '252': {
        'code': 'channel_46',
        'name': '通道46',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '253': {
        'code': 'channel_47',
        'name': '通道47',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '254': {
        'code': 'channel_48',
        'name': '通道48',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '255': {
        'code': 'channel_49',
        'name': '通道49',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '256': {
        'code': 'debug_data',
        'name': '调试数据',
        'type': 'element',
        'length': 200,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'zfill_0', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '257': {
        'code': 'result',
        'name': '结果',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '258': {
        'code': 'channel_50',
        'name': '通道50',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '259': {
        'code': 'channel_51',
        'name': '通道51',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '260': {
        'code': 'channel_52',
        'name': '通道52',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '261': {
        'code': 'channel_53',
        'name': '通道53',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '262': {
        'code': 'channel_54',
        'name': '通道54',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '263': {
        'code': 'channel_55',
        'name': '通道55',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '264': {
        'code': 'channel_56',
        'name': '通道56',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '265': {
        'code': 'channel_57',
        'name': '通道57',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '266': {
        'code': 'channel_58',
        'name': '通道58',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '267': {
        'code': 'channel_59',
        'name': '通道59',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '268': {
        'code': 'channel_60',
        'name': '通道60',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '269': {
        'code': 'channel_61',
        'name': '通道61',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '270': {
        'code': 'channel_62',
        'name': '通道62',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '271': {
        'code': 'channel_63',
        'name': '通道63',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '272': {
        'code': 'channel_64',
        'name': '通道64',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '273': {
        'code': 'channel_65',
        'name': '通道65',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '274': {
        'code': 'channel_66',
        'name': '通道66',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '275': {
        'code': 'channel_67',
        'name': '通道67',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '276': {
        'code': 'channel_68',
        'name': '通道68',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '277': {
        'code': 'channel_69',
        'name': '通道69',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '278': {
        'code': 'channel_70',
        'name': '通道70',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '279': {
        'code': 'channel_71',
        'name': '通道71',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '280': {
        'code': 'channel_72',
        'name': '通道72',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '281': {
        'code': 'channel_73',
        'name': '通道73',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '282': {
        'code': 'channel_74',
        'name': '通道74',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '283': {
        'code': 'channel_75',
        'name': '通道75',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '284': {
        'code': 'channel_76',
        'name': '通道76',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '285': {
        'code': 'channel_77',
        'name': '通道77',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '286': {
        'code': 'channel_78',
        'name': '通道78',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '287': {
        'code': 'channel_79',
        'name': '通道79',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '288': {
        'code': 'water_meter_address',
        'name': '水表地址',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_dechide', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'dechide_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '289': {
        'code': 'secret_type',
        'name': '加密类型',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '01': {
        'name': '控制（关泵开阀）应答',
        'type': '应答',
        'default': [],
        'element': ['040'],
        'type_dict': {}
    },
    '1D': {
        'name': '召测高低位水池控制参数应答',
        'type': '应答',
        'default': [],
        'element': ['102', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142',
                    '143', '144'],
        'type_dict': {}
    },
    '28': {
        'name': '召测卷帘控制信息应答',
        'type': '应答',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '30': {
        'name': '召测通道参数应答',
        'type': '应答',
        'default': [],
        'element': ['113', '040', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125',
                    '126', '127', '128', '129'],
        'type_dict': {}
    },
    '39': {
        'name': '远程升级应答',
        'type': '应答',
        'default': [],
        'element': ['221'],
        'type_dict': {}
    },
    '3A': {
        'name': '数据转发应答',
        'type': '应答',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '40': {
        'name': '召测DO参数应答',
        'type': '应答',
        'default': [],
        'element': ['102', '040', '114', '203', '204', '205', '206', '207', '208', '209'],
        'type_dict': {}
    },
    '41': {
        'name': '设备登陆上行',
        'type': '上行',
        'default': [],
        'element': ['001', '002', '003', '004'],
        'type_dict': {}
    },
    '42': {
        'name': '警情上报上行',
        'type': '上行',
        'default': ['037', '038', '039'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '通道数据值报警上行',
                'element': ['040', '041', '042', '043', '044'],
            },
            '02': {
                'name': '开关量报警上行',
                'element': ['040', '041'],
            },
            '03': {
                'name': '运行报警上行',
                'element': ['041', '045', '046'],
            },
            '04': {
                'name': '供电报警上行',
                'element': ['041', '047'],
            },
            '05': {
                'name': '控制输出报警上行',
                'element': ['041', '048'],
            },
            '06': {
                'name': '外部事件报警上行',
                'element': ['041', '049', '050'],
            },
        }
    },
    '43': {
        'name': '设备心跳上行',
        'type': '上行',
        'default': ['005', '006'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '链路心跳上行',
                'element': [],
            },
            '02': {
                'name': '状态心跳上行',
                'element': ['007', '008', '009', '010', '011', '012', '013', '014', '015'],
            },
        }
    },
    '44': {
        'name': '事件上报上行',
        'type': '上行',
        'default': ['051', '052', '053'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '控制计量事件上行',
                'element': ['054', '055', '056', '057', '058', '059', '060', '061', '062', '063', '064'],
            },
            '02': {
                'name': '卷帘控制事件上行',
                'element': ['065', '066', '067', '068', '069', '070'],
            },
            '04': {
                'name': '充值事件上行',
                'element': ['055', '191', '058', '059', '060', '061', '192', '062', '063'],
            },
        }
    },
    '46': {
        'name': '数据上报上行',
        'type': '上行',
        'default': [],
        'element': ['016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029',
                    '030', '031', '032',
                    '033', '034', '035', '036', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231',
                    '232', '233', '234',
                    '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248',
                    '249', '250', '251',
                    '252', '253', '254', '255', '258', '259', '260', '261', '262', '263', '264', '265', '266', '267',
                    '268', '269', '270',
                    '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283', '284',
                    '285', '286', '287'],
        'type_dict': {}
    },
    '48': {
        'name': '召测报警参数应答',
        'type': '应答',
        'default': [],
        'element': ['102', '145', '146', '147', '103', '148', '149', '150', '151', '152'],
        'type_dict': {}
    },
    '4A': {
        'name': '召测服务器参数应答',
        'type': '应答',
        'default': [],
        'element': ['102', '107', '108', '109', '110', '111', '112'],
        'type_dict': {}
    },
    '56': {
        'name': '低功耗上报周期读取应答',
        'type': '应答',
        'default': [],
        'element': ['201', '202'],
        'type_dict': {}
    },
    '57': {
        'name': '液位计探头高度读取应答',
        'type': '应答',
        'default': [],
        'element': ['200'],
        'type_dict': {}
    },
    '58': {
        'name': '余额读取应答',
        'type': '应答',
        'default': [],
        'element': ['197', '199'],
        'type_dict': {}
    },
    '5A': {
        'name': '用户卡黑名单读取应答',
        'type': '应答',
        'default': [],
        'element': ['184', '185'],
        'type_dict': {}
    },
    '5B': {
        'name': '余额报警阈值读取应答',
        'type': '应答',
        'default': [],
        'element': ['188'],
        'type_dict': {}
    },
    '5C': {
        'name': '水电比读取应答',
        'type': '应答',
        'default': [],
        'element': ['189'],
        'type_dict': {}
    },
    '5D': {
        'name': 'ESAM区域号读取应答',
        'type': '应答',
        'default': [],
        'element': ['190'],
        'type_dict': {}
    },
    '5E': {
        'name': '无流量数据自动跳闸读取应答',
        'type': '应答',
        'default': [],
        'element': ['194'],
        'type_dict': {}
    },
    '5F': {
        'name': '水表类型读取应答',
        'type': '应答',
        'default': [],
        'element': ['196'],
        'type_dict': {}
    },
    '6A': {
        'name': '召测T188水表地址应答',
        'type': '应答',
        'default': [],
        'element': ['153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164'],
        'type_dict': {}
    },
    '70': {
        'name': '恢复出厂设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    '81': {
        'name': '控制（开泵关阀）应答',
        'type': '应答',
        'default': [],
        'element': ['040'],
        'type_dict': {}
    },
    '9D': {
        'name': '设置高低位水池控制参数应答',
        'type': '应答',
        'default': [],
        'element': ['104'],
        'type_dict': {}
    },
    'A0': {
        'name': '设置寄存器应答',
        'type': '应答',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    'A1': {
        'name': '读取寄存器应答',
        'type': '应答',
        'default': [],
        'element': ['216', '217', '218'],
        'type_dict': {}
    },
    'B0': {
        'name': '设置通道参数应答',
        'type': '应答',
        'default': [],
        'element': ['113', '040', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125',
                    '126', '127', '128', '129'],
        'type_dict': {}
    },
    'C0': {
        'name': '设置DO参数应答',
        'type': '应答',
        'default': [],
        'element': ['102', '040', '114', '203', '204', '205', '206', '207', '208', '209'],
        'type_dict': {}
    },
    'C8': {
        'name': '设置报警参数应答',
        'type': '应答',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    'CA': {
        'name': '设置服务器参数应答',
        'type': '应答',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    'D1': {
        'name': '设置T188水表地址应答',
        'type': '应答',
        'default': [],
        'element': ['153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164'],
        'type_dict': {}
    },
    'D3': {
        'name': 'T188水表单阀控制应答',
        'type': '应答',
        'default': [],
        'element': ['105', '106'],
        'type_dict': {}
    },
    'D4': {
        'name': '设备ID设置应答',
        'type': '应答',
        'default': [],
        'element': ['215'],
        'type_dict': {}
    },
    'E9': {
        'name': '召测联户抄表应答',
        'type': '应答',
        'default': [],
        'element': ['102', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177'],
        'type_dict': {}
    },
    'EA': {
        'name': '用户卡黑名单设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'EB': {
        'name': '余额报警阈值设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'EC': {
        'name': '水电比设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'ED': {
        'name': 'ESAM区域号设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'EE': {
        'name': '无流量数据自动跳闸设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'EF': {
        'name': '水表类型设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'F1': {
        'name': '余额设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'F2': {
        'name': '液位计探头高度设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'F3': {
        'name': '低功耗上报周期设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    'F4': {
        'name': '阀门开度设置应答',
        'type': '应答',
        'default': [],
        'element': ['100', '193'],
        'type_dict': {}
    },
    'F9': {
        'name': '设置联户抄表应答',
        'type': '应答',
        'default': [],
        'element': ['102', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177'],
        'type_dict': {}
    },
    'D5': {
        'name': '设备调试应答',
        'type': '应答',
        'default': [],
        'element': ['257', '256'],
        'type_dict': {}
    },
    'D6': {
        'name': '数据加密设置应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '01': {
        'name': '控制（关泵开阀）上行',
        'type': '上行',
        'default': [],
        'element': ['040'],
        'type_dict': {}
    },
    '1D': {
        'name': '召测高低位水池控制参数上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '28': {
        'name': '召测卷帘控制信息上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '30': {
        'name': '召测通道参数上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '39': {
        'name': '远程升级上行',
        'type': '上行',
        'default': [],
        'element': ['178', '179', '180', '181', '182', '183'],
        'type_dict': {}
    },
    '3A': {
        'name': '数据转发上行',
        'type': '上行',
        'default': [],
        'element': ['210', '211', '212', '213'],
        'type_dict': {}
    },
    '40': {
        'name': '召测DO参数上行',
        'type': '上行',
        'default': [],
        'element': ['193'],
        'type_dict': {}
    },
    '41': {
        'name': '设备登陆应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    '42': {
        'name': '警情上报应答',
        'type': '应答',
        'default': ['100'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '通道数据值报警应答',
                'element': []
            },
            '02': {
                'name': '开关量报警应答',
                'element': []
            },
            '03': {
                'name': '运行报警应答',
                'element': []
            },
            '04': {
                'name': '供电报警应答',
                'element': []
            },
            '05': {
                'name': '控制输出报警应答',
                'element': []
            },
            '06': {
                'name': '外部事件报警应答',
                'element': []
            },
        }
    },
    '43': {
        'name': '设备心跳应答',
        'type': '应答',
        'default': ['005', '006'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '链路心跳应答',
                'element': []
            },
            '02': {
                'name': '状态心跳应答',
                'element': ['101']
            },
        }
    },
    '44': {
        'name': '事件上报应答',
        'type': '应答',
        'default': ['100', '052'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '控制计量事件应答',
                'element': []
            },
            '02': {
                'name': '卷帘控制事件应答',
                'element': []
            },
            '04': {
                'name': '充值事件应答',
                'element': []
            },
        }
    },
    '46': {
        'name': '数据上报应答',
        'type': '应答',
        'default': [],
        'element': ['100'],
        'type_dict': {}
    },
    '48': {
        'name': '召测报警参数上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '4A': {
        'name': '召测服务器参数上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '56': {
        'name': '低功耗上报周期读取上行',
        'type': '上行',
        'default': [],
        'element': ['193'],
        'type_dict': {}
    },
    '57': {
        'name': '液位计探头高度读取上行',
        'type': '上行',
        'default': [],
        'element': ['193'],
        'type_dict': {}
    },
    '58': {
        'name': '余额读取上行',
        'type': '上行',
        'default': [],
        'element': ['193'],
        'type_dict': {}
    },
    '5A': {
        'name': '用户卡黑名单读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '5B': {
        'name': '余额报警阈值读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '5C': {
        'name': '水电比读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '5D': {
        'name': 'ESAM区域号读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '5E': {
        'name': '无流量数据自动跳闸读取上行',
        'type': '上行',
        'default': [],
        'element': ['193'],
        'type_dict': {}
    },
    '5F': {
        'name': '水表类型读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '6A': {
        'name': '召测T188水表地址上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '70': {
        'name': '恢复出厂设置上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    '81': {
        'name': '控制（开泵关阀）上行',
        'type': '上行',
        'default': [],
        'element': ['040'],
        'type_dict': {}
    },
    '9D': {
        'name': '设置高低位水池控制参数上行',
        'type': '上行',
        'default': [],
        'element': ['102', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142',
                    '143', '144'],
        'type_dict': {}
    },
    'A0': {
        'name': '设置寄存器上行',
        'type': '上行',
        'default': [],
        'element': ['219', '220'],
        'type_dict': {}
    },
    'A1': {
        'name': '读取寄存器上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    'B0': {
        'name': '设置通道参数上行',
        'type': '上行',
        'default': [],
        'element': ['113', '040', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125',
                    '126', '127', '128', '129'],
        'type_dict': {}
    },
    'C0': {
        'name': '设置DO参数上行',
        'type': '上行',
        'default': [],
        'element': ['102', '040', '114', '203', '204', '205', '206', '207', '208', '209'],
        'type_dict': {}
    },
    'C8': {
        'name': '设置报警参数上行',
        'type': '上行',
        'default': [],
        'element': ['102', '145', '146', '147', '103', '148', '149', '150', '151', '152'],
        'type_dict': {}
    },
    'CA': {
        'name': '设置服务器参数上行',
        'type': '上行',
        'default': [],
        'element': ['102', '107', '108', '109', '110', '111', '112'],
        'type_dict': {}
    },
    'D1': {
        'name': '设置T188水表地址上行',
        'type': '上行',
        'default': [],
        'element': ['153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164'],
        'type_dict': {}
    },
    'D3': {
        'name': 'T188水表单阀控制上行',
        'type': '上行',
        'default': [],
        'element': ['105', '106'],
        'type_dict': {}
    },
    'D4': {
        'name': '设备ID设置',
        'type': '上行',
        'default': [],
        'element': ['215'],
        'type_dict': {}
    },
    'E9': {
        'name': '召测联户抄表上行',
        'type': '上行',
        'default': [],
        'element': ['102'],
        'type_dict': {}
    },
    'EA': {
        'name': '用户卡黑名单设置上行',
        'type': '上行',
        'default': [],
        'element': ['186', '187'],
        'type_dict': {}
    },
    'EB': {
        'name': '余额报警阈值设置上行',
        'type': '上行',
        'default': [],
        'element': ['188'],
        'type_dict': {}
    },
    'EC': {
        'name': '水电比设置上行',
        'type': '上行',
        'default': [],
        'element': ['189'],
        'type_dict': {}
    },
    'ED': {
        'name': 'ESAM区域号设置上行',
        'type': '上行',
        'default': [],
        'element': ['190'],
        'type_dict': {}
    },
    'EE': {
        'name': '无流量数据自动跳闸设置上行',
        'type': '上行',
        'default': [],
        'element': ['194'],
        'type_dict': {}
    },
    'EF': {
        'name': '水表类型设置上行',
        'type': '上行',
        'default': [],
        'element': ['196'],
        'type_dict': {}
    },
    'F1': {
        'name': '余额设置上行',
        'type': '上行',
        'default': [],
        'element': ['199'],
        'type_dict': {}
    },
    'F2': {
        'name': '液位计探头高度设置上行',
        'type': '上行',
        'default': [],
        'element': ['200'],
        'type_dict': {}
    },
    'F3': {
        'name': '低功耗上报周期设置上行',
        'type': '上行',
        'default': [],
        'element': ['201', '202'],
        'type_dict': {}
    },
    'F4': {
        'name': '阀门开度设置上行',
        'type': '上行',
        'default': [],
        'element': ['214', '193'],
        'type_dict': {}
    },
    'F9': {
        'name': '设置联户抄表上行',
        'type': '上行',
        'default': [],
        'element': ['102', '165', '166', '167', '168', '169', '170', '171', '172', '173', '174', '175', '176', '177'],
        'type_dict': {}
    },
    'D5': {
        'name': '设备调试上行',
        'type': '上行',
        'default': [],
        'element': ['256'],
        'type_dict': {}
    },
    'D6': {
        'name': '数据加密设置上行',
        'type': '上行',
        'default': [],
        'element': ['289'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['41', '42_01', '42_02', '42_03', '42_04', '42_05', '42_06', '43_02', '44_01', '44_02', '44_04', '46',
                'A1']

# 配置的CLASS
__CLASS__ = 'NBSettingInfo'


class NBSettingInfo(object):
    """
    获取NB协议配置信息
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
            if not self.__device_2_platform[command]['type_dict']:
                # 具体的解析协议由帧代号决定
                return [self.__element_dict[item] for item in self.__device_2_platform[command]['element']]
            else:
                # 具体的解析协议由帧代号、数据段类型所决定
                protocol_dict = {
                    'default': [self.__element_dict[item] for item in self.__device_2_platform[command]['default']],
                    'type_dict': {}
                }
                for type_key, type_value in self.__device_2_platform[command]['type_dict'].items():
                    protocol_dict['type_dict'][type_key] = [self.__element_dict[item] for item in type_value['element']]

                return protocol_dict
        else:
            return []

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
            if not self.__platform_2_device[command]['type_dict']:
                # 具体的解析协议由帧代号、功能码决定
                return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
            else:
                # 具体的解析协议由帧代号、功能码、数据段类型所决定
                protocol_dict = {
                    'default': [self.__element_dict[item] for item in self.__platform_2_device[command]['default']],
                    'type_dict': {}
                }
                for type_key, type_value in self.__platform_2_device[command]['type_dict'].items():
                    protocol_dict['type_dict'][type_key] = [self.__element_dict[item] for item in type_value['element']]

                return protocol_dict
        else:
            return []


if __name__ == '__main__':
    # import operator
    #
    # for item in sorted(DEVICE_2_PLATFORM.items(), key=operator.itemgetter(0), reverse=False):
    #     print(item[0])
    #
    # a = ['1-1', '2-1', '15-2', '16-7', '11-1', '11-3', '11-2']
    # print(sorted(a, key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1]))))
    setting_info = NBSettingInfo()
    ret = setting_info.get_platform_2_device_protocol_dict('48')
    print(ret)
    ret = setting_info.get_device_2_platform_protocol_dict('48')
    print(ret)
