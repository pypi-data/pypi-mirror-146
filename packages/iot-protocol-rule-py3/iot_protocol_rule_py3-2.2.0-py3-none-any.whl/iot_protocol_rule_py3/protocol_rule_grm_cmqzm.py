# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/07/08

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    u'一号闸远程': {
        'code': 'GATE1_REMOTE',
        'name': u'一号闸远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸使能': {
        'code': 'GATE1_ENABLED',
        'name': u'一号闸使能',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸启动': {
        'code': 'GATE1_START',
        'name': u'一号闸启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸停止': {
        'code': 'GATE1_STOP',
        'name': u'一号闸停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸复位': {
        'code': 'GATE1_RESET',
        'name': u'一号闸复位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸开度反馈': {
        'code': 'GATE1_OPEN_FEEDBACK',
        'name': u'一号闸开度反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸报警值': {
        'code': 'GATE1_ALARM_VALUE',
        'name': u'一号闸报警值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号闸开度设定': {
        'code': 'GATE1_OPEN_SET',
        'name': u'一号闸开度设定',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸远程': {
        'code': 'GATE2_REMOTE',
        'name': u'二号闸远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸使能': {
        'code': 'GATE2_ENABLED',
        'name': u'二号闸使能',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸启动': {
        'code': 'GATE2_START',
        'name': u'二号闸启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸停止': {
        'code': 'GATE2_STOP',
        'name': u'二号闸停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸复位': {
        'code': 'GATE2_RESET',
        'name': u'二号闸复位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸开度反馈': {
        'code': 'GATE2_OPEN_FEEDBACK',
        'name': u'二号闸开度反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸报警值': {
        'code': 'GATE2_ALARM_VALUE',
        'name': u'二号闸报警值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号闸开度设定': {
        'code': 'GATE2_OPEN_SET',
        'name': u'二号闸开度设定',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
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
                'element': [
                    u"一号闸远程", u"一号闸使能", u"一号闸启动", u"一号闸停止", u"一号闸复位", u"一号闸开度反馈", u"一号闸报警值", u"一号闸开度设定",
                    u"二号闸远程", u"二号闸使能", u"二号闸启动", u"二号闸停止", u"二号闸复位", u"二号闸开度反馈", u"二号闸报警值", u"二号闸开度设定"
                ],
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
__CLASS__ = 'GrmCmqzmSettingInfo'


class GrmCmqzmSettingInfo(object):
    """
    获取长鸣渠协议配置信息
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
    print(ELEMENT_DICT.keys())
