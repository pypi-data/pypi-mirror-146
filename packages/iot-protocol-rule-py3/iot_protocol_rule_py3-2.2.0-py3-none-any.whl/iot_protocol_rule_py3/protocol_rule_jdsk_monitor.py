# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/05/18

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    '0000': {
        'code': 'report_permission',
        'name': '上报许可',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'make_report_permission', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0001': {
        'code': 'link_mode',
        'name': '链接方式',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'serial_number',
        'name': '序列号',
        'length': 32,
        'de_plug': [
            # {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'product_type',
        'name': '产品类型',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'software_model',
        'name': '软件型号',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'software_version',
        'name': '软件版本',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'hardware_model',
        'name': '硬件型号',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'hardware_version',
        'name': '硬件版本',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'protocol_version',
        'name': '协议版本',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'channel_count',
        'name': '通道数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'channel_1',
        'name': '通道1',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'channel_2',
        'name': '通道2',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'channel_3',
        'name': '通道3',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'channel_4',
        'name': '通道4',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'channel_5',
        'name': '通道5',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'channel_6',
        'name': '通道6',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'channel_7',
        'name': '通道7',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'channel_8',
        'name': '通道8',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'channel_9',
        'name': '通道9',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'channel_10',
        'name': '通道10',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'channel_11',
        'name': '通道11',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'channel_12',
        'name': '通道12',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'channel_13',
        'name': '通道13',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'channel_14',
        'name': '通道14',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'channel_15',
        'name': '通道15',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'channel_16',
        'name': '通道16',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'package_count',
        'name': '包数量',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'make_package_channel_data', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'collect_time',
        'name': '采集时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'current_time',
        'name': '当前时间',
        'type': 'element',
        'length': 12,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'make_current_time', 'params': []}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'update_time',
        'name': '更新时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'base_state',
        'name': '基本状态',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'power_supply_state',
        'name': '供电状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'control_state',
        'name': '控制状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'position_state',
        'name': '位置状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'metering_state',
        'name': '计量状态',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'electric_meter_state',
        'name': '电表状态',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': 'water_meter_state',
        'name': '水表状态',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'water_level_sensor_state',
        'name': '水位传感器状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'pressure_sensor_state',
        'name': '压力传感器状态',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_bin', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'use_water_process_type',
        'name': '用水过程类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_type', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'account_no',
        'name': '账户编号',
        'type': 'element',
        'length': 16,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'charging_mode',
        'name': '计费模式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'this_use_electric_quantity',
        'name': '本次用电量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': 'this_use_water_quantity',
        'name': '本次用水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0044': {
        'code': 'this_use_time_quantity',
        'name': '本次用时量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': 'this_use_money_quantity',
        'name': '本次用钱量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': 'total_use_electric_quantity',
        'name': '总用电量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': 'total_use_water_quantity',
        'name': '总用水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': 'total_use_time_quantity',
        'name': '总用时量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': 'total_use_money_quantity',
        'name': '总用钱量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0050': {
        'code': 'run_water_meter_quantity',
        'name': '启动水表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': 'current_water_meter_quantity',
        'name': '当前水表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': 'run_electric_meter_quantity',
        'name': '启动电表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': 'current_electric_meter_quantity',
        'name': '当前电表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0054': {
        'code': 'water_level',
        'name': '水位',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0055': {
        'code': 'pressure',
        'name': '压力',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0056': {
        'code': 'record_type',
        'name': '记录类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_type', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0057': {
        'code': 'record_time',
        'name': '记录时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': [], 'code': 'update_command', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0058': {
        'code': 'open_account',
        'name': '开启用户',
        'type': 'element',
        'length': 16,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0059': {
        'code': 'open_time',
        'name': '开启时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0060': {
        'code': 'open_mode',
        'name': '开启方式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0061': {
        'code': 'close_account',
        'name': '关闭用户',
        'type': 'element',
        'length': 16,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0062': {
        'code': 'close_time',
        'name': '关闭时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0063': {
        'code': 'close_mode',
        'name': '关闭方式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0064': {
        'code': 'metering_mode',
        'name': '计量模式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0065': {
        'code': 'use_electric_quantity',
        'name': '用电量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0066': {
        'code': 'use_water_quantity',
        'name': '用水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0067': {
        'code': 'use_time_quantity',
        'name': '用时量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0068': {
        'code': 'use_money_quantity',
        'name': '用钱量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0069': {
        'code': 'run_water_meter_quantity',
        'name': '启动水表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0070': {
        'code': 'stop_water_meter_quantity',
        'name': '关闭水表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0071': {
        'code': 'run_electric_meter_quantity',
        'name': '启动电表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0072': {
        'code': 'stop_electric_meter_quantity',
        'name': '关闭电表量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0073': {
        'code': 'param_type',
        'name': '参数类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': [], 'code': 'update_type', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': [], 'code': 'update_type', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0074': {
        'code': 'engineering_no',
        'name': '工程编号',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0075': {
        'code': 'current_upper_limit',
        'name': '过流电流',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0076': {
        'code': 'voltage_upper_limit',
        'name': '电压上限',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0077': {
        'code': 'voltage_lower_limit',
        'name': '电压下限',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0078': {
        'code': 'extract_water_quantity',
        'name': '开采水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0079': {
        'code': 'extract_electric_quantity',
        'name': '开采电量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0080': {
        'code': 'water_electric_coefficient',
        'name': '水电系数',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'divided_by_100', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'multiplied_by_100', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0081': {
        'code': 'server_ip',
        'name': '服务器IP',
        'type': 'element',
        'length': 48,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_ip', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'ip_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'back_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0082': {
        'code': 'server_port',
        'name': '服务器PORT',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'back_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0083': {
        'code': 'set_result',
        'name': '设置结果',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0084': {
        'code': 'sequence',
        'name': '序号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0085': {
        'code': 'account_type',
        'name': '账户类型',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0086': {
        'code': 'remnant_electric',
        'name': '剩电',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0087': {
        'code': 'remnant_water',
        'name': '剩水',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0088': {
        'code': 'remnant_time',
        'name': '剩时',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0089': {
        'code': 'remnant_money',
        'name': '剩钱',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0090': {
        'code': 'control_object',
        'name': '控制对象',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0091': {
        'code': 'object_no',
        'name': '对象编号',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0092': {
        'code': 'extra_data',
        'name': '附加数据',
        'type': 'element',
        'length': 32,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0093': {
        'code': 'control_permission',
        'name': '控制许可',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0094': {
        'code': 'operate_mode',
        'name': '操作方式',
        'type': 'element',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0095': {
        'code': 'blacklist_count',
        'name': '黑名单数量',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'make_account_no_data', 'params': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0096': {
        'code': 'zone_no',
        'name': '区域号',
        'type': 'element',
        'length': 14,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0097': {
        'code': 'account_balance',
        'name': '账户余额',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0098': {
        'code': 'max_open_pump_duration',
        'name': '最大开泵时长',
        'type': 'element',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },

    '0099': {
        'code': 'account_number',
        'name': '用户编号',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0100': {
        'code': 'recharge_amount',
        'name': '充值金额',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0101': {
        'code': 'recharge_count',
        'name': '充值次数',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0102': {
        'code': 'swipe_count',
        'name': '刷卡次数',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0103': {
        'code': 'water_meter_number',
        'name': '水表序号',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0104': {
        'code': 'water_meter_address',
        'name': '水表地址',
        'type': 'element',
        'length': 14,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0105': {
        'code': 'water_meter_type',
        'name': '水表类型',
        'type': 'element',
        'length': 2,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0106': {
        'code': 'startup_money_quantity',
        'name': '启动钱量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0107': {
        'code': 'closed_money_quantity',
        'name': '关闭钱量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0108': {
        'code': 'annual_water_consumption',
        'name': '年度用水量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0109': {
        'code': 'current_money_quantity',
        'name': '当前钱量',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'float_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0110': {
        'code': 'open_user',
        'name': '开启用户',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0111': {
        'code': 'closed_user',
        'name': '关闭用户',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'to_int', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0112': {
        'code': 'channel_17',
        'name': '通道17',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0113': {
        'code': 'channel_18',
        'name': '通道18',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0114': {
        'code': 'channel_19',
        'name': '通道19',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0115': {
        'code': 'recharge_time',
        'name': '充值时间',
        'type': 'element',
        'length': 12,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'hex_to_time', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

    '0116': {
        'code': 'channel_20',
        'name': '通道20',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'timestamp_to_datetime', 'params': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0117': {
        'code': 'water_time_factor',
        'name': '水时系数',
        'type': 'element',
        'length': 4,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_int', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0118': {
        'code': 'lower_limit_flow',
        'name': '流量下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0119': {
        'code': 'upper_pressure_limit',
        'name': '压力上限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0120': {
        'code': 'lower_pressure_limit',
        'name': '压力下限',
        'type': 'element',
        'length': 8,
        'de_plug': [
            {'return': ['srg_data'], 'code': 'convert_high_low', 'params': ['srg_data']},
            {'return': ['srg_data'], 'code': 'hex_to_float', 'params': ['srg_data']}
        ],
        'en_plug': [
            {'return': ['msg_data'], 'code': 'int_to_hex', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'front_zero_fill', 'params': ['msg_data']},
            {'return': ['msg_data'], 'code': 'convert_high_low', 'params': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '02': {
        'name': '链路检测',
        'type': '上行',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '65': {
        'name': '信息注册',
        'type': '上行',
        'default': [],
        'element': ['0002', '0003', '0004', '0005', '0006', '0007', '0008'],
        'type_dict': {}
    },
    '66': {
        'name': '实时数据',
        'type': '上行',
        'default': [],
        'element': ['0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018', '0019', '0020',
                    '0021', '0022', '0023', '0024', '0025', '0112', '0113', '0114', '0116'],
        'type_dict': {}
    },
    '67': {
        'name': '历史数据',
        'type': '上行',
        'default': [],
        'element': ['0026', '0027', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018',
                    '0019', '0020', '0021', '0022', '0023', '0024', '0025', '0112', '0113', '0114'],
        'type_dict': {}
    },
    '68': {
        'name': '状态信息',
        'type': '上行',
        'default': [],
        'element': ['0029', '0030', '0031', '0032', '0033', '0034', '0035', '0036', '0037', '0038'],
        'type_dict': {}
    },
    '70': {
        'name': '读取终端应用参数',
        'type': '应答',
        'default': ['0073'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '计量参数',
                'element': ['0074', '0075', '0076', '0077', '0078', '0079', '0080'],
            },
            '02': {
                'name': '服务器参数',
                'element': ['0081', '0082'],
            },
        }
    },
    '71': {
        'name': '设置终端应用参数',
        'type': '应答',
        'default': [],
        'element': ['0073', '0083'],
        'type_dict': {}
    },
    '74': {
        'name': '遥控启动',
        'type': '应答',
        'default': [],
        'element': ['0093'],
        'type_dict': {}
    },
    '75': {
        'name': '遥控关闭',
        'type': '应答',
        'default': [],
        'element': ['0093'],
        'type_dict': {}
    },
    'C1': {
        'name': '用水过程',
        'type': '上行',
        'default': ['0039'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '计量用水过程',
                'element': ['0040', '0041', '0042', '0043', '0044', '0045', '0046', '0047', '0048', '0049', '0050',
                            '0051', '0052', '0053', '0054', '0055'],
            }
        }
    },
    'C2': {
        'name': '用水记录',
        'type': '上行',
        'default': ['0056', '0057'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '计量用水记录',
                'element': ['0058', '0059', '0060', '0061', '0062', '0063', '0064', '0065', '0066', '0067', '0068',
                            '0069', '0070', '0071', '0072'],
            }
        }
    },
    'C3': {
        'name': '读取计量账户信息',
        'type': '应答',
        'default': [],
        'element': ['0084', '0085', '0074', '0064', '0086', '0087', '0088', '0089'],
        'type_dict': {}
    },
    'C4': {
        'name': '设置计量账户信息',
        'type': '应答',
        'default': [],
        'element': ['0084', '0083'],
        'type_dict': {}
    },
    'C5': {
        'name': '设置用户卡黑名单',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    'C6': {
        'name': '读取用户卡黑名单',
        'type': '应答',
        'default': [],
        'element': ['0095', '0040'],
        'type_dict': {}
    },
    'C7': {
        'name': '设置区域号',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    'C8': {
        'name': '读取区域号',
        'type': '应答',
        'default': [],
        'element': ['0096'],
        'type_dict': {}
    },
    'C9': {
        'name': '复位参数',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    'CA': {
        'name': '网络开泵',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    'CB': {
        'name': '网络关泵',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },

    # 升级  新增功能
    '69': {
        'name': '自报用水过程',
        'type': '上行',
        'default': ['0039'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '计量用水过程',
                'element': ['0099', '0041', '0042', '0043', '0044', '0045', '0046', '0047', '0048', '0049', '0050',
                            '0051', '0052', '0053', '0054', '0055', '0106', '0109'],
            }
        }
    },
    '6A': {
        'name': '自报用水记录',
        'type': '上行',
        'default': ['0056', '0057'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '计量用水记录',
                'element': ['0110', '0059', '0060', '0111', '0062', '0063', '0064', '0065', '0066', '0067', '0068',
                            '0069', '0070', '0071', '0072', '0046', '0047', '0048', '0049', '0106', '0107', '0102',
                            '0108'],
            }
        }
    },
    '72': {
        'name': '读取计量账户信息',
        'type': '应答',
        'default': [],
        'element': ['0084', '0099', '0074', '0085', '0064', '0086', '0087', '0088', '0089'],
        'type_dict': {}
    },
    '73': {
        'name': '设置计量账号信息',
        'type': '应答',
        'default': [],
        'element': ['0084', '0083'],
        'type_dict': {}
    },
    '76': {
        'name': '充值报文',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    '77': {
        'name': '刷卡次数设置',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    '78': {
        'name': '水表地址设置',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    '79': {
        'name': '水表地址读取',
        'type': '应答',
        'default': [],
        'element': ['0103', '0104'],
        'type_dict': {}
    },
    '7A': {
        'name': '充值完成',
        'type': '上行',
        'default': [],
        'element': ['0099', '0100', '0101', '0115'],
        'type_dict': {}
    },
    '7B': {
        'name': '水表类型设置',
        'type': '应答',
        'default': [],
        'element': ['0083'],
        'type_dict': {}
    },
    '7C': {
        'name': '水表类型读取',
        'type': '应答',
        'default': [],
        'element': ['0103', '0105'],
        'type_dict': {}
    },
    '7F': {
        'name': '数据日报',
        'type': '上行',
        'default': [],
        'element': ['0057', '0066', '0065', '0067'],
        'type_dict': {}
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '02': {
        'name': '链路检测',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '65': {
        'name': '信息注册',
        'type': '应答',
        'default': [],
        'element': ['0000', '0028'],
        'type_dict': {}
    },
    '66': {
        'name': '实时数据',
        'type': '应答',
        'default': [],
        'element': ['0000'],
        'type_dict': {}
    },
    '67': {
        'name': '历史数据',
        'type': '应答',
        'default': [],
        'element': ['0000', '0028'],
        'type_dict': {}
    },
    '68': {
        'name': '状态信息',
        'type': '应答',
        'default': [],
        'element': ['0000'],
        'type_dict': {}
    },
    '70': {
        'name': '读取终端应用参数',
        'type': '上行',
        'default': [],
        'element': ['0073'],
        'type_dict': {}
    },
    '71': {
        'name': '设置终端应用参数',
        'type': '上行',
        'default': ['0073'],
        'element': [],
        'type_dict': {
            '01': {
                'name': '计量参数',
                'element': ['0074', '0075', '0076', '0077', '0078', '0079', '0080'],
            },
            '02': {
                'name': '服务器参数',
                'element': ['0081', '0082'],
            },
        }
    },
    '74': {
        'name': '遥控启动',
        'type': '上行',
        'default': [],
        'element': ['0090', '0091', '0092'],
        'type_dict': {}
    },
    '75': {
        'name': '遥控关闭',
        'type': '上行',
        'default': [],
        'element': ['0090', '0091', '0092'],
        'type_dict': {}
    },
    'C1': {
        'name': '用水过程',
        'type': '应答',
        'default': [],
        'element': ['0000'],
        'type_dict': {}
    },
    'C2': {
        'name': '用水记录',
        'type': '应答',
        'default': [],
        'element': ['0000'],
        'type_dict': {}
    },
    'C3': {
        'name': '读取计量账户信息',
        'type': '上行',
        'default': [],
        'element': ['0084'],
        'type_dict': {}
    },
    'C4': {
        'name': '设置计量账户信息',
        'type': '上行',
        'default': [],
        'element': ['0084', '0099', '0074', '0085', '0064', '0086', '0087', '0088', '0089'],
        'type_dict': {}
    },
    'C5': {
        'name': '设置用户卡黑名单',
        'type': '上行',
        'default': [],
        'element': ['0094', '0040'],
        'type_dict': {}
    },
    'C6': {
        'name': '读取用户卡黑名单',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'C7': {
        'name': '设置区域号',
        'type': '上行',
        'default': [],
        'element': ['0096'],
        'type_dict': {}
    },
    'C8': {
        'name': '读取区域号',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'C9': {
        'name': '复位参数',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'CA': {
        'name': '网络开泵',
        'type': '上行',
        'default': [],
        'element': ['0040', '0041', '0097', '0098'],
        'type_dict': {}
    },
    'CB': {
        'name': '网络关泵',
        'type': '上行',
        'default': [],
        'element': ['0040'],
        'type_dict': {}
    },

    # 升级新增功能
    '69': {
        'name': '自报用水过程',
        'type': '应答',
        'default': [],
        'element': ['0000'],
        'type_dict': {}
    },
    '6A': {
        'name': '自报用水记录',
        'type': '应答',
        'default': [],
        'element': ['0000', '0057'],
        'type_dict': {}
    },
    '72': {
        'name': '读取计量账户信息',
        'type': '上行',
        'default': [],
        'element': ['0084'],
        'type_dict': {}
    },
    '73': {
        'name': '设置计量账号信息',
        'type': '上行',
        'default': [],
        'element': ['0084', '0099', '0074', '0085', '0064', '0086', '0087', '0088', '0089'],
        'type_dict': {}
    },
    '76': {
        'name': '充值报文',
        'type': '上行',
        'default': [],
        'element': ['0099', '0100', '0101'],
        'type_dict': {}
    },
    '77': {
        'name': '刷卡次数设置',
        'type': '上行',
        'default': [],
        'element': ['0099', '0102'],
        'type_dict': {}
    },
    '78': {
        'name': '水表地址设置',
        'type': '上行',
        'default': [],
        'element': ['0103', '0104'],
        'type_dict': {}
    },
    '79': {
        'name': '水表地址读取',
        'type': '上行',
        'default': [],
        'element': ['0103'],
        'type_dict': {}
    },
    '7B': {
        'name': '水表类型设置',
        'type': '上行',
        'default': [],
        'element': ['0103', '0105'],
        'type_dict': {}
    },
    '7C': {
        'name': '水表类型读取',
        'type': '上行',
        'default': [],
        'element': ['0103'],
        'type_dict': {}
    },
    '7A': {
        'name': '充值完成',
        'type': '应答',
        'default': [],
        'element': ['0000'],
        'type_dict': {}
    },
    '7F': {
        'name': '数据日报',
        'type': '应答',
        'default': [],
        'element': ['0000', '0057'],
        'type_dict': {}
    },
}

# 入库的命令列表
IS_SAVE_LIST = ['65', '66', '67', '68', 'C1_01', 'C2_01', '69_01', '6A_01', '77']

# 配置的CLASS
__CLASS__ = 'JDSKMonitorSettingInfo'


class JDSKMonitorSettingInfo(object):
    """
    获取 井电双控智能计量监控设备与管理平台传输协议规范 配置信息
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
                # 具体的解析协议由功能码决定
                return [self.__element_dict[item] for item in self.__device_2_platform[command]['element']]
            else:
                # 具体的解析协议由功能码、数据段类型所决定
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
                # 具体的解析协议由功能码决定
                return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
            else:
                # 具体的解析协议由功能码、数据段类型所决定
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
    setting = JDSKMonitorSettingInfo()
    # print(setting.get_device_2_platform_protocol_dict('70'))
    # print(setting.get_platform_2_device_protocol_dict('C5'))
    for k, v in ELEMENT_DICT.items():
        if v['code'] == '':
            print(v['name'])
