# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2020/05/20

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    u'一号泵远程': {
        'code': '1_pump_remote',
        'name': u'一号泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号泵运行': {
        'code': '1_pump_run',
        'name': u'一号泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号泵故障': {
        'code': '1_pump_breakdown',
        'name': u'一号泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号泵启动': {
        'code': '1_pump_start',
        'name': u'一号泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号泵停止': {
        'code': '1_pump_stop',
        'name': u'一号泵停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号电动阀开': {
        'code': '1_electric_valve_open',
        'name': u'一号电动阀开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号电动阀关': {
        'code': '1_electric_valve_close',
        'name': u'一号电动阀关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号电动阀全开': {
        'code': '1_electric_valve_all_open',
        'name': u'一号电动阀全开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号电动阀全关': {
        'code': '1_electric_valve_all_close',
        'name': u'一号电动阀全关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号频率反馈': {
        'code': '1_frequency_feedback',
        'name': u'一号频率反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号电流反馈': {
        'code': '1_current_feedback',
        'name': u'一号电流反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号出水压力': {
        'code': '1_out_water_pressure',
        'name': u'一号出水压力',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号瞬时流量': {
        'code': '1_instantaneous_flow',
        'name': u'一号瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'一号累计流量': {
        'code': '1_total_flow',
        'name': u'一号累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号泵远程': {
        'code': '2_pump_remote',
        'name': u'二号泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号泵运行': {
        'code': '2_pump_run',
        'name': u'二号泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号泵故障': {
        'code': '2_pump_breakdown',
        'name': u'二号泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号泵启动': {
        'code': '2_pump_start',
        'name': u'二号泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号泵停止': {
        'code': '2_pump_stop',
        'name': u'二号泵停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号电动阀开': {
        'code': '2_electric_valve_open',
        'name': u'二号电动阀开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号电动阀关': {
        'code': '2_electric_valve_close',
        'name': u'二号电动阀关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号电动阀全开': {
        'code': '2_electric_valve_all_open',
        'name': u'二号电动阀全开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号电动阀全关': {
        'code': '2_electric_valve_all_close',
        'name': u'二号电动阀全关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号频率反馈': {
        'code': '2_frequency_feedback',
        'name': u'二号频率反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号电流反馈': {
        'code': '2_current_feedback',
        'name': u'二号电流反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号出水压力': {
        'code': '2_out_water_pressure',
        'name': u'二号出水压力',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号瞬时流量': {
        'code': '2_instantaneous_flow',
        'name': u'二号瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号累计流量': {
        'code': '2_total_flow',
        'name': u'二号累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号泵远程': {
        'code': '3_pump_remote',
        'name': u'三号泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号泵运行': {
        'code': '3_pump_run',
        'name': u'三号泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号泵故障': {
        'code': '3_pump_breakdown',
        'name': u'三号泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号泵启动': {
        'code': '3_pump_start',
        'name': u'三号泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号泵停止': {
        'code': '3_pump_stop',
        'name': u'三号泵停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号电动阀开': {
        'code': '3_electric_valve_open',
        'name': u'三号电动阀开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号电动阀关': {
        'code': '3_electric_valve_close',
        'name': u'三号电动阀关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号电动阀全开': {
        'code': '3_electric_valve_all_open',
        'name': u'三号电动阀全开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号电动阀全关': {
        'code': '3_electric_valve_all_close',
        'name': u'三号电动阀全关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号频率反馈': {
        'code': '3_frequency_feedback',
        'name': u'三号频率反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号电流反馈': {
        'code': '3_current_feedback',
        'name': u'三号电流反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号出水压力': {
        'code': '3_out_water_pressure',
        'name': u'三号出水压力',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号瞬时流量': {
        'code': '3_instantaneous_flow',
        'name': u'三号瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'三号累计流量': {
        'code': '3_total_flow',
        'name': u'三号累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号泵远程': {
        'code': '4_pump_remote',
        'name': u'四号泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号泵运行': {
        'code': '4_pump_run',
        'name': u'四号泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号泵故障': {
        'code': '4_pump_breakdown',
        'name': u'四号泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号泵启动': {
        'code': '4_pump_start',
        'name': u'四号泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号泵停止': {
        'code': '4_pump_stop',
        'name': u'四号泵停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号电动阀开': {
        'code': '4_electric_valve_open',
        'name': u'四号电动阀开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号电动阀关': {
        'code': '4_electric_valve_close',
        'name': u'四号电动阀关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号电动阀全开': {
        'code': '4_electric_valve_all_open',
        'name': u'四号电动阀全开',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号电动阀全关': {
        'code': '4_electric_valve_all_close',
        'name': u'四号电动阀全关',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号频率反馈': {
        'code': '4_frequency_feedback',
        'name': u'四号频率反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号电流反馈': {
        'code': '4_current_feedback',
        'name': u'四号电流反馈',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号出水压力': {
        'code': '4_out_water_pressure',
        'name': u'四号出水压力',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号瞬时流量': {
        'code': '4_instantaneous_flow',
        'name': u'四号瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'四号累计流量': {
        'code': '4_total_flow',
        'name': u'四号累计流量',
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
                'element': [u"一号泵远程", u"一号泵运行", u"一号泵故障", u"一号泵启动", u"一号泵停止", u"一号电动阀开",
                            u"一号电动阀关", u"一号电动阀全开", u"一号电动阀全关", u"一号频率反馈", u"一号电流反馈",
                            u"一号出水压力", u"一号瞬时流量", u"一号累计流量", u"二号泵远程", u"二号泵运行", u"二号泵故障",
                            u"二号泵启动", u"二号泵停止", u"二号电动阀开", u"二号电动阀关", u"二号电动阀全开",
                            u"二号电动阀全关", u"二号频率反馈", u"二号电流反馈", u"二号出水压力", u"二号瞬时流量",
                            u"二号累计流量", u"三号泵远程", u"三号泵运行", u"三号泵故障", u"三号泵启动", u"三号泵停止",
                            u"三号电动阀开", u"三号电动阀关", u"三号电动阀全开", u"三号电动阀全关", u"三号频率反馈",
                            u"三号电流反馈", u"三号出水压力", u"三号瞬时流量", u"三号累计流量", u"四号泵远程",
                            u"四号泵运行", u"四号泵故障", u"四号泵启动", u"四号泵停止", u"四号电动阀开", u"四号电动阀关",
                            u"四号电动阀全开", u"四号电动阀全关", u"四号频率反馈", u"四号电流反馈", u"四号出水压力",
                            u"四号瞬时流量", u"四号累计流量"],
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
            }
        }
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['exdata_R']

# 配置的CLASS
__CLASS__ = 'GrmSJTSettingInfo'


class GrmSJTSettingInfo(object):
    """
    获取GrmSJT协议配置信息
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
    pass
