# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/01/07

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    'PW': {
        'code': 'pw',
        'name': '密码',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'make_pw', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    'TP': {
        'code': 'tp',
        'name': '时间标签',
        'length': 10,
        'de_plug': [
            {'code': 'tp_time', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'make_tp', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'link_state',
        'name': '链路状态',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'terminal_address',
        'name': '终端地址',
        'length': 10,
        'de_plug': [
            {'code': 'to_address', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'make_address', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'terminal_clock',
        'name': '终端时钟',
        'length': 12,
        'de_plug': [
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']},
        ],
        'en_plug': [
            {'code': 'make_terminal_clock', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'work_mode',
        'name': '工作模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [{'code': 'make_work_mode', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'data_type',
        'name': '数据种类',
        'length': 4,
        'de_plug': [{'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'rainfall_cycle',
        'name': '雨量周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'water_level_cycle',
        'name': '水位周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'flow_cycle',
        'name': '流量（水量）周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_bcd', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'flow_speed_cycle',
        'name': '流速周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'gate_site_cycle',
        'name': '闸位周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'power_cycle',
        'name': '功率周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'air_pressure_cycle',
        'name': '气压周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'wind_speed_cycle',
        'name': '风速（风向）周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'water_temperature_cycle',
        'name': '水温周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'water_quality_cycle',
        'name': '水质周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'soil_water_rate_cycle',
        'name': '土壤含水率周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'evaporation_capacity_cycle',
        'name': '蒸发量周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'water_pressure_cycle',
        'name': '水压周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_bcd', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'alarm_or_state_cycle',
        'name': '报警或状态周期',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'fill_zero', 'params': [], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'upper_lower_limit_of_water_pressure',
        'name': '水压上下限',
        'length': None,
        'de_plug': [{'code': 'bcd_int_8', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_bcd_8', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'terminal_alarm',
        'name': '终端报警',
        'length': 4,
        'de_plug': [{'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'flow_upper_limit_val',
        'name': '流量参数上下限值',
        'length': None,
        'de_plug': [{'code': 'bcd_int_10', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_bcd_10', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'terminal_status',
        'name': '终端状态',
        'length': 4,
        'de_plug': [{'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'rainfall',
        'name': '雨量参数实时值',
        'length': 6,
        'de_plug': [{'code': 'bcd_int_3', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'water_level',
        'name': '水位参数实时值',
        'length': None,
        'de_plug': [{'code': 'bcd_int_4_3', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'flow',
        'name': '流量(水量)参数实时值',  # 累计流量
        'length': None,
        'de_plug': [{'code': 'bcd_flow', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'flow_rate',
        'name': '流速参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'gate_position',
        'name': '闸位参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'power',
        'name': '功率参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'air_pressure',
        'name': '气压参数实时值',
        'length': 6,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'wind_speed',
        'name': '风速参数实时值',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'water_temperature',
        'name': '水温参数实时值',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'water_quality',
        'name': '水质参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'soil_moisture',
        'name': '土壤含水率参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'evaporation',
        'name': '蒸发量参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': 'water_pressure',
        'name': '水压参数实时值',
        'length': None,
        'de_plug': [{'code': 'bcd_int_4_2', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'comprehensive',
        'name': '综合参数实时值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'input_voltage',
        'name': '输入电压实时值',
        'length': 4,
        'de_plug': [{'code': 'bcd_int_2', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'threshold_param_category',
        'name': '启报阈值参数类别',
        'length': 1,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'set_param_number',
        'name': '被设置参数编号',
        'length': 1,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'solid_state_storage_time_interval',
        'name': '固态存储时间间隔',
        'length': 2,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'start_threshold',
        'name': '启报阈值',
        'length': None,
        'de_plug': [
            {'code': 'bcd_int_5', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'bcd_int_4_2', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'int_bcd_5', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'int_bcd_4_2', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': 'param_code',
        'name': '参数编码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0044': {
        'code': 'start_time',
        'name': '开始时间',
        'length': 8,
        'de_plug': [{'code': 'bcd_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'time_bcd', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': 'end_time',
        'name': '结束时间',
        'length': 8,
        'de_plug': [{'code': 'bcd_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'time_bcd', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': 'ERC1',
        'name': '数据初始化记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': 'ERC2',
        'name': '参数变更记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': 'ERC3',
        'name': '状态量变位记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': 'ERC4',
        'name': '仪表故障记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0050': {
        'code': 'ERC5',
        'name': '密码错误记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': 'ERC6',
        'name': '终端故障记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': 'ERC7',
        'name': '交流失电记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': 'ERC8',
        'name': '蓄电池电压低告警记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0054': {
        'code': 'ERC9',
        'name': '终端箱非法打开记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0055': {
        'code': 'ERC10',
        'name': '水泵故障记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0056': {
        'code': 'ERC11',
        'name': '剩余水量超越告警记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0057': {
        'code': 'ERC12',
        'name': '水位超限告警记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0058': {
        'code': 'ERC13',
        'name': '水压超限告警记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0059': {
        'code': 'ERC14',
        'name': '水质参数超限告警记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0060': {
        'code': 'ERC15',
        'name': '数据错误记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0061': {
        'code': 'ERC16',
        'name': '发报文记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0062': {
        'code': 'ERC17',
        'name': '收报文记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0063': {
        'code': 'ERC18',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0064': {
        'code': 'ERC19',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0065': {
        'code': 'ERC20',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0066': {
        'code': 'ERC21',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0067': {
        'code': 'ERC22',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0068': {
        'code': 'ERC23',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0069': {
        'code': 'ERC24',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0070': {
        'code': 'ERC25',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0071': {
        'code': 'ERC26',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0072': {
        'code': 'ERC27',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0073': {
        'code': 'ERC28',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0074': {
        'code': 'ERC29',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0075': {
        'code': 'ERC30',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0076': {
        'code': 'ERC31',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0077': {
        'code': 'ERC32',
        'name': '发报文出错记录',
        'length': 4,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0078': {
        'code': 'choice_type',
        'name': '选择类型',
        'length': 1,
        'de_plug': [{'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'bin_hex', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0079': {
        'code': 'numbering',
        'name': '水泵或阀门/闸门编号',
        'length': 1,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_hex', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0080': {
        'code': 'response_result',
        'name': '响应结果',
        'length': 1,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0081': {
        'code': 'reset_type',
        'name': '复位类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0082': {
        'code': 'verify_results',
        'name': '确认结果',
        'length': 2,
        'de_plug': [],
        'en_plug': [{'code': 'make_work_mode', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0083': {
        'code': 'clear_data',
        'name': '清空数据',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0084': {
        'code': 'pw_data',
        'name': '密码数据',
        'length': 4,
        'de_plug': [{'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0085': {
        'code': 'flow_overrun',
        'name': '流量超限',
        'length': None,
        'de_plug': [{'code': 'bcd_int_5', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0086': {
        'code': 'water_pressure_overrun',
        'name': '水压超限',
        'length': None,
        'de_plug': [{'code': 'bcd_int_4_2', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0087': {
        'code': 'open_type',
        'name': '开关类型',
        'length': 2,
        'de_plug': [{'code': 'hex_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0088': {
        'code': 'total_flow',
        'name': '累计流量',
        'length': 10,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0089': {
        'code': 'water_user_no',
        'name': '用水户号',
        'length': 10,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0090': {
        'code': 'water_user_balance',
        'name': '用水户余额',
        'length': 8,
        'de_plug': [{'code': 'bcd_int_4_2', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0091': {
        'code': 'use_water_start_time',
        'name': '用水户用水开始时间',
        'length': 12,
        'de_plug': [{'code': 'bcd_datatime', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0092': {
        'code': 'use_water_end_time',
        'name': '用水户用水结束时间',
        'length': 12,
        'de_plug': [{'code': 'bcd_datatime', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0093': {
        'code': 'water_consumption_this_time',
        'name': '用水户本次用水量',
        'length': 10,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0094': {
        'code': 'amount_consumption',
        'name': '用水户本次消费金额',
        'length': 8,
        'de_plug': [{'code': 'bcd_int_4_2', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0095': {
        'code': 'use_time',
        'name': '用水户本次用水时间',
        'length': 8,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0096': {
        'code': 'record_cuount',
        'name': '记录数量',
        'length': 4,
        'de_plug': [{'code': 'bcd_int', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [{'code': 'int_bcd', 'params': ['msg_data'], 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '0097': {
        'code': 'flow_fix_data',
        'name': '流量固态存储数据',
        'length': None,
        'de_plug': [{'code': 'bcd_flow_fix_data', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0098': {
        'code': 'water_pressure',
        'name': '水压固态存储数据',
        'length': None,
        'de_plug': [{'code': 'bcd_int_4_2', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '02': {
        'name': '链路检测',
        'type': '上行',
        'default': ['0001'],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': '设置遥测终端地址',
        'type': '响应',
        'default': ['0002', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '50': {
        'name': '查询遥测终端地址',
        'type': '响应',
        'default': ['0002'],
        'element': [],
        'type_dict': {}
    },
    '11': {
        'name': '设置遥测终端时钟',
        'type': '响应',
        'default': ['0003', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '51': {
        'name': '查询遥测终端时钟',
        'type': '响应',
        'default': ['0003'],
        'element': [],
        'type_dict': {}
    },
    '12': {
        'name': '设置遥测终端工作模式',
        'type': '响应',
        'default': ['0004', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '52': {
        'name': '查询遥测终端工作模式',
        'type': '响应',
        'default': ['0004'],
        'element': [],
        'type_dict': {}
    },
    'A1': {
        'name': '设置遥测终端的数据自报种类及时间间隔',
        'type': '响应',
        'default': ['0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016',
                    '0017', '0018', '0019', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '53': {
        'name': '查询遥测终端的数据自报种类及时间间隔',
        'type': '响应',
        'default': ['0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016',
                    '0017', '0018', '0019'],
        'element': [],
        'type_dict': {}
    },
    '18': {
        'name': '设置遥测终端水压上、下限值',
        'type': '响应',
        'default': ['0020', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '58': {
        'name': '查询遥测终端水压上下限值',
        'type': '响应',
        'default': ['0020', '0021'],
        'element': [],
        'type_dict': {}
    },
    '1F': {
        'name': '设置遥测终端的流量参数上限值',
        'type': '响应',
        'default': ['0022', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '64': {
        'name': '查询遥测终端流量参数上限值',
        'type': '响应',
        'default': ['0022', '0021'],
        'element': [],
        'type_dict': {}
    },
    'B0': {
        'name': '查询遥测终端实时值',
        'type': '响应',
        'default': [],
        'element': [],
        'type_dict': {
            '3': {
                'name': '查询流量(水量)参数',
                'element': ['0026', '0021', '0023']
            },
            'F': {
                'name': '查询水压参数',
                'element': ['0036', '0021', '0023']
            }
        }
    },
    '20': {
        'name': '设置遥测终端检测参数启报阈值及固态存储时间段间隔',
        'type': '响应',
        'default': ['0039', '0040', '0041', '0042', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    'B1': {
        'name': '查询终端固态存储数据',
        'type': '响应',
        'default': [],
        'element': [],
        'type_dict': {
            '3': {
                'name': '流量(水量)',
                'element': ['0043', '0044', '0045', '0097'],
            },
            'F': {
                'name': '水压',
                'element': ['0043', '0044', '0045', '0098'],
            },
        }
    },
    '5D': {
        'name': '查询遥测终端的事件记录',
        'type': '响应',
        'default': ['0046', '0047', '0048', '0049', '0050', '0051', '0052', '0053', '0054', '0055', '0056', '0057',
                    '0058', '0059', '0060', '0061', '0062', '0063', '0064', '0065', '0066', '0067', '0068', '0069',
                    '0070', '0071', '0072', '0073', '0074', '0075', '0076', '0077'],
        'element': [],
        'type_dict': {}
    },
    '5E': {
        'name': '查询遥测终端状态和报警状态',
        'type': '响应',
        'default': ['0021', '0023'],
        'element': [],
        'type_dict': {}
    },
    '92': {
        'name': '遥控启动水泵或阀门/闸门',
        'type': '响应',
        'default': ['0080', '0079'],
        'element': [],
        'type_dict': {}
    },
    '93': {
        'name': '遥控关闭水泵或阀门/闸门',
        'type': '响应',
        'default': ['0080', '0079'],
        'element': [],
        'type_dict': {}
    },
    '90': {
        'name': '复位遥测终端参数和状态',
        'type': '响应',
        'default': ['0082'],
        'element': [],
        'type_dict': {}
    },
    '91': {
        'name': '清空遥测终端的历史数据单元',
        'type': '响应',
        'default': ['0083'],
        'element': [],
        'type_dict': {}
    },
    '96': {
        'name': '修改遥测终端密码',
        'type': '响应',
        'default': ['0084'],
        'element': [],
        'type_dict': {}
    },
    'C0': {
        'name': '自报实时数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '3': {
                'name': '流量(水量)实时数据',
                'element': ['0026', '0021', '0023', 'TP'],
            },
            'F': {
                'name': '水压实时数据',
                'element': ['0036', '0021', '0023', 'TP'],
            },
        }
    },
    '81': {
        'name': '随机自报报警数据',
        'type': '上行',
        'default': ['0021'],
        'element': [],
        'type_dict': {
            '3': {
                'name': '流量(水量)超限报警',
                'element': ['0085', '0023', 'TP'],
            },
            'F': {
                'name': '水压超限报警',
                'element': ['0086', '0023', 'TP'],
            },
        }
    },
    '83': {
        'name': '遥测终端开关泵自报',
        'type': '上行',
        'default': ['0005', '0087', '0088', '0089', '0090', '0091', '0092', '0093', '0094', '0095', 'TP'],
        'element': [],
        'type_dict': {}
    },
    'B3': {
        'name': '查询开关泵记录',
        'type': '响应',
        'default': ['0096', '0005', '0087', '0088', '0089', '0090', '0091', '0092', '0093', '0094', '0095'],
        'element': [],
        'type_dict': {}
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '02': {
        'name': '链路检测',
        'type': '响应',
        'default': ['0001'],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': '设置遥测终端地址',
        'type': '上行',
        'default': ['0002', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '50': {
        'name': '查询遥测终端地址',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '11': {
        'name': '设置遥测终端时钟',
        'type': '上行',
        'default': ['0003', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '51': {
        'name': '查询遥测终端时钟',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '12': {
        'name': '设置遥测终端工作模式',
        'type': '上行',
        'default': ['0004', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '52': {
        'name': '查询遥测终端工作模式',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'A1': {
        'name': '设置遥测终端的数据自报种类及时间间隔',
        'type': '上行',
        'default': ['0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016',
                    '0017', '0018', '0019', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '53': {
        'name': '查询遥测终端的数据自报种类及时间间隔',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '18': {
        'name': '设置遥测终端水压上、下限值',
        'type': '上行',
        'default': ['0020', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '58': {
        'name': '查询遥测终端水压上下限值',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '1F': {
        'name': '设置遥测终端的流量参数上限值',
        'type': '上行',
        'default': ['0022', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '64': {
        'name': '查询遥测终端流量参数上限值',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'B0': {
        'name': '查询遥测终端实时值',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '3': {
                'name': '查询流量(水量)参数',
                'element': []
            },
            'F': {
                'name': '查询水压参数',
                'element': []
            }
        }
    },
    '20': {
        'name': '设置遥测终端检测参数启报阈值及固态存储时间段间隔',
        'type': '上行',
        'default': ['0039', '0040', '0041', '0042', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    'B1': {
        'name': '查询终端固态存储数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            '3': {
                'name': '流量(水量)',
                'element': ['0043', '0044', '0045'],
            },
            'F': {
                'name': '水压',
                'element': ['0043', '0044', '0045'],
            },
        }
    },
    '5D': {
        'name': '查询遥测终端的事件记录',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '5E': {
        'name': '查询遥测终端状态和报警状态',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '92': {
        'name': '遥控启动水泵或阀门/闸门',
        'type': '上行',
        'default': ['0079', '0078', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '93': {
        'name': '遥控关闭水泵或阀门/闸门',
        'type': '上行',
        'default': ['0079', '0078', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '90': {
        'name': '复位遥测终端参数和状态',
        'type': '上行',
        'default': ['0081', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '91': {
        'name': '清空遥测终端的历史数据单元',
        'type': '上行',
        'default': ['0083', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    '96': {
        'name': '修改遥测终端密码',
        'type': '上行',
        'default': ['0084', 'PW', 'TP'],
        'element': [],
        'type_dict': {}
    },
    'C0': {
        'name': '自报实时数据',
        'type': '响应',
        'default': [],
        'element': [],
        'type_dict': {
            '3': {
                'name': '流量(水量)实时数据',
                'element': ['0082'],
            },
            'F': {
                'name': '水压实时数据',
                'element': ['0082'],
            },
        }
    },
    '81': {
        'name': '随机自报报警数据',
        'type': '响应',
        'default': ['0082'],
        'element': [],
        'type_dict': {}
    },
    '83': {
        'name': '遥测终端开关泵自报',
        'type': '响应',
        'default': ['0082'],
        'element': [],
        'type_dict': {}
    },
    'B3': {
        'name': '查询开关泵记录',
        'type': '上行',
        'default': ['0096', 'TP'],
        'element': [],
        'type_dict': {}
    },
}

# 入库的命令列表
IS_SAVE_LIST = ['C0_3', 'C0_F', '81_3', '81_F', '83']

# 配置的CLASS
__CLASS__ = 'WaterResourceSettingInfo'


class WaterResourceSettingInfo(object):
    """
    水资源协议配置信息
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
        获取平台发出报文的协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
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
    setting_info = WaterResourceSettingInfo()
    []
    dict_info = setting_info.get_device_2_platform_protocol_dict('83')
    for item in dict_info['default']:
        print('| ' + item['code'] + ' | ' + item['name'] + ' | ')
    for item in dict_info['type_dict']:
        print('| ' + item['code'] + ' | ' + item['name'] + ' | ')
