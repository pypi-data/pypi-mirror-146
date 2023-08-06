# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/12/12

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'byte_count',
        'name': '字节个数',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'write_data_info',
        'name': '写数据内容',
        'length': None,
        'de_plug': [],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'write_data_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'start_address',
        'name': '起始地址',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'register_count',
        'name': '寄存器数量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0000': {
        'code': '1_gate_board_control',
        'name': '1#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': '1_gate_board_set_value',
        'name': '1#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': '2_gate_board_control',
        'name': '2#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': '2_gate_board_set_value',
        'name': '2#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': '3_gate_board_control',
        'name': '3#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': '3_gate_board_set_value',
        'name': '3#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': '4_gate_board_control',
        'name': '4#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': '4_gate_board_set_value',
        'name': '4#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': '5_gate_board_control',
        'name': '5#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': '5_gate_board_set_value',
        'name': '5#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '000A': {
        'code': '6_gate_board_control',
        'name': '6#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '000B': {
        'code': '6_gate_board_set_value',
        'name': '6#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '000C': {
        'code': '7_gate_board_control',
        'name': '7#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '000D': {
        'code': '7_gate_board_set_value',
        'name': '7#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '000E': {
        'code': '8_gate_board_control',
        'name': '8#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '000F': {
        'code': '8_gate_board_set_value',
        'name': '8#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': '9_gate_board_control',
        'name': '9#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': '9_gate_board_set_value',
        'name': '9#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': '10_gate_board_control',
        'name': '10#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': '10_gate_board_set_value',
        'name': '10#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': '11_gate_board_control',
        'name': '11#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': '11_gate_board_set_value',
        'name': '11#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': '12_gate_board_control',
        'name': '12#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': '12_gate_board_set_value',
        'name': '12#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': '13_gate_board_control',
        'name': '13#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': '13_gate_board_set_value',
        'name': '13#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '001A': {
        'code': '14_gate_board_control',
        'name': '14#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '001B': {
        'code': '14_gate_board_set_value',
        'name': '14#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '001C': {
        'code': '15_gate_board_control',
        'name': '15#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '001D': {
        'code': '15_gate_board_set_value',
        'name': '15#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '001E': {
        'code': '16_gate_board_control',
        'name': '16#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '001F': {
        'code': '16_gate_board_set_value',
        'name': '16#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': '17_gate_board_control',
        'name': '17#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': '17_gate_board_set_value',
        'name': '17#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': '18_gate_board_control',
        'name': '18#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': '18_gate_board_set_value',
        'name': '18#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': '19_gate_board_control',
        'name': '19#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': '19_gate_board_set_value',
        'name': '19#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': '20_gate_board_control',
        'name': '20#闸板控制字',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': '20_gate_board_set_value',
        'name': '20#闸板设定值',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [
            {'params': ['msg_data'], 'code': 'int_hex', 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'gate_board_count',
        'name': '闸板数量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'upper_water_level',
        'name': '闸前水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': '1_gate_board_lower_water_level',
        'name': '1#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': '1_gate_board_open_value',
        'name': '1#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': '1_gate_board_instantaneous_flow',
        'name': '1#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': '1_gate_board_total_flow',
        'name': '1#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': '1_gate_board_state',
        'name': '1#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003A': {
        'code': '1_gate_board_alarm',
        'name': '1#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003B': {
        'code': '1_gate_board_weight',
        'name': '1#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003C': {
        'code': '1_gate_board_voltage',
        'name': '1#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003D': {
        'code': '1_gate_board_current',
        'name': '1#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': '2_gate_board_lower_water_level',
        'name': '2#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': '2_gate_board_open_value',
        'name': '2#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': '2_gate_board_instantaneous_flow',
        'name': '2#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': '2_gate_board_total_flow',
        'name': '2#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': '2_gate_board_state',
        'name': '2#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': '2_gate_board_alarm',
        'name': '2#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': '2_gate_board_weight',
        'name': '2#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': '2_gate_board_voltage',
        'name': '2#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': '2_gate_board_current',
        'name': '2#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004C': {
        'code': '3_gate_board_lower_water_level',
        'name': '3#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004D': {
        'code': '3_gate_board_open_value',
        'name': '3#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004E': {
        'code': '3_gate_board_instantaneous_flow',
        'name': '3#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004F': {
        'code': '3_gate_board_total_flow',
        'name': '3#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': '3_gate_board_state',
        'name': '3#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': '3_gate_board_alarm',
        'name': '3#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': '3_gate_board_weight',
        'name': '3#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0054': {
        'code': '3_gate_board_voltage',
        'name': '3#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0055': {
        'code': '3_gate_board_current',
        'name': '3#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0058': {
        'code': '4_gate_board_lower_water_level',
        'name': '4#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0059': {
        'code': '4_gate_board_open_value',
        'name': '4#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005A': {
        'code': '4_gate_board_instantaneous_flow',
        'name': '4#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005B': {
        'code': '4_gate_board_total_flow',
        'name': '4#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005D': {
        'code': '4_gate_board_state',
        'name': '4#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005E': {
        'code': '4_gate_board_alarm',
        'name': '4#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005F': {
        'code': '4_gate_board_weight',
        'name': '4#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0060': {
        'code': '4_gate_board_voltage',
        'name': '4#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0061': {
        'code': '4_gate_board_current',
        'name': '4#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0064': {
        'code': '5_gate_board_lower_water_level',
        'name': '5#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0065': {
        'code': '5_gate_board_open_value',
        'name': '5#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0066': {
        'code': '5_gate_board_instantaneous_flow',
        'name': '5#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0067': {
        'code': '5_gate_board_total_flow',
        'name': '5#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0069': {
        'code': '5_gate_board_state',
        'name': '5#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006A': {
        'code': '5_gate_board_alarm',
        'name': '5#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006B': {
        'code': '5_gate_board_weight',
        'name': '5#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006C': {
        'code': '5_gate_board_voltage',
        'name': '5#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006D': {
        'code': '5_gate_board_current',
        'name': '5#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0070': {
        'code': '6_gate_board_lower_water_level',
        'name': '6#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0071': {
        'code': '6_gate_board_open_value',
        'name': '6#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0072': {
        'code': '6_gate_board_instantaneous_flow',
        'name': '6#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0073': {
        'code': '6_gate_board_total_flow',
        'name': '6#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0075': {
        'code': '6_gate_board_state',
        'name': '6#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0076': {
        'code': '6_gate_board_alarm',
        'name': '6#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0077': {
        'code': '6_gate_board_weight',
        'name': '6#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0078': {
        'code': '6_gate_board_voltage',
        'name': '6#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0079': {
        'code': '6_gate_board_current',
        'name': '6#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007C': {
        'code': '7_gate_board_lower_water_level',
        'name': '7#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007D': {
        'code': '7_gate_board_open_value',
        'name': '7#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007E': {
        'code': '7_gate_board_instantaneous_flow',
        'name': '7#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007F': {
        'code': '7_gate_board_total_flow',
        'name': '7#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0081': {
        'code': '7_gate_board_state',
        'name': '7#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0082': {
        'code': '7_gate_board_alarm',
        'name': '7#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0083': {
        'code': '7_gate_board_weight',
        'name': '7#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0084': {
        'code': '7_gate_board_voltage',
        'name': '7#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0085': {
        'code': '7_gate_board_current',
        'name': '7#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0088': {
        'code': '8_gate_board_lower_water_level',
        'name': '8#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0089': {
        'code': '8_gate_board_open_value',
        'name': '8#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008A': {
        'code': '8_gate_board_instantaneous_flow',
        'name': '8#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008B': {
        'code': '8_gate_board_total_flow',
        'name': '8#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008D': {
        'code': '8_gate_board_state',
        'name': '8#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008E': {
        'code': '8_gate_board_alarm',
        'name': '8#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008F': {
        'code': '8_gate_board_weight',
        'name': '8#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0090': {
        'code': '8_gate_board_voltage',
        'name': '8#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0091': {
        'code': '8_gate_board_current',
        'name': '8#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0094': {
        'code': '9_gate_board_lower_water_level',
        'name': '9#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0095': {
        'code': '9_gate_board_open_value',
        'name': '9#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0096': {
        'code': '9_gate_board_instantaneous_flow',
        'name': '9#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0097': {
        'code': '9_gate_board_total_flow',
        'name': '9#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0099': {
        'code': '9_gate_board_state',
        'name': '9#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009A': {
        'code': '9_gate_board_alarm',
        'name': '9#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009B': {
        'code': '9_gate_board_weight',
        'name': '9#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009C': {
        'code': '9_gate_board_voltage',
        'name': '9#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009D': {
        'code': '9_gate_board_current',
        'name': '9#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A0': {
        'code': '10_gate_board_lower_water_level',
        'name': '10#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A1': {
        'code': '10_gate_board_open_value',
        'name': '10#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A2': {
        'code': '10_gate_board_instantaneous_flow',
        'name': '10#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A3': {
        'code': '10_gate_board_total_flow',
        'name': '10#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A5': {
        'code': '10_gate_board_state',
        'name': '10#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A6': {
        'code': '10_gate_board_alarm',
        'name': '10#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A7': {
        'code': '10_gate_board_weight',
        'name': '10#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A8': {
        'code': '10_gate_board_voltage',
        'name': '10#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00A9': {
        'code': '10_gate_board_current',
        'name': '10#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00AC': {
        'code': '11_gate_board_lower_water_level',
        'name': '11#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00AD': {
        'code': '11_gate_board_open_value',
        'name': '11#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00AE': {
        'code': '11_gate_board_instantaneous_flow',
        'name': '11#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00AF': {
        'code': '11_gate_board_total_flow',
        'name': '11#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B1': {
        'code': '11_gate_board_state',
        'name': '11#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B2': {
        'code': '11_gate_board_alarm',
        'name': '11#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B3': {
        'code': '11_gate_board_weight',
        'name': '11#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B4': {
        'code': '11_gate_board_voltage',
        'name': '11#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B5': {
        'code': '11_gate_board_current',
        'name': '11#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B8': {
        'code': '12_gate_board_lower_water_level',
        'name': '12#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00B9': {
        'code': '12_gate_board_open_value',
        'name': '12#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00BA': {
        'code': '12_gate_board_instantaneous_flow',
        'name': '12#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00BB': {
        'code': '12_gate_board_total_flow',
        'name': '12#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00BD': {
        'code': '12_gate_board_state',
        'name': '12#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00BE': {
        'code': '12_gate_board_alarm',
        'name': '12#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00BF': {
        'code': '12_gate_board_weight',
        'name': '12#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C0': {
        'code': '12_gate_board_voltage',
        'name': '12#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C1': {
        'code': '12_gate_board_current',
        'name': '12#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C4': {
        'code': '13_gate_board_lower_water_level',
        'name': '13#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C5': {
        'code': '13_gate_board_open_value',
        'name': '13#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C6': {
        'code': '13_gate_board_instantaneous_flow',
        'name': '13#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C7': {
        'code': '13_gate_board_total_flow',
        'name': '13#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00C9': {
        'code': '13_gate_board_state',
        'name': '13#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00CA': {
        'code': '13_gate_board_alarm',
        'name': '13#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00CB': {
        'code': '13_gate_board_weight',
        'name': '13#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00CC': {
        'code': '13_gate_board_voltage',
        'name': '13#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00CD': {
        'code': '13_gate_board_current',
        'name': '13#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D0': {
        'code': '14_gate_board_lower_water_level',
        'name': '14#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D1': {
        'code': '14_gate_board_open_value',
        'name': '14#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D2': {
        'code': '14_gate_board_instantaneous_flow',
        'name': '14#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D3': {
        'code': '14_gate_board_total_flow',
        'name': '14#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D5': {
        'code': '14_gate_board_state',
        'name': '14#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D6': {
        'code': '14_gate_board_alarm',
        'name': '14#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D7': {
        'code': '14_gate_board_weight',
        'name': '14#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D8': {
        'code': '14_gate_board_voltage',
        'name': '14#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00D9': {
        'code': '14_gate_board_current',
        'name': '14#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00DC': {
        'code': '15_gate_board_lower_water_level',
        'name': '15#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00DD': {
        'code': '15_gate_board_open_value',
        'name': '15#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00DE': {
        'code': '15_gate_board_instantaneous_flow',
        'name': '15#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00DF': {
        'code': '15_gate_board_total_flow',
        'name': '15#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E1': {
        'code': '15_gate_board_state',
        'name': '15#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E2': {
        'code': '15_gate_board_alarm',
        'name': '15#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E3': {
        'code': '15_gate_board_weight',
        'name': '15#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E4': {
        'code': '15_gate_board_voltage',
        'name': '15#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E5': {
        'code': '15_gate_board_current',
        'name': '15#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E8': {
        'code': '16_gate_board_lower_water_level',
        'name': '16#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00E9': {
        'code': '16_gate_board_open_value',
        'name': '16#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00EA': {
        'code': '16_gate_board_instantaneous_flow',
        'name': '16#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00EB': {
        'code': '16_gate_board_total_flow',
        'name': '16#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00ED': {
        'code': '16_gate_board_state',
        'name': '16#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00EE': {
        'code': '16_gate_board_alarm',
        'name': '16#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00EF': {
        'code': '16_gate_board_weight',
        'name': '16#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F0': {
        'code': '16_gate_board_voltage',
        'name': '16#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F1': {
        'code': '16_gate_board_current',
        'name': '16#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F4': {
        'code': '17_gate_board_lower_water_level',
        'name': '17#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F5': {
        'code': '17_gate_board_open_value',
        'name': '17#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F6': {
        'code': '17_gate_board_instantaneous_flow',
        'name': '17#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F7': {
        'code': '17_gate_board_total_flow',
        'name': '17#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00F9': {
        'code': '17_gate_board_state',
        'name': '17#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00FA': {
        'code': '17_gate_board_alarm',
        'name': '17#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00FB': {
        'code': '17_gate_board_weight',
        'name': '17#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00FC': {
        'code': '17_gate_board_voltage',
        'name': '17#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '00FD': {
        'code': '17_gate_board_current',
        'name': '17#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0100': {
        'code': '18_gate_board_lower_water_level',
        'name': '18#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0101': {
        'code': '18_gate_board_open_value',
        'name': '18#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0102': {
        'code': '18_gate_board_instantaneous_flow',
        'name': '18#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0103': {
        'code': '18_gate_board_total_flow',
        'name': '18#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0105': {
        'code': '18_gate_board_state',
        'name': '18#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0106': {
        'code': '18_gate_board_alarm',
        'name': '18#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0107': {
        'code': '18_gate_board_weight',
        'name': '18#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0108': {
        'code': '18_gate_board_voltage',
        'name': '18#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0109': {
        'code': '18_gate_board_current',
        'name': '18#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010C': {
        'code': '19_gate_board_lower_water_level',
        'name': '19#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010D': {
        'code': '19_gate_board_open_value',
        'name': '19#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010E': {
        'code': '19_gate_board_instantaneous_flow',
        'name': '19#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010F': {
        'code': '19_gate_board_total_flow',
        'name': '19#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0111': {
        'code': '19_gate_board_state',
        'name': '19#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0112': {
        'code': '19_gate_board_alarm',
        'name': '19#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0113': {
        'code': '19_gate_board_weight',
        'name': '19#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0114': {
        'code': '19_gate_board_voltage',
        'name': '19#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0115': {
        'code': '19_gate_board_current',
        'name': '19#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0118': {
        'code': '20_gate_board_lower_water_level',
        'name': '20#闸板闸后水位',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0119': {
        'code': '20_gate_board_open_value',
        'name': '20#闸板开度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011A': {
        'code': '20_gate_board_instantaneous_flow',
        'name': '20#闸板瞬时流量',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011B': {
        'code': '20_gate_board_total_flow',
        'name': '20#闸板累计流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011D': {
        'code': '20_gate_board_state',
        'name': '20#闸板状态',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011E': {
        'code': '20_gate_board_alarm',
        'name': '20#闸板报警',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_bin', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011F': {
        'code': '20_gate_board_weight',
        'name': '20#闸板荷重',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_to_plus_minus_int', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0120': {
        'code': '20_gate_board_voltage',
        'name': '20#闸板电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0121': {
        'code': '20_gate_board_current',
        'name': '20#闸板电流',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    '03': {
        'name': u'读寄存器响应',
        'type': '应答',
        'default': ['001'],
        'element': [
            '0032', '0033',
            '0034', '0035', '0036', '0037', '0039', '003A', '003B', '003C', '003D',
            '0040', '0041', '0042', '0043', '0045', '0046', '0047', '0048', '0049',
            '004C', '004D', '004E', '004F', '0051', '0052', '0053', '0054', '0055',
            '0058', '0059', '005A', '005B', '005D', '005E', '005F', '0060', '0061',
            '0064', '0065', '0066', '0067', '0069', '006A', '006B', '006C', '006D',
            '0070', '0071', '0072', '0073', '0075', '0076', '0077', '0078', '0079',
            '007C', '007D', '007E', '007F', '0081', '0082', '0083', '0084', '0085',
            '0088', '0089', '008A', '008B', '008D', '008E', '008F', '0090', '0091',
            '0094', '0095', '0096', '0097', '0099', '009A', '009B', '009C', '009D',
            '00A0', '00A1', '00A2', '00A3', '00A5', '00A6', '00A7', '00A8', '00A9',
            '00AC', '00AD', '00AE', '00AF', '00B1', '00B2', '00B3', '00B4', '00B5',
            '00B8', '00B9', '00BA', '00BB', '00BD', '00BE', '00BF', '00C0', '00C1',
            '00C4', '00C5', '00C6', '00C7', '00C9', '00CA', '00CB', '00CC', '00CD',
            '00D0', '00D1', '00D2', '00D3', '00D5', '00D6', '00D7', '00D8', '00D9',
            '00DC', '00DD', '00DE', '00DF', '00E1', '00E2', '00E3', '00E4', '00E5',
            '00E8', '00E9', '00EA', '00EB', '00ED', '00EE', '00EF', '00F0', '00F1',
            '00F4', '00F5', '00F6', '00F7', '00F9', '00FA', '00FB', '00FC', '00FD',
            '0100', '0101', '0102', '0103', '0105', '0106', '0107', '0108', '0109',
            '010C', '010D', '010E', '010F', '0111', '0112', '0113', '0114', '0115',
            '0118', '0119', '011A', '011B', '011D', '011E', '011F', '0120', '0121',
        ],
        'type_dict': {}
    },
    '10': {
        'name': u'写寄存器响应',
        'type': '应答',
        'default': ['003', '004'],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    '03': {
        'name': u'读寄存器上行',
        'type': '上行',
        'default': ['003', '004'],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': u'写寄存器上行',
        'type': '上行',
        'default': ['002'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['03']

# 配置的CLASS
__CLASS__ = 'PLCHNQGateInfo'


class PLCHNQGateInfo(object):
    """
    获取PLC惠农渠闸门配置信息
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
    print(sorted(ELEMENT_DICT.keys()))
