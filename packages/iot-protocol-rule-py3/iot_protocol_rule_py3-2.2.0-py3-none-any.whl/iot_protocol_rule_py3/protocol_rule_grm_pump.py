# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/07/05

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    u'瞬时流量': {
        'code': 'instantaneous_flow',
        'name': u'瞬时流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'累计流量': {
        'code': 'total_flow',
        'name': u'累计流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井阀开阀': {
        'code': 'deep_well_valve_open',
        'name': u'深井阀开阀',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井阀关阀': {
        'code': 'deep_well_valve_close',
        'name': u'深井阀关阀',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井阀停止': {
        'code': 'deep_well_valve_stop',
        'name': u'深井阀停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井阀开到位': {
        'code': 'deep_well_valve_open_in_place',
        'name': u'深井阀开到位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井阀关到位': {
        'code': 'deep_well_valve_close_in_place',
        'name': u'深井阀关到位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井阀故障': {
        'code': 'deep_well_valve_breakdown',
        'name': u'深井阀故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压阀开阀': {
        'code': 'booster_valve_open',
        'name': u'增压阀开阀',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压阀关阀': {
        'code': 'booster_valve_close',
        'name': u'增压阀关阀',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压阀停止': {
        'code': 'booster_valve_stop',
        'name': u'增压阀停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压阀开到位': {
        'code': 'booster_valve_open_in_place',
        'name': u'增压阀开到位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压阀关到位': {
        'code': 'booster_valve_close_in_place',
        'name': u'增压阀关到位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压阀故障': {
        'code': 'booster_valve_breakdown',
        'name': u'增压阀故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'出水阀开阀': {
        'code': 'out_water_valve_open',
        'name': u'出水阀开阀',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'出水阀关阀': {
        'code': 'out_water_valve_close',
        'name': u'出水阀关阀',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'出水阀停止': {
        'code': 'out_water_valve_stop',
        'name': u'出水阀停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'出水阀开到位': {
        'code': 'out_water_valve_open_in_place',
        'name': u'出水阀开到位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'出水阀关到位': {
        'code': 'out_water_valve_close_in_place',
        'name': u'出水阀关到位',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'出水阀故障': {
        'code': 'out_water_valve_breakdown',
        'name': u'出水阀故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵远程': {
        'code': 'deep_well_pump_remote',
        'name': u'深井泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵运行': {
        'code': 'deep_well_pump_run',
        'name': u'深井泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵故障': {
        'code': 'deep_well_pump_breakdown',
        'name': u'深井泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵启动': {
        'code': 'deep_well_pump_start',
        'name': u'深井泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵停止': {
        'code': 'deep_well_pump_stop',
        'name': u'深井泵停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵频率': {
        'code': 'deep_well_pump_frequency',
        'name': u'深井泵频率',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'深井泵电流': {
        'code': 'deep_well_pump_current',
        'name': u'深井泵电流',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵远程': {
        'code': 'booster_pump_remote',
        'name': u'增压泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵运行': {
        'code': 'booster_pump_run',
        'name': u'增压泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵故障': {
        'code': 'booster_pump_breakdown',
        'name': u'增压泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵启动': {
        'code': 'booster_pump_start',
        'name': u'增压泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵停止': {
        'code': 'booster_pump_stop',
        'name': u'增压泵停止',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵频率': {
        'code': 'booster_pump_frequency',
        'name': u'增压泵频率',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'增压泵电流': {
        'code': 'booster_pump_current',
        'name': u'增压泵电流',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号深井泵远程': {
        'code': '2_deep_well_pump_remote',
        'name': u'二号深井泵远程',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号深井泵运行': {
        'code': '2_deep_well_pump_run',
        'name': u'二号深井泵运行',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号深井泵故障': {
        'code': '2_deep_well_pump_breakdown',
        'name': u'二号深井泵故障',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号深井泵启动': {
        'code': '2_deep_well_pump_start',
        'name': u'二号深井泵启动',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    u'二号深井泵停止': {
        'code': '2_deep_well_pump_stop',
        'name': u'二号深井泵停止',
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
                'element': [u"瞬时流量", u"累计流量", u"深井阀开阀", u"深井阀关阀", u"深井阀停止", u"深井阀开到位",
                            u"深井阀关到位", u"深井阀故障", u"增压阀开阀", u"增压阀关阀", u"增压阀停止", u"增压阀开到位",
                            u"增压阀关到位", u"增压阀故障", u"出水阀开阀", u"出水阀关阀", u"出水阀停止", u"出水阀开到位",
                            u"出水阀关到位", u"出水阀故障", u"深井泵远程", u"深井泵运行", u"深井泵故障", u"深井泵启动",
                            u"深井泵停止", u"深井泵频率", u"深井泵电流", u"增压泵远程", u"增压泵运行", u"增压泵故障",
                            u"增压泵启动", u"增压泵停止", u"增压泵频率", u"增压泵电流", u"二号深井泵远程",
                            u"二号深井泵运行", u"二号深井泵故障", u"二号深井泵启动", u"二号深井泵停止"],
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
__CLASS__ = 'GrmPumpSettingInfo'


class GrmPumpSettingInfo(object):
    """
    获取GrmPump协议配置信息
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
