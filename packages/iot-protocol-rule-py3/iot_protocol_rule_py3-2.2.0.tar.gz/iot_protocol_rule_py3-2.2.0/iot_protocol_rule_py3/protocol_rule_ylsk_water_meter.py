# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/12/30

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
            {'code': 'data_zfill', 'params': ['msg_data'], 'return': ['msg_data']},
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
        'code': 'bootloader_version',
        'name': 'Bootloader版本',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'total_flow',
        'name': '累计流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_1_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'day_total_flow',
        'name': '日累计流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_1_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 10,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'del_1_byte', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'divided_by_100', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'state_1',
        'name': '状态ST_1',
        'length': 2,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'state_2',
        'name': '状态ST_2',
        'length': 2,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'signal_strength',
        'name': '信号强度',
        'length': 2,
        'de_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'voltage',
        'name': '电压',
        'length': 4,
        'de_plug': [
            {'code': 'convert_high_low', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
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
    '018': {
        'code': 'now_network_mode',
        'name': '当前网络模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'valve_open_close',
        'name': '阀开/关',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'ip',
        'name': 'IP',
        'length': 8,
        'de_plug': [
            {'code': 'hex_ip', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'ip_hex', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'port',
        'name': '端口',
        'length': 4,
        'de_plug': [
            {'code': 'hex_port', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'port_hex', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'active',
        'name': '激活',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'recharge_amount',
        'name': '充值金额',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'code': 'multiplied_by_100', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'data_zfill', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'network_mode',
        'name': '网络模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'unit_code',
        'name': '单位代码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'preset_total_flow',
        'name': '预设累计流量',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'code': 'multiplied_by_100', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'data_zfill', 'params': ['msg_data'], 'return': ['msg_data']},
            {'code': 'convert_high_low', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'upgrade_progress',
        'name': '升级进度',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'to_int', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'upgrade_state',
        'name': '升级状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'start_timestamp',
        'name': '开始时间戳',
        'length': 8,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
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
        'name': '主动上报上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册上行',
                'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009'],
            },
            '0008': {
                'name': '数据上报上行',
                'element': ['010', '011', '012', '005', '013', '014', '015', '016', '017', '018'],
            }
        }
    },
    'B2': {
        'name': '告警上报上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '磁干扰报警上行',
                'element': ['005', '013', '014'],
            },
            '000D': {
                'name': '余额报警上行',
                'element': ['005', '017'],
            }
        }
    },
    'A5': {
        'name': '阀门控制应答',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            'A017': {
                'name': '闸门控制应答1',
                'element': ['013', '014'],
            },
            '17A0': {
                'name': '闸门控制应答2',
                'element': ['013', '014'],
            }
        }
    },
    '84': {
        'name': '写数据应答',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '设置上报周期应答',
                'element': [],
            },
            '000A': {
                'name': '设置服务器信息应答',
                'element': [],
            },
            '000B': {
                'name': '激活写卡状态应答',
                'element': [],
            },
            '000C': {
                'name': '充值应答',
                'element': [],
            },
            '000E': {
                'name': '设置付费方式应答',
                'element': [],
            },
            '000F': {
                'name': '设置网络模式应答',
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
                'name': '设置水表底数应答1',
                'element': ['013', '014'],
            },
            '16A0': {
                'name': '设置水表底数应答2',
                'element': ['013', '014'],
            }
        }
    },
    '81': {
        'name': '读数据应答',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0009': {
                'name': '召测上报周期应答',
                'element': ['006'],
            },
            '000A': {
                'name': '召测服务器信息应答',
                'element': ['020', '021'],
            },
            '000E': {
                'name': '召测付费方式应答',
                'element': ['007'],
            },
            '000F': {
                'name': '召测网络模式应答',
                'element': ['024'],
            }
        }
    },
    '33': {
        'name': '设备升级',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0003': {
                'name': '升级进度上行',
                'element': ['009', '027', '015', '016'],
            },
            '0004': {
                'name': '升级状态上行',
                'element': ['028'],
            },
            '0005': {
                'name': '升级URL应答',
                'element': [],
            }
        }
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '31': {
        'name': '主动上报应答',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0007': {
                'name': '设备注册应答',
                'element': ['005'],
            },
            '0008': {
                'name': '数据上报应答',
                'element': ['005'],
            }
        }
    },
    '32': {
        'name': '告警上报应答',
        'type': '应答',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '磁干扰报警应答',
                'element': [],
            },
            '000D': {
                'name': '余额报警应答',
                'element': [],
            }
        }
    },
    '2A': {
        'name': '阀门控制上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            'A017': {
                'name': '闸门控制上行1',
                'element': ['019'],
            },
            '17A0': {
                'name': '闸门控制上行2',
                'element': ['019'],
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
                'name': '设置上报周期上行',
                'element': ['006'],
            },
            '000A': {
                'name': '设置服务器信息上行',
                'element': ['020', '021'],
            },
            '000B': {
                'name': '激活写卡状态上行',
                'element': ['022'],
            },
            '000C': {
                'name': '充值上行',
                'element': ['023'],
            },
            '000E': {
                'name': '设置付费方式上行',
                'element': ['007'],
            },
            '000F': {
                'name': '设置网络模式上行',
                'element': ['024'],
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
                'element': ['025', '026'],
            },
            '16A0': {
                'name': '设置水表底数上行2',
                'element': ['025', '026'],
            }
        }
    },
    '01': {
        'name': '读数据上行',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0006': {
                'name': '召测上报周期上行',
                'element': [],
            },
            '000A': {
                'name': '召测服务器信息上行',
                'element': [],
            },
            '000E': {
                'name': '召测付费方式上行',
                'element': [],
            },
            '000F': {
                'name': '召测网络模式上行',
                'element': [],
            }
        }
    },
    'B3': {
        'name': '设备升级',
        'type': '上行',
        'default': ['DI', 'SER'],
        'element': [],
        'type_dict': {
            '0003': {
                'name': '升级进度上行',
                'element': [],
            },
            '0004': {
                'name': '升级状态上行',
                'element': [],
            },
            '0005': {
                'name': '升级URL应答',
                'element': ['029', '030'],
            }
        }
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['B1_0007', 'B1_0008', 'B2_0006', 'B2_000D', 'A5_A017', 'A5_17A0', '84_0009', '84_000A', '84_000B',
                '84_000C', '84_000E', '84_000F', '96_A016', '96_16A0', '81_0009', '81_000A', '81_000E', '81_000F']

# 配置的CLASS
__CLASS__ = 'YLSKWaterMeterSettingInfo'


class YLSKWaterMeterSettingInfo(object):
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
        :param protocol:
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
        :param protocol:
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
    setting = YLSKWaterMeterSettingInfo()
    # print(setting.get_platform_2_device_protocol_dict('0007'))

    print('81_000A' in IS_SAVE_LIST)
