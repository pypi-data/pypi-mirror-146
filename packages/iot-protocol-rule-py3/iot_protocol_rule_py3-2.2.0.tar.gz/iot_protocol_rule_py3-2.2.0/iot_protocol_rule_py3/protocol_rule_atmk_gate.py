# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/21

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'reportTm',
        'name': u'上报时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'gatePos',
        'name': u'闸门开度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'gateLevl',
        'name': u'闸门闸位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'frontWl',
        'name': u'闸前水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'backWl',
        'name': u'闸后水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'instance',
        'name': u'瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'accumulate',
        'name': u'累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'boxWl',
        'name': u'测水箱水位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'rechargeVoltage',
        'name': u'充电电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'rechargeElectricity',
        'name': u'充电电流',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'batteryVoltage',
        'name': u'电池电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'workVoltage',
        'name': u'工作电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'workElectricity',
        'name': u'工作电流',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'temperature',
        'name': u'温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'motorElectricity',
        'name': u'电机电流',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'rotateSpeed',
        'name': u'转速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'dtuModel',
        'name': u'DTU工作模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'currAmount',
        'name': u'本次用水量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'accAmount',
        'name': u'累计用水量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'currRunTime',
        'name': u'本次运行时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'accRunTime',
        'name': u'累计运行时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'remainWorkTime',
        'name': u'剩余工作时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'opModel',
        'name': u'操作模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'emControlType',
        'name': u'闸门控制方式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'motorStatus',
        'name': u'电机状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'emDirect',
        'name': u'电机方向',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'upperLimit',
        'name': u'上限位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'lowerLimit',
        'name': u'下限位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'execTimeout',
        'name': u'执行超时',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'getElecType',
        'name': u'本地/供电方式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'teleCommunicationStatus',
        'name': u'远程通讯状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'controlWorkModel',
        'name': u'控制器工作模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'gateAddr': {
        'code': 'gateAddr',
        'name': u'闸门地址',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'posi': {
        'code': 'posi',
        'name': u'开启闸门高度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'instance': {
        'code': 'instance',
        'name': u'闸门瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'getRealData': {
        'name': u'获取闸门最新数据',
        'type': '应答',
        'default': [],
        'element': [str(index).zfill(3) for index in range(1, 33)],
        'type_dict': {}
    }
}
# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'getRealData': {
        'name': u'获取闸门最新数据',
        'type': '上行',
        'default': [],
        'element': ['gateAddr'],
        'type_dict': {}
    },
    'setGatePosi': {
        'name': u'开度控制',
        'type': '上行',
        'default': [],
        'element': ['gateAddr', 'posi'],
        'type_dict': {}
    },
    'setGateInstance': {
        'name': u'流量控制',
        'type': '上行',
        'default': [],
        'element': ['gateAddr', 'instance'],
        'type_dict': {}
    },
    'setGateStop': {
        'name': u'闸门停止',
        'type': '上行',
        'default': [],
        'element': ['gateAddr'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['getRealData']

# 配置的CLASS
__CLASS__ = 'ATMKSettingInfo'


class ATMKSettingInfo(object):
    """
    获取奥特美克配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__element_list = [ELEMENT_DICT[str(item).zfill(3)]['code'] for item in range(1, 33)]
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

    def get_element_list(self):
        """
        获取元素列表
        :return:
        """
        return self.__element_list

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param command:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
        else:
            return []


if __name__ == '__main__':
    setting = ATMKSettingInfo()
    print(setting.get_element_list())
