# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/09/10

@author: gw
"""
import hashlib
import random
import string
import time

# 元素字典
ELEMENT_DICT = {
    '1': {
        'code': 'air_temperature',
        'name': u'空气温度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '2': {
        'code': 'air_humidity',
        'name': u'空气湿度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '3': {
        'code': 'carbon_dioxide_concentration',
        'name': u'二氧化碳浓度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '4': {
        'code': 'light_intensity',
        'name': u'光照度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '5': {
        'code': 'soil_temperature',
        'name': u'土壤温度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '6': {
        'code': 'soil_moisture',
        'name': u'土壤水分',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '7': {
        'code': 'wind_speed',
        'name': u'风速',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '8': {
        'code': 'wind_direction',
        'name': u'风向',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '9': {
        'code': 'atmospheric_pressure',
        'name': u'大气压力',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10': {
        'code': 'rainfall',
        'name': u'雨量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '11': {
        'code': 'total_radiation',
        'name': u'总辐射',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '12': {
        'code': 'photosynthetically_radiation',
        'name': u'光合有效辐射',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '13': {
        'code': 'pipe_conductivity_(EC)',
        'name': u'管道电导率(EC)',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '14': {
        'code': 'pipe_pH',
        'name': u'管道酸碱值(pH)',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '15': {
        'code': 'pressure',
        'name': u'压力',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '16': {
        'code': 'evaporation_(ET)',
        'name': u'蒸发量(ET)',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '17': {
        'code': 'soil_salinity',
        'name': u'土壤盐分',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '18': {
        'code': 'soil_conductivity_(EC)',
        'name': u'土壤电导率(EC)',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '19': {
        'code': 'soil_pH',
        'name': u'土壤酸碱值(pH)',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '20': {
        'code': 'PM2.5',
        'name': u'PM2.5',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '21': {
        'code': 'PM100',
        'name': u'PM100',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '33': {
        'code': 'water_instantaneous_flow',
        'name': u'入水瞬时流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '34': {
        'code': 'fertilizer_instantaneous_flow',
        'name': u'肥通道瞬时流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '40': {
        'code': 'water_total_this_time',
        'name': u'入水(本次)累计总量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '41': {
        'code': 'fertilizer_total_this_time',
        'name': u'肥通道(本次)总量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '49': {
        'code': 'water_total_history',
        'name': u'入水(历史)累计总量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '50': {
        'code': 'fertilizer_total_history',
        'name': u'肥通道(历史)总量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '65': {
        'code': 'rain_snow',
        'name': u'雨雪',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '66': {
        'code': 'liquid_level',
        'name': u'液位',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '67': {
        'code': 'frost',
        'name': u'霜冻',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '97': {
        'code': 'plant_growth_lamp',
        'name': u'植物生长灯',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '98': {
        'code': 'fan',
        'name': u'风机',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '99': {
        'code': 'carbon_dioxide_tank',
        'name': u'二氧化碳罐',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '100': {
        'code': 'irrigation_valve',
        'name': u'灌溉阀',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '101': {
        'code': 'insecticide_lamp',
        'name': u'杀虫灯',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '102': {
        'code': 'dehumidifier',
        'name': u'除湿机',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '103': {
        'code': 'auxiliary_switch',
        'name': u'辅助开关',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '104': {
        'code': 'fertilizer_channel_switch',
        'name': u'注肥通道开关',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '144': {
        'code': 'irrigation_area',
        'name': u'灌区',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'token': {
        'code': 'token',
        'name': u'通用令牌',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'username': {
        'code': 'username',
        'name': u'用户名',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'password': {
        'code': 'password',
        'name': u'用户密码',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'groupid': {
        'code': 'groupid',
        'name': u'项目id',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'deviceIndex': {
        'code': 'deviceIndex',
        'name': u'设备索引',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'action': {
        'code': 'action',
        'name': u'控制状态',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'jsonstr': {
        'code': 'jsonstr',
        'name': u'打开关闭',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'msgID': {
        'code': 'msgID',
        'name': u'设备类型',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },

}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'getDeviceListByGroupIDV2': {
        'name': u'获取变量实时数据',
        'type': '应答',
        'default': [],
        'element': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '33', '34', '40', '41', '49', '50', '65', '66', '67', '97', '98', '99', '100', '101', '102', '103', '104', '144'],
        'type_dict': {}
    },

}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'login': {
        'name': u'获取TOKEN上行',
        'type': '上行',
        'default': [],
        'element': ['username', 'password'],
        'type_dict': {}
    },
    'getGroupListV2': {
        'name': u'获取水肥机列表',
        'type': '上行',
        'default': [],
        'element': ['username', 'token'],
        'type_dict': {}
    },
    'getDeviceListByGroupIDV2': {
        'name': u'获取变量实时数据上行',
        'type': '上行',
        'default': [],
        'element': ['username', 'token', 'groupid'],
        'type_dict': {}
    },
    'operateDeviceV3': {
        'name': u'控制变量上行',
        'type': '上行',
        'default': [],
        'element': ['username', 'token', 'deviceIndex', 'action','msgID'],
        'type_dict': {}
    }
}

IS_SAVE_LIST = ['getDeviceListByGroupIDV2']
# 配置的CLASS
__CLASS__ = 'XingLianYunKeSettingInfo'


class XingLianYunKeSettingInfo(object):
    """
    获取明牛协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__root_url = 'https://cloud.satlic.com:9090/api/'
        self.__element_dict = ELEMENT_DICT
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__is_save_list = IS_SAVE_LIST

    def get_root_url(self):
        """
        获取请求根路径
        :return:
        """
        return self.__root_url

    def get_element_dict(self):
        """
        获取元素字典
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

    def get_random(self):
        """
        获取随机6位字母与数字的字符串
        :return:
        """
        return ''.join(random.sample(string.ascii_lowercase + string.digits, 6))

    def get_timestamp(self):
        """
        获取当前时间戳
        :return:
        """
        return str(int(round(time.time() * 1000)))

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
    print(ELEMENT_DICT.keys())
