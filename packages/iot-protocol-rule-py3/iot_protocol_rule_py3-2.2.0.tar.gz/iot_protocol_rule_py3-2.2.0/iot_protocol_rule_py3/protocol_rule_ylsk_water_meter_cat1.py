# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/02/04

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    'METER_TYPE': {
        'code': 'meter_type',
        'name': '表类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'METER_ADDRESS': {
        'code': 'meter_address',
        'name': '表地址',
        'length': 14,
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
    'DI': {
        'code': 'di',
        'name': '数据标识DI',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'SER': {
        'code': 'ser',
        'name': '序号SER',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'control_frame',
        'name': '控制帧',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'protocol_version',
        'name': '协议版本',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'software_version',
        'name': '软件版本',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'reset_number',
        'name': '复位次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'ccid',
        'name': 'CCID',
        'length': 20,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'imei',
        'name': 'IMEI',
        'length': 16,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'actual_time',
        'name': '实时时间',
        'length': 14,
        'de_plug': [
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'update_command', 'params': ['srg_data'], 'return': []}
        ],
        'en_plug': [
            {'code': 'syn_time', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'report_cycle',
        'name': '上报周期',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'msg_zfill', 'params': [], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'pay_mode',
        'name': '付费方式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'default_network_mode',
        'name': '默认网络模式',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'network_module_type',
        'name': '网络模块类型',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'boot_loader_software_version',
        'name': 'BootLoader软件版本',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'hardware_version_number',
        'name': '硬件版本',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'imsi',
        'name': 'IMSI',
        'length': 16,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'total_flow',
        'name': '累计流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'day_total_flow',
        'name': '日累计流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_10000', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'ST',
        'name': '状态ST',
        'length': 4,
        'de_plug': [
            {'code': 'hex_to_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'signal',
        'name': '信号',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'voltage',
        'name': '电压',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_1000', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'balance',
        'name': '余额',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'now_network_mode',
        'name': '当前网络模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'signal_strength',
        'name': '信号强度',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_plus_minus_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'snr',
        'name': '信噪比',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_plus_minus_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'nwt_work_cover_level',
        'name': '网络覆盖等级',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'base_station_community_id',
        'name': '基站小区ID',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'base_station_location_info_lac',
        'name': '基站位置信息LAC',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'equip_running_time',
        'name': '设备运行时间',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'send_successful_times',
        'name': '发送成功次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'send_failure_times',
        'name': '发送失败次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'open_valve_times',
        'name': '开阀次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'close_valve_times',
        'name': '关阀次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'signal_percentage',
        'name': '信号百分比',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'battery_percentage',
        'name': '电量百分比',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'hibernation_error',
        'name': '休眠错误',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': 'reserved_text',
        'name': '保留字段',
        'length': 16,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'data_time',
        'name': '数据时间',
        'length': 14,
        'de_plug': [
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'syn_time', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'open_valve_success_times',
        'name': '开阀成功次数',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'close_valve_success_times',
        'name': '关阀成功次数',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'valve_current_status',
        'name': '阀门当前状态',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'factory_test_results',
        'name': '工厂测试结果',
        'length': 8,
        'de_plug': [
            {'code': 'hex_to_bin', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'total_flow_hours',
        'name': '整点累计流量',
        'length': 240,
        'de_plug': [
            {'code': 'hex_int_24', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': 'start_time',
        'name': '起始时间',
        'length': 14,
        'de_plug': [
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'syn_time', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0044': {
        'code': 'end_time',
        'name': '结束时间',
        'length': 14,
        'de_plug': [
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': 'flow_threshold',
        'name': '流量阈值',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'set_flow_threshold', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': 'current_total_flow',
        'name': '当前累计流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': 'valve_open_close',
        'name': '阀开/关',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': 'active_write_card_flag',
        'name': '激活写卡标志',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': 'recharge_amount',
        'name': '充值金额',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0050': {
        'code': 'pay_mode',
        'name': '付费方式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': 'net_mode',
        'name': '网络模式',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': 'start_time_point',
        'name': '开始时间点',
        'length': 2,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': 'close_time_point',
        'name': '结束时间点',
        'length': 2,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0054': {
        'code': 'debug_mode_status',
        'name': '调试模式状态',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0055': {
        'code': 'long_conn_time',
        'name': '长连接时长',
        'length': 2,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0056': {
        'code': 'charge_type',
        'name': '计费类型',
        'length': 2,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0057': {
        'code': 'ladder_price_1',
        'name': '阶梯价格1',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0058': {
        'code': 'ladder_flow_1',
        'name': '阶梯流量1',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0059': {
        'code': 'ladder_price_2',
        'name': '阶梯价格2',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0060': {
        'code': 'ladder_flow_2',
        'name': '阶梯流量2',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0061': {
        'code': 'ladder_price_3',
        'name': '阶梯价格3',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0062': {
        'code': 'price',
        'name': '价格',
        'length': 8,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_first_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'float_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0063': {
        'code': 'reset_value',
        'name': '复位值',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0064': {
        'code': 'cleaning_state_execution',
        'name': '清洗状态执行',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0065': {
        'code': 'cleaning_state_cycle',
        'name': '清洗状态周期',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_hex', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0066': {
        'code': 'cleaning_day',
        'name': '清洗日',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0067': {
        'code': 'cleaning_hour',
        'name': '清洗时',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0068': {
        'code': 'cleaning_minte',
        'name': '清洗分',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0069': {
        'code': 'freeze_status',
        'name': '数据冻结上报状态',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0070': {
        'code': 'alarm_interval',
        'name': '报警间隔',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0071': {
        'code': 'unit_code',
        'name': '单位代码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0072': {
        'code': 'preset_total_flow',
        'name': '预设累计流量',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'code': 'preset_flow', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0073': {
        'code': '30_day_total_flow',
        'name': '历史数据',
        'length': 240,
        'de_plug': [
            {'code': 'total_flow_30_day', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0074': {
        'code': 'meter_manufacturer',
        'name': '水表厂商',
        'length': 0,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_meter_control_params', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0075': {
        'code': 'locked_voltage',
        'name': '堵转电压',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0076': {
        'code': 'control_duration',
        'name': '控制时长',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0077': {
        'code': 'overtime_duration',
        'name': '超时时长',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'to_bcd', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0078': {
        'code': 'encrypt_support',
        'name': '加密支持',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0079': {
        'code': 'ip',
        'name': 'IP',
        'length': 8,
        'de_plug': [
            {'code': 'hex_to_ip', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'ip_to_hex', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0080': {
        'code': 'port',
        'name': 'Port',
        'length': 4,
        'de_plug': [
            {'code': 'hex_to_port', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'port_to_hex', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    'B1': {
        'name': '主动上报',
        'type': '上行',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册',
                'element': ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014'],
            },
            '0008': {
                'name': '数据上报',
                'element': ['0001', '0002', '0015', '0016', '0017', '0007', '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025',
                            '0026', '0027'],
            },
            '0010': {
                'name': '调试上报',
                'element': ['0001', '0002', '0028', '0029', '0030', '0031', '0032', '0033', '0034', '0035', '0007', '0036'],
            },
            '0019': {
                'name': '长连接心跳',
                'element': ['0001', '0002'],
            },
            '0021': {
                'name': '数据补报',
                'element': ['0001', '0002', '0037', '0016'],
            },
            '0024': {
                'name': '清洗上报',
                'element': ['0001', '0002', '0038', '0039', '0040'],
            },
            '0025': {
                'name': '工厂测试时上报',
                'element': ['0001', '0002', '0041'],
            },
            '0027': {
                'name': '数据冻结上报',
                'element': ['0001', '0002', '0042'],
            }
        }
    },
    'B2': {
        'name': '告警上报',
        'type': '上行',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '磁干扰报警',
                'element': ['0007', '0018'],
            },
            '000D': {
                'name': '余额报警',
                'element': ['0007', '0021'],
            },
            '0028': {
                'name': '流量报警',
                'element': ['0043', '0044', '0045', '0046'],
            },
        }
    },
    'B5': {
        'name': '主动上报（加密）',
        'type': '上行',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册',
                'element': ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014'],
            },
            '0008': {
                'name': '数据上报',
                'element': ['0001', '0002', '0015', '0016', '0017', '0007', '0018', '0019', '0020', '0021', '0022', '0023', '0024', '0025',
                            '0026', '0027'],
            },
            '0010': {
                'name': '调试上报',
                'element': ['0001', '0002', '0028', '0029', '0030', '0031', '0032', '0033', '0034', '0035', '0007', '0036'],
            },
            '0019': {
                'name': '长连接心跳',
                'element': ['0001', '0002'],
            },
            '0021': {
                'name': '数据补报',
                'element': ['0001', '0002', '0037', '0016'],
            },
            '0024': {
                'name': '清洗上报',
                'element': ['0001', '0002', '0038', '0039', '0040'],
            },
            '0025': {
                'name': '工厂测试时上报',
                'element': ['0001', '0002', '0041'],
            },
            '0027': {
                'name': '数据冻结上报',
                'element': ['0001', '0002', '0042'],
            }
        }
    },
    'A5': {
        'name': '阀门控制',
        'type': '响应',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            'A017': {
                'name': '闸门控制',
                'element': ['0018'],
            },
        }
    },
    '84': {
        'name': '写数据',
        'type': '响应',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '设置上报周期',
                'element': [],
            },
            '000A': {
                'name': '设置服务器信息',
                'element': [],
            },
            '000B': {
                'name': '激活写卡状态',
                'element': [],
            },
            '000C': {
                'name': '充值',
                'element': [],
            },
            '000E': {
                'name': '设置付费方式',
                'element': [],
            },
            '000F': {
                'name': '设置网络模式',
                'element': [],
            },
            '0011': {
                'name': '设置上报时间点',
                'element': [],
            },
            '0012': {
                'name': '设置调试模式状态',
                'element': [],
            },
            '0013': {
                'name': '设置长连接',
                'element': [],
            },
            '0022': {
                'name': '设置重启',
                'element': [],
            },
            '0023': {
                'name': '设置清洗时间',
                'element': [],
            },
            '0026': {
                'name': '设置数据冻结状态',
                'element': [],
            },
            '0029': {
                'name': '设置流量阈值',
                'element': [],
            },
            '002B': {
                'name': '设置水表控制参数',
                'element': [],
            },
            '0018': {
                'name': '加密配置',
                'element': [],
            }
        }
    },
    '96': {
        'name': '设置水表底数',
        'type': '响应',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            'A016': {
                'name': '设置水表底数',
                'element': ['0018'],
            },
        }
    },
    '81': {
        'name': '召测数据',
        'type': '响应',
        'default': ['METER_TYPE', 'METER_ADDRESS', 'CONTROL_CODE', 'DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '上报周期',
                'element': ['0008'],
            },
            '000E': {
                'name': '付费方式',
                'element': ['0009'],
            },
            '000F': {
                'name': '网络模式',
                'element': ['0051'],
            },
            '0011': {
                'name': '上报时间点',
                'element': ['0052', '0053'],
            },
            '0014': {
                'name': '阶梯水价',
                'element': ['0056', '0057', '0058', '0059', '0060', '0061', '0062'],
            },
            '0023': {
                'name': '清洗时间',
                'element': ['0064', '0065', '0066', '0067', '0068'],
            },
            '0026': {
                'name': '数据冻结状态',
                'element': ['0069'],
            },
            '0029': {
                'name': '流量阈值',
                'element': ['0070', '0045'],
            },
            '002A': {
                'name': '历史数据',
                'element': ['0073']
            },
            '002B': {
                'name': '水表控制参数',
                'element': ['0075', '0076', '0077']
            }
        }
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '31': {
        'name': '主动上报',
        'type': '响应',
        'default': [],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册',
                'element': ['0001', '0007'],
            },
            '0008': {
                'name': '数据上报',
                'element': ['0001', '0007'],
            },
            '0010': {
                'name': '长连接心跳',
                'element': ['0001', '0007'],
            },
            '0019': {
                'name': '长连接心跳',
                'element': ['0001', '0007'],
            },
            '0021': {
                'name': '数据补报',
                'element': ['0001', '0007'],
            },
            '0024': {
                'name': '清洗上报',
                'element': ['0001', '0007'],
            },
            '0025': {
                'name': '工厂测试时上报',
                'element': ['0001', '0007'],
            },
            '0027': {
                'name': '数据冻结上报',
                'element': ['0001', '0007'],
            }
        }
    },
    '32': {
        'name': '告警上报',
        'type': '响应',
        'default': [],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '磁干扰报警',
                'element': [],
            },
            '000D': {
                'name': '余额报警',
                'element': [],
            },
            '0028': {
                'name': '流量报警',
                'element': [],
            },
        }
    },
    '2A': {
        'name': '阀门控制',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            'A017': {
                'name': '闸门控制',
                'element': ['0047'],
            },
        }
    },
    '04': {
        'name': '写数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '设置上报周期',
                'element': ['0008'],
            },
            '000A': {
                'name': '设置服务器信息',
                'element': ['0079', '0080'],
            },
            '000B': {
                'name': '激活写卡状态',
                'element': ['0048'],
            },
            '000C': {
                'name': '充值',
                'element': ['0049'],
            },
            '000E': {
                'name': '设置付费方式',
                'element': ['0009'],
            },
            '000F': {
                'name': '设置网络模式',
                'element': ['0051'],
            },
            '0011': {
                'name': '设置上报时间点',
                'element': ['0052', '0053'],
            },
            '0012': {
                'name': '设置调试模式状态',
                'element': ['0054'],
            },
            '0013': {
                'name': '设置长连接',
                'element': ['0043', '0055'],
            },
            '0014': {
                'name': '设置阶梯水价',
                'element': ['0056', '0057', '0058', '0059', '0060', '0061', '0062'],
            },
            '0022': {
                'name': '设置重启',
                'element': ['0063'],
            },
            '0023': {
                'name': '设置清洗时间',
                'element': ['0064', '0065', '0066', '0067', '0068'],
            },
            '0026': {
                'name': '设置数据冻结状态',
                'element': ['0069'],
            },
            '0029': {
                'name': '设置流量阈值',
                'element': ['0070', '0045'],
            },
            '002B': {
                'name': '设置水表控制参数',
                'element': ['0074', '0075', '0076', '0077'],
            },
            '0018': {
                'name': '加密配置',
                'element': ['0078'],
            }
        }
    },
    '16': {
        'name': '设置水表底数',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            'A016': {
                'name': '设置水表底数',
                'element': ['0071', '0072'],
            },
        }
    },
    '01': {
        'name': '召测数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '注册信息',
                'element': [],
            },
            '0009': {
                'name': '上报周期',
                'element': [],
            },
            '000E': {
                'name': '付费方式',
                'element': [],
            },
            '000F': {
                'name': '网络模式',
                'element': [],
            },
            '0011': {
                'name': '上报时间点',
                'element': [],
            },
            '0014': {
                'name': '阶梯水价',
                'element': [],
            },
            '0023': {
                'name': '清洗时间',
                'element': [],
            },
            '0026': {
                'name': '数据冻结状态',
                'element': [],
            },
            '0029': {
                'name': '流量阈值',
                'element': [],
            },
            '002A': {
                'name': '历史数据',
                'element': []
            },
            '002B': {
                'name': '水表控制参数',
                'element': []
            }
        }
    },
}

# 入库的命令列表
IS_SAVE_LIST = ['A5_A017', 'B1_0007', 'B1_0008', 'B1_0010', 'B1_0019', 'B1_0021', 'B1_0024', 'B1_0025', 'B1_0027', 'B2_0006', 'B2_000D',
                'B2_0028']

# 配置的CLASS
__CLASS__ = 'YlskWaterMeterCat1SettingInfo'


class YlskWaterMeterCat1SettingInfo(object):
    """
    获取 优联时空水表配置信息
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

    def get_device_2_platform_protocol_dict(self, control_code, di):
        """
        获取设备至平台协议字典
        :param control_code:
        :param di:
        :return:
        """
        if control_code in self.__device_2_platform.keys():
            if di in self.__device_2_platform[control_code]['type_dict'].keys():
                return [self.__element_dict[item] for item in
                        self.__device_2_platform[control_code]['type_dict'][di]['element']]
            else:
                return []
        else:
            return []

    def get_platform_2_device_protocol_dict(self, control_code, di):
        """
        获取平台至设备协议字典
        :param control_code:
        :param di:
        :return:
        """
        if control_code in self.__platform_2_device.keys():
            if di in self.__platform_2_device[control_code]['type_dict'].keys():
                return [self.__element_dict[item] for item in
                        self.__platform_2_device[control_code]['type_dict'][di]['element']]
            else:
                return []
        else:
            return []


if __name__ == '__main__':
    pass
