# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/7/27

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'imei',
        'name': u'通讯板唯一ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'iccid',
        'name': u'物联网卡的iccid号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'csq',
        'name': u'信号强度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'dtype',
        'name': u'设备类型',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'dver',
        'name': u'设备固件版本',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'rps',
        'name': u'雨控状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'lps',
        'name': u'光控状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'tps',
        'name': u'温控状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'gs',
        'name': u'通道状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'upds',
        'name': u'上仓门状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'dnds',
        'name': u'下仓门状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'hs',
        'name': u'加热状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'ts',
        'name': u'定时模式',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'lat',
        'name': u'纬度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'lng',
        'name': u'经度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'stamp',
        'name': u'时间戳',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'at',
        'name': u'环境温度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'ah',
        'name': u'环境湿度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'hrt',
        'name': u'加热仓实时温度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'image',
        'name': u'图片',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'status': {
        'name': u'状态报告上行',
        'type': '上行',
        'default': [],
        'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014',
                    '015', '016'],
        'type_dict': {}
    },
    'data': {
        'name': u'数据报告上行',
        'type': '上行',
        'default': [],
        'element': ['001', '017', '018', '019', '006', '007', '008', '014', '015', '016'],
        'type_dict': {}
    },
    'image': {
        'name': u'图片上行',
        'type': '上行',
        'default': [],
        'element': ['001', '020'],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {}

# 入库的命令列表
IS_SAVE_LIST = ['status', 'data', 'image']

# 配置的CLASS
__CLASS__ = 'InsertSituationSettingInfo'


class InsertSituationSettingInfo(object):
    """
    获取新惠普虫情仪协议配置信息
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
            return [self.__element_dict[item]['code'] for item in self.__device_2_platform[command]['element']]
        else:
            return []


if __name__ == '__main__':
    setting_info = InsertSituationSettingInfo()
    print(setting_info.get_device_2_platform_protocol_dict('status'))
