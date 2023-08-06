# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2021/03/18

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    'appid': {
        'code': 'appid',
        'name': 'E生态应用ID',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'secret': {
        'code': 'secret',
        'name': 'E生态应用秘钥',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'message': {
        'code': 'message',
        'name': '响应结果',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'token': {
        'code': 'token',
        'name': '授权码',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'expires': {
        'code': 'expires',
        'name': '失效时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'sn': {
        'code': 'sn',
        'name': '设备序列号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'collect_time': {
        'code': 'collect_time',
        'name': '采集时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'timestamp': {
        'code': 'timestamp',
        'name': '时间戳',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'datetime': {
        'code': 'datetime',
        'name': '时间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'lng': {
        'code': 'lng',
        'name': '经度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'lat': {
        'code': 'lat',
        'name': '纬度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_34': {
        'code': 'temperature',
        'name': '土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_36': {
        'code': 'relativeHumidity',
        'name': '相对湿度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_37': {
        'code': 'dewPoint',
        'name': '露点',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_38': {
        'code': 'atmosphericPressure',
        'name': '大气压力',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_40': {
        'code': 'maxWindSpeed',
        'name': '最大风速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_41': {
        'code': 'averageWindSpeed',
        'name': '风速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_42': {
        'code': 'windDirection',
        'name': '风向',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_44': {
        'code': 'rainfall',
        'name': '雨量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_45': {
        'code': 'solarRadiationIntensity',
        'name': '当前太阳辐射强度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_46': {
        'code': 'solarRadiationAmount',
        'name': '累积太阳辐射量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_50': {
        'code': 'battery',
        'name': '电池电量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_54': {
        'code': 'outsideVoltage',
        'name': '外部输入电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_55': {
        'code': 'accX',
        'name': '三轴-X',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_56': {
        'code': 'accY',
        'name': '三轴-Y',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_57': {
        'code': 'accZ',
        'name': '三轴-Z',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_60': {
        'code': 'rssi',
        'name': 'RSSi信号值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_63': {
        'code': 'gsmLac',
        'name': 'GSM LAC',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_64': {
        'code': 'gsmCellId',
        'name': 'GSM基站ID',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_71': {
        'code': 'tcpConnectErrCount',
        'name': 'TCP连接错误次数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_92': {
        'code': 'airTemperature',
        'name': '气温',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '地表_104': {
        'code': 'rainDaily',
        'name': '日累积雨量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10cm_34': {
        'code': '10cm_temperature',
        'name': '10厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '10cm_82': {
        'code': '10cm_moisture',
        'name': '10厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '20cm_34': {
        'code': '20cm_temperature',
        'name': '20厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '20cm_82': {
        'code': '20cm_moisture',
        'name': '20厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30cm_34': {
        'code': '30cm_temperature',
        'name': '30厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '30cm_82': {
        'code': '30cm_moisture',
        'name': '30厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '40cm_34': {
        'code': '40cm_temperature',
        'name': '40厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '40cm_82': {
        'code': '40cm_moisture',
        'name': '40厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '50cm_34': {
        'code': '50cm_temperature',
        'name': '50厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '50cm_82': {
        'code': '50cm_moisture',
        'name': '50厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '60cm_34': {
        'code': '60cm_temperature',
        'name': '60厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '60cm_82': {
        'code': '60cm_moisture',
        'name': '60厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '70cm_34': {
        'code': '70cm_temperature',
        'name': '70厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '70cm_82': {
        'code': '70cm_moisture',
        'name': '70厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '80cm_34': {
        'code': '80cm_temperature',
        'name': '80厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '80cm_82': {
        'code': '80cm_moisture',
        'name': '80厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '90cm_34': {
        'code': '90cm_temperature',
        'name': '90厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '90cm_82': {
        'code': '90cm_moisture',
        'name': '90厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '100cm_34': {
        'code': '100cm_temperature',
        'name': '100厘米土壤温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '100cm_82': {
        'code': '100cm_moisture',
        'name': '100厘米水分含量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    'PUSH_REPORT': {
        'name': '推送上报',
        'type': '上行',
        'default': [],
        'element': ['地表_92', '地表_34', '地表_36', '地表_40', '地表_41', '地表_42', '地表_44', '地表_104', '地表_38', '地表_37',
                    '地表_45',  '地表_46', '地表_50', '地表_54', '地表_55', '地表_56', '地表_57', '地表_60', '地表_63', '地表_64',
                    '地表_71',  '10cm_34', '10cm_82', '20cm_34', '20cm_82', '30cm_34', '30cm_82', '40cm_34', '40cm_82', '50cm_34',
                    '50cm_82', '60cm_34', '60cm_82', '70cm_34', '70cm_82', '80cm_34', '80cm_82', '90cm_34', '90cm_82', '100cm_34',
                    '100cm_82'],
        'type_dict': {}
    },
    'GET_TOKEN': {
        'name': '获取接口验证码',
        'type': '响应',
        'default': ['message', 'token', 'expires'],
        'element': [],
        'type_dict': {}
    },
    'GET_MOMENT_DATA': {
        'name': '获取指定时间数据',
        'type': '响应',
        'default': ['message', 'timestamp', 'datetime'],
        'element': ['地表_92', '地表_34', '地表_36', '地表_40', '地表_41', '地表_42', '地表_44', '地表_104', '地表_38', '地表_37',
                    '地表_45',  '地表_46', '地表_50', '地表_54', '地表_55', '地表_56', '地表_57', '地表_60', '地表_63', '地表_64',
                    '地表_71',  '10cm_34', '10cm_82', '20cm_34', '20cm_82', '30cm_34', '30cm_82', '40cm_34', '40cm_82', '50cm_34',
                    '50cm_82', '60cm_34', '60cm_82', '70cm_34', '70cm_82', '80cm_34', '80cm_82', '90cm_34', '90cm_82', '100cm_34',
                    '100cm_82'],
        'type_dict': {}
    },
    'GET_LATEST_DATA': {
        'name': '获取最新一包数据',
        'type': '响应',
        'default': ['message', 'timestamp', 'datetime', 'lng', 'lat'],
        'element': ['地表_92', '地表_34', '地表_36', '地表_40', '地表_41', '地表_42', '地表_44', '地表_104', '地表_38', '地表_37',
                    '地表_45',  '地表_46', '地表_50', '地表_54', '地表_55', '地表_56', '地表_57', '地表_60', '地表_63', '地表_64',
                    '地表_71',  '10cm_34', '10cm_82', '20cm_34', '20cm_82', '30cm_34', '30cm_82', '40cm_34', '40cm_82', '50cm_34',
                    '50cm_82', '60cm_34', '60cm_82', '70cm_34', '70cm_82', '80cm_34', '80cm_82', '90cm_34', '90cm_82', '100cm_34',
                    '100cm_82'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    'GET_TOKEN': {
        'name': '获取接口验证码',
        'type': '上行',
        'default': [],
        'element': ['appid', 'secret'],
        'type_dict': {}
    },
    'GET_MOMENT_DATA': {
        'name': '获取指定时间数据',
        'type': '上行',
        'default': [],
        'element': ['token', 'sn', 'datetime'],
        'type_dict': {}
    },
    'GET_LATEST_DATA': {
        'name': '获取最新一包数据',
        'type': '上行',
        'default': [],
        'element': ['token', 'sn'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['PUSH_REPORT']

# 配置的CLASS
__CLASS__ = 'EcoisSettingInfo'


class EcoisSettingInfo(object):
    """
    获取 E生态配置信息
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

    def get_code_key_dict(self):
        """
        获取 编码-键 字典
        :return:
        """
        return {v['code']: k for k, v in self.__element_dict.items()}


if __name__ == '__main__':
    pass
