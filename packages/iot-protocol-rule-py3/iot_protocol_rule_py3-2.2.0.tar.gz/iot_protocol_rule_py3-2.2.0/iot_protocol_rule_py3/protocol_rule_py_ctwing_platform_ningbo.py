# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/09/02

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'batteryThreshold',
        'name': '电量告警门限',
        'length': None,
        'de_plug': [{'code': 'divide_by_100', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'batteryLevel',
        'name': '电池电压',
        'length': None,
        'de_plug': [{'code': 'divide_by_100', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'valveStatus',
        'name': '阀门状态',
        'length': None,
        'de_plug': [{'code': 'to_valve_status', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'softVersion',
        'name': '软件版本',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'signalStrength',
        'name': '信号强度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'sendTime',
        'name': '发送时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'rssi',
        'name': 'rssi',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'pci',
        'name': 'pci',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'motorStatus',
        'name': '马达状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'meterCode',
        'name': '表号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'frequency',
        'name': '频率',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'dailyActivityTime',
        'name': '日通讯激活时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'currentReading',
        'name': '累积流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'timeOfStarting',
        'name': '密集采集(5分钟)起始时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'timeOfReading',
        'name': '数据采集时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'temperature',
        'name': '温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'snr',
        'name': '信噪比',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'pulse',
        'name': '脉冲',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'peakFlowRateTime',
        'name': '日最高流速时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'peakFlowRate',
        'name': '日最高流速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'intervalPressures',
        'name': '瞬时压力',
        'length': None,
        'de_plug': [{'code': 'list_to_str', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'intervalFlowStartingTime',
        'name': '间隔流量起始时间',
        'length': None,
        'de_plug': [{'code': 'to_time', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'intervalFlow',
        'name': '间隔流量(30分钟)',
        'length': None,
        'de_plug': [{'code': 'list_to_str', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'highRateReverseFlow',
        'name': '密集采集(5分钟)逆流量',
        'length': None,
        'de_plug': [{'code': 'list_to_str', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'highRateFlow',
        'name': '密集采集(5分钟)正流量',
        'length': None,
        'de_plug': [{'code': 'list_to_str', 'params': ['srg_data'], 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'dailyReverseFlow',
        'name': '日结累计逆流值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'dailyFlow',
        'name': '日结累计正流量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'currentFlow',
        'name': '实时流速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'csq',
        'name': '信号质量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'cc',
        'name': '覆盖等级',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'unitTransAlarm',
        'name': 'unitTransAlarm',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'tamperingAlarm',
        'name': '篡改报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'storeErrorAlarm',
        'name': '存储错误报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'separateAlarm',
        'name': '分离报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': 'sensorAlarm',
        'name': '传感器报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'reverseFlowAlarm',
        'name': '逆流报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'reverseERFlowAlarm',
        'name': 'reverseERFlowAlarm',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'mialarm',
        'name': '磁干扰告警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'lowWaterPressure',
        'name': '低水压力报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'lowTemperatureAlarm',
        'name': '低温报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'lowFlowAlarm',
        'name': '低流量报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': 'lowERBatteryAlarm',
        'name': 'lowERBatteryAlarm',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0044': {
        'code': 'lowBatteryAlarm',
        'name': '低电量告警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': 'highWaterPressure',
        'name': '高水压报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': 'highWaterFlowAlarm',
        'name': '高水流量报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': 'highTemperatureAlarm',
        'name': '高温报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': 'highInnerTemperatureAlarm',
        'name': '表内高温报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': 'highFlowAlarm',
        'name': '持续高流量告警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0050': {
        'code': 'emptyAlarm',
        'name': '空警报',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': 'dataStorageAlarm',
        'name': '数据存储报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': 'codeCheckAlarm',
        'name': '代码检查报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': 'adErrorAlarm',
        'name': '地址错误报警',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    'Battery': {
        'name': '电池信息',
        'type': '上行',
        'default': [],
        'element': ['0001', '0002'],
        'type_dict': {}
    },
    'Meter': {
        'name': '表计信息',
        'type': '上行',
        'default': [],
        'element': ['0003', '0005', '0012', '0013'],
        'type_dict': {}
    },
    'WaterMeter': {
        'name': '水表信息',
        'type': '上行',
        'default': [],
        'element': ['0014', '0015', '0017', '0019', '0020', '0023', '0024', '0025',
                    '0026', '0027', '0028', '0029', '0030', '0031'],
        'type_dict': {}
    },
    'WaterMeterAlarm': {
        'name': '报警信息',
        'type': '上行',
        'default': [],
        'element': ['0032', '0033', '0034', '0035', '0036', '0037', '0038', '0039', '0040', '0041', '0042', '0043',
                    '0044', '0045', '0046', '0047', '0048', '0049', '0050', '0051', '0052', '0053'],
        'type_dict': {}
    },
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {

}

# 入库的命令列表
IS_SAVE_LIST = ['Battery', 'Meter', 'WaterMeter', 'WaterMeterAlarm']

# 配置的CLASS
__CLASS__ = 'CtwingNingBoSettingInfo'


class CtwingNingBoSettingInfo(object):
    """
    获取 天翼使能平台迈拓水表配置信息
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
