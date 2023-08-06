# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/23

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'username',
        'name': u'用户名',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'password',
        'name': u'密码',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'token',
        'name': u'令牌',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'pageIndex',
        'name': u'页索引',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'pageSize',
        'name': u'页条数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'readType',
        'name': u'读取类型',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'meterAddr',
        'name': u'表地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'valveStatus',
        'name': u'阀门状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'Result',
        'name': u'结果',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'Msg',
        'name': u'描述',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'TaskId',
        'name': u'任务ID',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'ExeMark',
        'name': u'执行标记',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '001': {
        'code': 'collectoraddr',
        'name': u'采集地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'imei',
        'name': u'IMEI',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'meteraddr',
        'name': u'表地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'freezedate',
        'name': u'冻结日期',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'readdate',
        'name': u'抄表时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'meternumber',
        'name': u'表读数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'valvestatus',
        'name': u'阀门状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'csq',
        'name': u'信号强度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'voltage',
        'name': u'电池电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'batteryvoltage',
        'name': u'电池状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'attackstate',
        'name': u'攻击状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'IMEI',
        'name': u'IMEI',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'MeterAddr',
        'name': u'表地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'FreezeDate',
        'name': u'冻结日期',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'ReadDate',
        'name': u'抄表时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'MeterNumber',
        'name': u'表读数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'ValveStatus',
        'name': u'阀门状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'CSQ',
        'name': u'信号强度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'Voltage',
        'name': u'电池电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'BatteryVoltage',
        'name': u'电池状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'AttackState',
        'name': u'攻击状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'login': {
        'name': u'登录',
        'type': '应答',
        'default': [],
        'element': ['0003'],
        'type_dict': {}
    },
    'ReadMeterList': {
        'name': u'批量抄表',
        'type': '应答',
        'default': [],
        'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011'],
        'type_dict': {}
    },
    'ReadMeter': {
        'name': u'单个抄表',
        'type': '应答',
        'default': [],
        'element': ['012', '013', '014', '015', '016', '017', '018', '019', '020', '021'],
        'type_dict': {}
    },
    'ValveControl': {
        'name': u'控阀',
        'type': '应答',
        'default': [],
        'element': ['0009', '0010', '0011'],
        'type_dict': {}
    },
    'QueryValveControlResult': {
        'name': u'控阀结果查询',
        'type': '应答',
        'default': [],
        'element': ['0009', '0012', '0010'],
        'type_dict': {}
    }
}
# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'login': {
        'name': u'登录',
        'type': '上行',
        'default': [],
        'element': ['0001', '0002'],
        'type_dict': {}
    },
    'ReadMeterList': {
        'name': u'批量抄表',
        'type': '上行',
        'default': [],
        'element': ['0003', '0004', '0005', '0006'],
        'type_dict': {}
    },
    'ReadMeter': {
        'name': u'单个抄表',
        'type': '上行',
        'default': [],
        'element': ['0003', '0007', '0006'],
        'type_dict': {}
    },
    'ValveControl': {
        'name': u'控阀',
        'type': '上行',
        'default': [],
        'element': ['0003', '0007', '0008'],
        'type_dict': {}
    },
    'QueryValveControlResult': {
        'name': u'控阀结果查询',
        'type': '上行',
        'default': [],
        'element': ['0003', '0007', '0011'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['ReadMeterList']

# 配置的CLASS
__CLASS__ = 'QTXEBWaterMeterSettingInfo'


class QTXEBWaterMeterSettingInfo(object):
    """
    获取科鼎配置信息
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
    pass
