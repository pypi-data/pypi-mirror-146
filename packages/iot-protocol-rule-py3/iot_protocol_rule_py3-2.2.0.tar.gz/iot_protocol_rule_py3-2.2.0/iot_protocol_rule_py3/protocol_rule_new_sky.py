# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/07/05

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'serial_number',
        'name': '序列号',
        'length': 30,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'reserve',
        'name': '保留',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'software_version',
        'name': '软件版本',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'hardware_version',
        'name': '硬件版本',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'reset_number',
        'name': '复位次数',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'heartbeat_type',
        'name': '心跳类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']},
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'reserve',
        'name': '保留',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'connect_mode',
        'name': '连接方式',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'device_time',
        'name': '设备时间',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date', 'params': ['srg_data']},
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'report_cycle',
        'name': '上报周期',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'collect_cycle',
        'name': '采集周期',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'storage_cycle',
        'name': '存储周期',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'signal_strength',
        'name': '信号强度',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'save_data',
        'name': '存储数据',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'not_report_data',
        'name': '未报数据',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'device_energy',
        'name': '设备能量',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float_normal', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'package_count',
        'name': '数据包数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_report_data', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'collect_time',
        'name': '采集时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'channel_count',
        'name': '通道数量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'data_address',
        'name': '数据地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'save_info',
        'name': '存储信息',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'channel_0',
        'name': '通道0',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'channel_1',
        'name': '通道1',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'channel_2',
        'name': '通道2',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'channel_3',
        'name': '通道3',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'channel_4',
        'name': '通道4',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'channel_5',
        'name': '通道5',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'channel_6',
        'name': '通道6',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'channel_7',
        'name': '通道7',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'channel_8',
        'name': '通道8',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'channel_9',
        'name': '通道9',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'channel_10',
        'name': '通道10',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'channel_11',
        'name': '通道11',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'channel_12',
        'name': '通道12',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'channel_13',
        'name': '通道13',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'channel_14',
        'name': '通道14',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'channel_15',
        'name': '通道15',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'call_type',
        'name': '抄表类型',
        'length': 2,
        'de_plug': [{'return': [], 'code': 'get_type_key', 'params': []}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'syn_flg',
        'name': '同步标示',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'current_time',
        'name': '当前时间',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'current_time_hex', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'device_type',
        'name': '设备类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'device_count',
        'name': '设备数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_device_address', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '043': {
        'code': 'device_address',
        'name': '设备地址',
        'length': None,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'device_address_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'beacon_type',
        'name': '信标类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'beacon_type_hex', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'channel_no',
        'name': '通道号',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'control_device_count',
        'name': '控制设备数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_address_channel_no', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'channel_no',
        'name': '通道号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'call_device_count',
        'name': '召测设备数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_status_data', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '049': {
        'code': 'device_time',
        'name': '设备时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '050': {
        'code': 'device_data',
        'name': '设备数据',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '051': {
        'code': 'index_no',
        'name': '索引号',
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
    '052': {
        'code': 'center_no',
        'name': '中心序号',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '053': {
        'code': 'use_status',
        'name': '使用状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '054': {
        'code': 'address_type',
        'name': '地址类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '055': {
        'code': 'address_length',
        'name': '地址长度',
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
    '056': {
        'code': 'address_string',
        'name': '地址字符串',
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
    '057': {
        'code': 'port',
        'name': '端口号',
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
    '058': {
        'code': 'success_flag',
        'name': '成功标识',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'check_response', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '059': {
        'code': 'syn_flg',
        'name': '同步标示',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'check_equip_status', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '060': {
        'code': 'address_channel_no',
        'name': '设备地址+通道号',
        'length': None,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'address_channel_no_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '061': {
        'code': 'success_flag',
        'name': '成功标识',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '062': {
        'code': 'document_type',
        'name': '档案类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '063': {
        'code': 'document_count',
        'name': '档案数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_device_document', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '064': {
        'code': 'device_document',
        'name': '设备档案',
        'length': None,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'device_document_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '065': {
        'code': 'document_type',
        'name': '档案类型',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '066': {
        'code': 'app_type',
        'name': '应用类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '067': {
        'code': 'copy_channel',
        'name': '抄取信道',
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
    '068': {
        'code': 'upload_channel',
        'name': '上传信道',
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
    '069': {
        'code': 'reserve',
        'name': '保留',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '070': {
        'code': 'maintain_type',
        'name': '维护类型',
        'type': 'default',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '071': {
        'code': 'device_type',
        'name': '设备类型',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'get_type_key', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '072': {
        'code': 'pipe_network_pressure_upper_limit_value',
        'name': '管网压力上限值',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_100', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_100', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '073': {
        'code': 'pressure_standard_low_pressure_pressure_value',
        'name': '压力标定低压压力值',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_1000', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '074': {
        'code': 'pressure_standard_high_pressure_pressure_value',
        'name': '压力标定高压压力值',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_1000', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '075': {
        'code': 'pressure_standard_low_pressure_voltage_value',
        'name': '压力标定低压电压值',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_1000', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '076': {
        'code': 'pressure_standard_high_pressure_voltage_value',
        'name': '压力标定高压电压值',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_1000', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_1000', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '077': {
        'code': 'timed_upload_time_interval',
        'name': '定时上传时间间隔',
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
    '078': {
        'code': 'flow_sensor_transition_coefficient',
        'name': '流量传感器转换系数',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '079': {
        'code': 'temperature_parameter_1',
        'name': '温度参数1',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '080': {
        'code': 'temperature_parameter_2',
        'name': '温度参数2',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '081': {
        'code': 'humidity_parameter_1',
        'name': '湿度参数1',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '082': {
        'code': 'humidity_parameter_2',
        'name': '湿度参数2',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '083': {
        'code': 'server_ccid',
        'name': '服务器CCID',
        'length': 20,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '084': {
        'code': 'server_ip',
        'name': '服务器IP',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_server_ip', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'server_ip_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '085': {
        'code': 'server_port',
        'name': '服务器PORT',
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
    '086': {
        'code': 'server_apn',
        'name': '服务器APN',
        'length': None,
        'de_plug': [
            {'return': [], 'code': 'get_server_apn_length', 'params': []},
            {'return': ['srg_data'], 'code': 'hex_server_apn', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'server_apn_hex', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '087': {
        'code': 'report_time_interval',
        'name': '上报时间间隔',
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
    '088': {
        'code': 'valve_count',
        'name': '阀门数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '089': {
        'code': 'moisture_meter_count',
        'name': '墒情仪数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '090': {
        'code': 'gateway_time',
        'name': '网关时间',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_date', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '091': {
        'code': 'gateway_battery_voltage',
        'name': '网关电池电压',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '092': {
        'code': 'gateway_signal_strength',
        'name': '网关信号强度',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '093': {
        'code': 'gateway_program_version',
        'name': '网关程序版本号',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 平台至设备协议配置
DEVICE_2_PLATFORM = {
    '01': {
        'name': '单点控制关阀应答',
        'type': '应答',
        'default': [],
        'element': ['045'],
        'type_dict': {}
    },
    '03': {
        'name': '多点控制开阀应答',
        'type': '应答',
        'default': [],
        'element': ['046', '043', '047'],
        'type_dict': {}
    },
    '41': {
        'name': '设备登陆上行',
        'type': '上行',
        'default': [],
        'element': ['001', '002', '003', '004', '005'],
        'type_dict': {}
    },
    '43': {
        'name': '设备心跳上行',
        'type': '上行',
        'default': ['006'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '链路心跳上行',
                'element': ['007'],
            },
            '02': {
                'name': '状态心跳上行',
                'element': ['007', '008', '009', '010', '011', '012', '013', '014', '015', '016'],
            },
        }
    },
    '46': {
        'name': '数据上报上行',
        'type': '上行',
        'default': [],
        'element': ['007', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029',
                    '030', '031', '032', '033', '034', '035', '036', '037'],
        'type_dict': {}
    },
    '4A': {
        'name': '召测服务器参数应答',
        'type': '应答',
        'default': [],
        'element': ['051', '052', '053', '054', '055', '056', '057'],
        'type_dict': {}
    },
    '63': {
        'name': '召测网关下行设备状态应答',
        'type': '应答',
        'default': [],
        'element': ['048', '043', '049', '050'],
        'type_dict': {}
    },
    '7E': {
        'name': '多点抄表应答',
        'type': '应答',
        'default': [],
        'element': ['042', '043', '044', '007'],
        'type_dict': {}
    },
    '7F': {
        'name': '全网抄表应答',
        'type': '应答',
        'default': ['038'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '全网抄表同步时钟应答',
                'element': ['039', '040'],
            },
            '03': {
                'name': '全网抄表实时数据应答',
                'element': ['041'],
            },
        }
    },
    '81': {
        'name': '单点控制开阀应答',
        'type': '应答',
        'default': [],
        'element': ['045'],
        'type_dict': {}
    },
    '83': {
        'name': '多点控制关阀应答',
        'type': '应答',
        'default': [],
        'element': ['046', '043', '047'],
        'type_dict': {}
    },
    '8F': {
        'name': '设备档案维护应答',
        'type': '应答',
        'default': ['065'],
        'element': [],
        'type_dict': {
            '11': {
                'name': '下载档案应答',
                'element': [],
            },
            '22': {
                'name': '删除档案应答',
                'element': [],
            },
            '33': {
                'name': '读取档案应答',
                'element': ['041', '063', '064'],
            },
            '44': {
                'name': '格式化档案应答',
                'element': [],
            }
        }
    },
    'CA': {
        'name': '设置服务器参数应答',
        'type': '应答',
        'default': [],
        'element': ['058'],
        'type_dict': {}
    },
    'B6': {
        'name': '网关无线参数读取应答',
        'type': '应答',
        'default': [],
        'element': ['067', '068', '069'],
        'type_dict': {}
    },
    'B5': {
        'name': '网关无线参数设置应答',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '8E': {
        'name': '网关下行设备参数维护应答',
        'type': '应答',
        'default': ['070', '071'],
        'element': [],
        'type_dict': {
            '0B0A': {
                'name': '智能阀门设置参数应答',
                'element': [],
            },
            '0B07': {
                'name': '智能墒情仪设置参数应答',
                'element': [],
            },
            '0C0A': {
                'name': '智能阀门读取参数应答',
                'element': ['072', '073', '074', '075', '076', '077', '078'],
            },
            '0C07': {
                'name': '智能墒情仪读取参数应答',
                'element': ['079', '080', '081', '082'],
            },
            '0D0A': {
                'name': '智能阀门设置无线通讯参数应答',
                'element': [],
            },
            '0D07': {
                'name': '智能墒情仪设置无线通讯参数应答',
                'element': [],
            },
            '0E0A': {
                'name': '智能阀门读取无线通讯参数应答',
                'element': ['067', '068', '069'],
            },
            '0E07': {
                'name': '智能墒情仪读取无线通讯参数应答',
                'element': ['067', '068', '069'],
            },
        }
    },
    '33': {
        'name': '网关工作参数读取应答',
        'type': '应答',
        'default': [],
        'element': ['083', '084', '085', '086', '087', '088', '089', '090', '091', '092', '093'],
        'type_dict': {}
    },
    '31': {
        'name': '网关工作参数设置应答',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '62': {
        'name': '查询网关下行设备数据应答',
        'type': '应答',
        'default': [],
        'element': ['048', '043', '049', '050'],
        'type_dict': {}
    }
}

# 设备至平台协议配置
PLATFORM_2_DEVICE = {
    '01': {
        'name': '单点控制关阀上行',
        'type': '上行',
        'default': [],
        'element': ['045'],
        'type_dict': {}
    },
    '03': {
        'name': '多点控制开阀上行',
        'type': '上行',
        'default': [],
        'element': ['042', '060'],
        'type_dict': {}
    },
    '41': {
        'name': '设备登陆应答',
        'type': '应答',
        'default': [],
        'element': ['058'],
        'type_dict': {}
    },
    '43': {
        'name': '设备心跳应答',
        'type': '应答',
        'default': ['006'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '链路心跳应答',
                'element': ['007'],
            },
            '02': {
                'name': '状态心跳应答',
                'element': ['007', '059'],
            },
        }
    },
    '46': {
        'name': '数据上报应答',
        'type': '应答',
        'default': [],
        'element': ['058'],
        'type_dict': {}
    },
    '4A': {
        'name': '召测服务器参数上行',
        'type': '上行',
        'default': [],
        'element': ['051'],
        'type_dict': {}
    },
    '63': {
        'name': '召测网关下行设备状态上行',
        'type': '上行',
        'default': [],
        'element': ['048', '043'],
        'type_dict': {}
    },
    '7E': {
        'name': '多点抄表上行',
        'type': '上行',
        'default': [],
        'element': ['042', '043', '044', '007'],
        'type_dict': {}
    },
    '7F': {
        'name': '全网抄表上行',
        'type': '上行',
        'default': ['038'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '全网抄表同步时钟上行',
                'element': ['039', '040'],
            },
            '03': {
                'name': '全网抄表实时数据上行',
                'element': ['041'],
            },
        }
    },
    '81': {
        'name': '单点控制开阀上行',
        'type': '上行',
        'default': [],
        'element': ['045'],
        'type_dict': {}
    },
    '83': {
        'name': '多点控制关阀上行',
        'type': '上行',
        'default': [],
        'element': ['042', '060'],
        'type_dict': {}
    },
    '8F': {
        'name': '设备档案维护上行',
        'type': '上行',
        'default': ['065'],
        'element': [],
        'type_dict': {
            '11': {
                'name': '下载档案上行',
                'element': ['041', '063', '064'],
            },
            '22': {
                'name': '删除档案上行',
                'element': ['041', '063', '064'],
            },
            '33': {
                'name': '读取档案上行',
                'element': ['041'],
            },
            '44': {
                'name': '格式化档案上行',
                'element': ['041'],
            }
        }
    },
    'CA': {
        'name': '设置服务器参数上行',
        'type': '上行',
        'default': [],
        'element': ['051', '052', '053', '054', '055', '056', '057'],
        'type_dict': {}
    },
    'B6': {
        'name': '网关无线参数读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'B5': {
        'name': '网关无线参数设置上行',
        'type': '上行',
        'default': [],
        'element': ['067', '068', '069'],
        'type_dict': {}
    },
    '8E': {
        'name': '网关下行设备参数维护上行',
        'type': '上行',
        'default': ['070', '071'],
        'element': [],
        'type_dict': {
            '0B0A': {
                'name': '智能阀门设置参数上行',
                'element': ['072', '073', '074', '075', '076', '077', '078'],
            },
            '0B07': {
                'name': '智能墒情仪设置参数上行',
                'element': ['079', '080', '081', '082'],
            },
            '0C0A': {
                'name': '智能阀门读取参数上行',
                'element': [],
            },
            '0C07': {
                'name': '智能墒情仪读取参数上行',
                'element': [],
            },
            '0D0A': {
                'name': '智能阀门设置无线通讯参数上行',
                'element': ['067', '068', '069'],
            },
            '0D07': {
                'name': '智能墒情仪设置无线通讯参数上行',
                'element': ['067', '068', '069'],
            },
            '0E0A': {
                'name': '智能阀门读取无线通讯参数上行',
                'element': [],
            },
            '0E07': {
                'name': '智能墒情仪读取无线通讯参数上行',
                'element': [],
            },
        }
    },
    '33': {
        'name': '网关工作参数读取上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '31': {
        'name': '网关工作参数设置上行',
        'type': '上行',
        'default': [],
        'element': ['084', '085', '086', '087'],
        'type_dict': {}
    },
    '62': {
        'name': '查询网关下行设备数据上行',
        'type': '上行',
        'default': [],
        'element': ['048', '045', '043'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['41', '43_02', '46']

# 配置的CLASS
__CLASS__ = 'NewSkySettingInfo'


class NewSkySettingInfo(object):
    """
    获取NEWSKY协议配置信息
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
        :param protocol:
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
        :param protocol:
        :return:
        """
        if command in self.__platform_2_device.keys():
            if not self.__device_2_platform[command]['type_dict']:
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
    setting_info = NewSkySettingInfo()
    print(setting_info.get_platform_2_device_protocol_dict('01'))

    print(len(PLATFORM_2_DEVICE))
