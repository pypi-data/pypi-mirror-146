# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/07/05

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    u'流量计1瞬时流量': {
        'code': 'instantaneous_flow_1',
        'name': u'流量计1瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'流量计1累积流量': {
        'code': 'total_flow_1',
        'name': u'流量计1累积流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'流量计2瞬时流量': {
        'code': 'instantaneous_flow_2',
        'name': u'流量计2瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'流量计2累积流量': {
        'code': 'total_flow_2',
        'name': u'流量计2累积流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'exdata': {
        'name': '读写数据操作应答',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {
            'R': {
                'name': '读数据操作应答',
                'element': [u'流量计1瞬时流量', u'流量计1累积流量', u'流量计2瞬时流量', u'流量计2累积流量'],
            },
            'W': {
                'name': '写数据操作应答',
                'element': [],
            },
        }
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'exlog': {
        'name': '登录上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'exdata': {
        'name': '读写数据操作上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {
            'R': {
                'name': '读数据操作上行',
                'element': [],
            },
            'W': {
                'name': '写数据操作上行',
                'element': [],
            },
        }
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['exdata_R']

# 配置的CLASS
__CLASS__ = 'GrmFlowMeterSettingInfo'


class GrmFlowMeterSettingInfo(object):
    """
    获取GRMFLOWMETER协议配置信息
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


if __name__ == '__main__':
    setting_info = GrmFlowMeterSettingInfo()
    print(setting_info.get_element_dict())
