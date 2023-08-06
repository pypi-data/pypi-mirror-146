# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2022/02/15

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'order_issue_flow_number',
        'name': u'指令下发流水号',
        'length': 4,
        'de_plug': [
            {'code': 'update_command', 'params': ['srg_data'], 'return': []}
        ],
        'en_plug': [
            {'code': 'get_order_issue_flow_number', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'reporting_time',
        'name': u'发报时间',
        'length': 12,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'update_command', 'params': ['srg_data'], 'return': []}
        ],
        'en_plug': [
            {'code': 'get_report_time', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'telemetry_station_address',
        'name': u'遥测站地址',
        'length': 14,
        'de_plug': [
            {'code': 'del_4_bit', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'telemetry_station_type_code',
        'name': u'遥测站分类码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'observe_time',
        'name': u'观测时间',
        'length': 14,
        'de_plug': [
            {'code': 'del_4_bit', 'params': ['srg_data'], 'return': ['srg_data']},
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'result',
        'name': u'结果',
        'length': 2,
        'de_plug': [],
        'en_plug': [
            {'code': 'zfill_0', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'pump_state',
        'name': u'泵状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'user_no',
        'name': u'用户号',
        'length': 22,
        'de_plug': [
            {'code': 'del_6_bit', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'make_user_no', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'balance',
        'name': u'余额',
        'length': 16,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_balance', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '28': {
        'code': 'Q1',
        'name': u'机井瞬时流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '38': {
        'code': 'VT',
        'name': u'电源电压',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3C': {
        'code': 'Z1',
        'name': u'机井水位',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '45': {
        'code': 'ZT',
        'name': u'遥测站状态及报警信息',
        'length': None,
        'de_plug': [
            {'code': 'hex_bin', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '58': {
        'code': 'WP1',
        'name': u'机井管道水压',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '70': {
        'code': 'VTA',
        'name': u'交流A相电压',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '71': {
        'code': 'VTB',
        'name': u'交流B相电压',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '72': {
        'code': 'VTC',
        'name': u'交流C相电压',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '73': {
        'code': 'VIA',
        'name': u'交流A相电流',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '74': {
        'code': 'VIB',
        'name': u'交流B相电流',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '75': {
        'code': 'VIC',
        'name': u'交流C相电流',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'F0': {
        'code': 'TT',
        'name': u'观测时间',
        'length': None,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'F1': {
        'code': 'ST',
        'name': u'遥测站地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF01': {
        'code': 'JJLJLL',
        'name': u'机井累计流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF02': {
        'code': 'CSQ',
        'name': u'信号强度CSQ',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF03': {
        'code': 'BNSDLJLL',
        'name': u'本年设定累计流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF04': {
        'code': 'BNLJLL',
        'name': u'本年累计流量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF05': {
        'code': 'LJDL',
        'name': u'累计电量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF06': {
        'code': 'YHH',
        'name': u'用户号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF07': {
        'code': 'BCSYDL',
        'name': u'本次使用电量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF08': {
        'code': 'BCSYSL',
        'name': u'本次使用水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF09': {
        'code': 'BCKSSJ',
        'name': u'本次开始时间',
        'length': None,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF0A': {
        'code': 'BCJSSJ',
        'name': u'本次结束时间',
        'length': None,
        'de_plug': [
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF0B': {
        'code': 'JJBH',
        'name': u'机井编号',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF0C': {
        'code': 'XZQHJB',
        'name': u'行政区级别',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FF0D': {
        'code': 'XZQHBM',
        'name': u'行政区编码',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA1': {
        'code': 'YE',
        'name': u'余额',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA2': {
        'code': 'SSJE',
        'name': u'实时金额',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA3': {
        'code': 'ZCZJE',
        'name': u'总充值金额',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA4': {
        'code': 'ZCZSL',
        'name': u'总充值水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA5': {
        'code': 'ZCZDL',
        'name': u'总充值电量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA6': {
        'code': 'ZSYJE',
        'name': u'总使用金额',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA7': {
        'code': 'ZSYSL',
        'name': u'总使用水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFA8': {
        'code': 'ZSYDL',
        'name': u'总使用电量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFAB': {
        'code': 'YHLJYSL',
        'name': u'用户累计用水量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFAC': {
        'code': 'YHLJYDL',
        'name': u'用户累计用电量',
        'length': None,
        'de_plug': [
            {'code': 'int_float', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFAE': {
        'code': 'JHID',
        'name': u'计划ID',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'FFFE': {
        'code': 'BBH',
        'name': u'版本号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '2F': {
        'name': u'链路维持报上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '32': {
        'name': u'遥测站定时报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['FFFE', 'FF0B', '3C', '58', '28', 'FF04', 'FF01', 'FF05', 'FF06', '45', '70', '71', '72', '73', '74', '75', '38',
                    'FF02'],
        'type_dict': {}
    },
    '33': {
        'name': u'遥测站加时报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '34': {
        'name': u'遥测站小时报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    '4A': {
        'name': u'中心站设置遥测站时钟应答',
        'type': '应答',
        'default': ['0001', '0002', '0003'],
        'element': [],
        'type_dict': {}
    },
    'E0': {
        'name': u'机井定点报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['FFFE', 'FF0B', '3C', '58', '28', 'FF04', 'FF01', 'FF05', 'FF06', '45', '70', '71', '72', '73', '74', '75', '38',
                    'FF02'],
        'type_dict': {}
    },
    'E1': {
        'name': u'机井开泵上报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['FFFE', 'FF0B', '3C', '58', '28', 'FF04', 'FF01', 'FF05', 'FF06', 'FFA3', 'FFA4', 'FFA5', 'FF07', 'FF08', 'FF0C',
                    'FF09', 'FF0A', 'FFA6', 'FFA7', 'FFA8', 'FFAB', 'FFAC', 'FFAE', '45', '70', '71', '72', '73', '74', '75', '38', 'FF02'],
        'type_dict': {}
    },
    'E2': {
        'name': u'机井关泵上报上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': ['FFFE', 'FF0B', '3C', '58', '28', 'FF04', 'FF01', 'FF05', 'FF06', 'FFA3', 'FFA4', 'FFA5', 'FF07', 'FF08', 'FF0C',
                    'FF09', 'FF0A', 'FFA6', 'FFA7', 'FFA8', 'FFAB', 'FFAC', 'FFAE', '45', '70', '71', '72', '73', '74', '75', '38', 'FF02'],
        'type_dict': {}
    },
    'E7': {
        'name': u'遥测站登录上行',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0005'],
        'element': [],
        'type_dict': {}
    },
    'E9': {
        'name': u'实时交易状态上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': ['FF06', 'FF07', 'FF08', 'FF0C', 'FF09', 'FF0A', 'FFA6', 'FFA7', 'FFA8', 'FFAB', 'FFAC', 'FFAE'],
        'type_dict': {}
    },
    'EB': {
        'name': u'远程开关泵（计费）应答',
        'type': '上行',
        'default': ['0001', '0002', '0003', '0004', '0008', '0006'],
        'element': [],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '32': {
        'name': u'遥测站定时报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '33': {
        'name': u'遥测站加时报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '34': {
        'name': u'遥测站小时报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    '4A': {
        'name': u'中心站设置遥测站时钟上行',
        'type': '上行',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    'E0': {
        'name': u'机井定点报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    'E1': {
        'name': u'机井开泵上报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    'E2': {
        'name': u'机井关泵上报应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    'E7': {
        'name': u'遥测站登录应答',
        'type': '应答',
        'default': ['0001', '0002', '0006'],
        'element': [],
        'type_dict': {}
    },
    'E9': {
        'name': u'实时交易状态应答',
        'type': '应答',
        'default': ['0001', '0002'],
        'element': [],
        'type_dict': {}
    },
    'EB': {
        'name': u'远程开关泵（计费）上行',
        'type': '上行',
        'default': ['0001', '0002', '0007', '0008', '0009'],
        'element': [],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['32', 'E0', 'E1', 'E2', 'E9']

# 配置的CLASS
__CLASS__ = 'XMSXJJSettingInfo'


class XMSXJJSettingInfo(object):
    """
    厦门四信 机井 配置信息
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
    pass
