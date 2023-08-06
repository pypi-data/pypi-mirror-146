# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/03/30

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    'DI': {
        'code': 'di',
        'name': '数据标识DI',
        'length': 4,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'SER': {
        'code': 'ser',
        'name': '序号SER',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'CONTROL_FRAME': {
        'code': 'control_frame',
        'name': '控制帧',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'PROTOCOL_VERSION': {
        'code': 'protocol_version',
        'name': '协议版本',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '001': {
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
    '002': {
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
    '003': {
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
    '004': {
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
    '005': {
        'code': 'actual_time',
        'name': '实时时间',
        'length': 14,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'update_command', 'params': ['srg_data'], 'return': []}
        ],
        'en_plug': [
            {'code': 'syn_time', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
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
    '007': {
        'code': 'pay_mode',
        'name': '付费方式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'default_network_mode',
        'name': '默认网络模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'network_module_type',
        'name': '网络模块类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
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
    '011': {
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
    '012': {
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
    '013': {
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
    '014': {
        'code': 'state_1',
        'name': '状态ST_1',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'state_2',
        'name': '状态ST_2',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
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
    '017': {
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
    '018': {
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
    '019': {
        'code': 'now_network_mode',
        'name': '当前网络模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
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
    '021': {
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
    '022': {
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
    '023': {
        'code': 'base_station_community_id',
        'name': '基站小区ID',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'base_station_location_info_lac',
        'name': '基站位置信息LAC',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'device_run_time',
        'name': '设备运行时间',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'send_success_count',
        'name': '发送成功次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'send_failed_count',
        'name': '发送失败次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'open_valve_count',
        'name': '开阀次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'close_valve_count',
        'name': '关阀次数',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'signal_percentage',
        'name': '信号百分比',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'electric_percentage',
        'name': '电量百分比',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'valve_open_close',
        'name': '阀开/关',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
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
    '034': {
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
    '035': {
        'code': 'start_time_point',
        'name': '开始时间点',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'int_to_hex', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'msg_zfill', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'end_time_point',
        'name': '结束时间点',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'int_to_hex', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'msg_zfill', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'active_write_card_flg',
        'name': '激活写卡标志',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'recharge_amount',
        'name': '充值金额',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'code': 'multiplied_by_100', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'msg_zfill', 'params': [], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'network_mode',
        'name': '网络模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'debug_mode_state',
        'name': '调试模式状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'long_lived_start_time',
        'name': '长连接开始时间',
        'length': 14,
        'de_plug': [],
        'en_plug': [
            {'code': 'time_to_hex', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'long_lived_duration',
        'name': '长连接时长',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_to_hex', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'msg_zfill', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '043': {
        'code': 'unit_code',
        'name': '单位代码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'preset_total_flow',
        'name': '预设累计流量',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'code': 'multiplied_by_100', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'msg_zfill', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'upgrade_progress_percentage',
        'name': '升级进度百分比',
        'length': 2,
        'de_plug': [
            {'code': 'hex_to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'upgrade_state',
        'name': '升级状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'start_timestamp',
        'name': '开始时间戳',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'upgrade_url',
        'name': '升级URL',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    'B1': {
        'name': '主动上报',
        'type': '上行',
        'default': ['DI', 'SER', 'CONTROL_FRAME', 'PROTOCOL_VERSION'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册',
                'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010'],
            },
            '0008': {
                'name': '数据上报',
                'element': ['011', '012', '013', '005', '014', '015', '016', '017', '018', '019', '020', '021', '022',
                            '023', '024'],
            },
            '0010': {
                'name': '调试上报',
                'element': ['025', '026', '027', '028', '029', '030', '031'],
            },
            '0019': {
                'name': '长连接心跳',
                'element': [],
            }
        }
    },
    'B9': {
        'name': '主动上报',
        'type': '上行',
        'default': ['DI', 'SER', 'CONTROL_FRAME', 'PROTOCOL_VERSION'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册',
                'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010'],
            },
            '0008': {
                'name': '数据上报',
                'element': ['011', '012', '013', '005', '014', '015', '016', '017', '018', '019', '020', '021', '022',
                            '023', '024'],
            },
            '0010': {
                'name': '调试上报',
                'element': ['025', '026', '027', '028', '029', '030', '031'],
            },
            '0019': {
                'name': '长连接心跳',
                'element': [],
            }
        }
    },
    'B2': {
        'name': '告警上报',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '磁干扰报警上行',
                'element': ['005', '014', '015'],
            },
            '000D': {
                'name': '余额报警上行',
                'element': ['005', '018'],
            }
        }
    },
    'A5': {
        'name': '阀门控制',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            'A017': {
                'name': '闸门控制_1',
                'element': ['014', '015'],
            },
            '17A0': {
                'name': '闸门控制_2',
                'element': ['014', '015'],
            }
        }
    },
    '84': {
        'name': '写数据',
        'type': '应答',
        'default': ['DI', 'SER'],
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
                'name': '付费方式配置',
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
            }
        }
    },
    '96': {
        'name': '设置水表底数应答',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            'A016': {
                'name': '设置水表底数_1',
                'element': ['014', '015'],
            },
            '16A0': {
                'name': '设置水表底数_2',
                'element': ['014', '015'],
            }
        }
    },
    '81': {
        'name': '读数据',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '召测上报周期',
                'element': ['006'],
            },
            '000A': {
                'name': '召测服务器信息',
                'element': ['033', '034'],
            },
            '000E': {
                'name': '召测付费方式',
                'element': ['007'],
            },
            '000F': {
                'name': '召测网络模式',
                'element': ['039'],
            },
            '0011': {
                'name': '召测上报时间点',
                'element': ['035', '036'],
            }
        }
    },
    'B3': {
        'name': '设备升级',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0003': {
                'name': '升级进度',
                'type': '上行',
                'element': ['010', '045', '016', '017'],
            },
            '0004': {
                'name': '升级状态',
                'type': '上行',
                'element': ['045'],
            },
            '0005': {
                'name': '升级URL',
                'type': '应答',
                'element': [],
            }
        }
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '31': {
        'name': '主动上报',
        'type': '应答',
        'default': ['DI', 'SER', 'CONTROL_FRAME'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册',
                'element': ['005'],
            },
            '0008': {
                'name': '数据上报',
                'element': ['005'],
            },
            '0010': {
                'name': '调试上报',
                'element': [],
            },
            '0019': {
                'name': '长连接心跳',
                'element': [],
            }
        }
    },
    '32': {
        'name': '告警上报',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '磁干扰报警',
                'element': [],
            },
            '000D': {
                'name': '余额报警',
                'element': [],
            }
        }
    },
    '2A': {
        'name': '阀门控制',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            'A017': {
                'name': '闸门控制_1',
                'element': ['032'],
            },
            '17A0': {
                'name': '闸门控制_2',
                'element': ['032'],
            }
        }
    },
    '04': {
        'name': '写数据上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '设置上报周期',
                'element': ['006'],
            },
            '000A': {
                'name': '设置服务器信息',
                'element': ['033', '034'],
            },
            '000B': {
                'name': '激活写卡状态',
                'element': ['037'],
            },
            '000C': {
                'name': '充值上行',
                'element': ['038'],
            },
            '000E': {
                'name': '设置付费方式',
                'element': ['007'],
            },
            '000F': {
                'name': '设置网络模式',
                'element': ['039'],
            },
            '0011': {
                'name': '设置上报时间点',
                'element': ['035', '036'],
            },
            '0012': {
                'name': '设置调试模式状态',
                'element': ['040'],
            },
            '0013': {
                'name': '设置长连接',
                'element': ['041', '042'],
            }
        }
    },
    '0C': {
        'name': '写数据上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '设置上报周期',
                'element': ['006'],
            },
            '000A': {
                'name': '设置服务器信息',
                'element': ['033', '034'],
            },
            '000B': {
                'name': '激活写卡状态',
                'element': ['037'],
            },
            '000C': {
                'name': '充值上行',
                'element': ['038'],
            },
            '000E': {
                'name': '设置付费方式',
                'element': ['007'],
            },
            '000F': {
                'name': '设置网络模式',
                'element': ['039'],
            },
            '0011': {
                'name': '设置上报时间点',
                'element': ['035', '036'],
            },
            '0012': {
                'name': '设置调试模式状态',
                'element': ['040'],
            },
            '0013': {
                'name': '设置长连接',
                'element': ['041', '042'],
            }
        }
    },
    '16': {
        'name': '设置水表底数上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            'A016': {
                'name': '设置水表底数上行1',
                'element': ['043', '044'],
            },
            '16A0': {
                'name': '设置水表底数上行2',
                'element': ['043', '044'],
            }
        }
    },
    '01': {
        'name': '读数据上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '召测上报周期',
                'element': [],
            },
            '000A': {
                'name': '召测服务器信息',
                'element': [],
            },
            '000E': {
                'name': '召测付费方式',
                'element': [],
            },
            '000F': {
                'name': '召测网络模式',
                'element': [],
            },
            '0011': {
                'name': '召测上报时间点',
                'element': [],
            }
        }
    },
    '33': {
        'name': '设备升级',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0003': {
                'name': '升级进度',
                'type': '应答',
                'element': [],
            },
            '0004': {
                'name': '升级状态',
                'type': '应答',
                'element': [],
            },
            '0005': {
                'name': '升级URL',
                'type': '上行',
                'element': ['047', '048'],
            }
        }
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['B1_0007', 'B1_0008', 'B1_0010', 'B1_0019', 'B2_0006', 'B2_000D', 'B1_0007', 'B1_0008', 'B1_0010',
                'B1_0019', 'B2_0006', 'B2_000D', 'A5_A017', 'A5_17A0', '84_0009', '84_000A', '84_000B', '84_000C',
                '84_000E', '84_000F', '84_0011', '84_0012', '84_0013', '96_A016', '96_16A0', '81_0009', '81_000A',
                '81_000E', '81_000F', '81_0011', 'B3_0003', 'B3_0004', 'B3_0005']

# 配置的CLASS
__CLASS__ = 'YLSKWaterMeterV2SettingInfo'


class YLSKWaterMeterV2SettingInfo(object):
    """
    获取优联时空水表配置信息
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
            protocol_dict = {
                'default': [self.__element_dict[item] for item in self.__device_2_platform[command]['default']],
                'type_dict': {}
            }
            for type_key, type_value in self.__device_2_platform[command]['type_dict'].items():
                protocol_dict['type_dict'][type_key] = [self.__element_dict[item] for item in type_value['element']]

            return protocol_dict
        else:
            return {}

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
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
            return {}


if __name__ == '__main__':
    setting = YLSKWaterMeterV2SettingInfo()
    # print(setting.get_platform_2_device_protocol_dict('0007'))

    print('81_000A' in IS_SAVE_LIST)
