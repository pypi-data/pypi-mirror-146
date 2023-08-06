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
    'variant_value_0': {
        'code': 'variant_value_0',
        'name': u'变量_0',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_1': {
        'code': 'variant_value_1',
        'name': u'变量_1',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_2': {
        'code': 'variant_value_2',
        'name': u'变量_2',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_3': {
        'code': 'variant_value_3',
        'name': u'变量_3',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_4': {
        'code': 'variant_value_4',
        'name': u'变量_4',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_5': {
        'code': 'variant_value_5',
        'name': u'变量_5',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_6': {
        'code': 'variant_value_6',
        'name': u'变量_6',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_7': {
        'code': 'variant_value_7',
        'name': u'变量_7',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_8': {
        'code': 'variant_value_8',
        'name': u'变量_8',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_9': {
        'code': 'variant_value_9',
        'name': u'变量_9',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_10': {
        'code': 'variant_value_10',
        'name': u'变量_10',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_11': {
        'code': 'variant_value_11',
        'name': u'变量_11',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_12': {
        'code': 'variant_value_12',
        'name': u'变量_12',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_13': {
        'code': 'variant_value_13',
        'name': u'变量_13',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_14': {
        'code': 'variant_value_14',
        'name': u'变量_14',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_15': {
        'code': 'variant_value_15',
        'name': u'变量_15',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_16': {
        'code': 'variant_value_16',
        'name': u'变量_16',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_17': {
        'code': 'variant_value_17',
        'name': u'变量_17',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_18': {
        'code': 'variant_value_18',
        'name': u'变量_18',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_19': {
        'code': 'variant_value_19',
        'name': u'变量_19',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_20': {
        'code': 'variant_value_20',
        'name': u'变量_20',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_21': {
        'code': 'variant_value_21',
        'name': u'变量_21',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_22': {
        'code': 'variant_value_22',
        'name': u'变量_22',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_23': {
        'code': 'variant_value_23',
        'name': u'变量_23',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_24': {
        'code': 'variant_value_24',
        'name': u'变量_24',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_25': {
        'code': 'variant_value_25',
        'name': u'变量_25',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_26': {
        'code': 'variant_value_26',
        'name': u'变量_26',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_27': {
        'code': 'variant_value_27',
        'name': u'变量_27',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_28': {
        'code': 'variant_value_28',
        'name': u'变量_28',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_29': {
        'code': 'variant_value_29',
        'name': u'变量_29',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_30': {
        'code': 'variant_value_30',
        'name': u'变量_30',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_31': {
        'code': 'variant_value_31',
        'name': u'变量_31',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_32': {
        'code': 'variant_value_32',
        'name': u'变量_32',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_33': {
        'code': 'variant_value_33',
        'name': u'变量_33',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_34': {
        'code': 'variant_value_34',
        'name': u'变量_34',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_35': {
        'code': 'variant_value_35',
        'name': u'变量_35',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_36': {
        'code': 'variant_value_36',
        'name': u'变量_36',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_37': {
        'code': 'variant_value_37',
        'name': u'变量_37',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_38': {
        'code': 'variant_value_38',
        'name': u'变量_38',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_39': {
        'code': 'variant_value_39',
        'name': u'变量_39',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_40': {
        'code': 'variant_value_40',
        'name': u'变量_40',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_41': {
        'code': 'variant_value_41',
        'name': u'变量_41',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_42': {
        'code': 'variant_value_42',
        'name': u'变量_42',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_43': {
        'code': 'variant_value_43',
        'name': u'变量_43',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_44': {
        'code': 'variant_value_44',
        'name': u'变量_44',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_45': {
        'code': 'variant_value_45',
        'name': u'变量_45',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_46': {
        'code': 'variant_value_46',
        'name': u'变量_46',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_47': {
        'code': 'variant_value_47',
        'name': u'变量_47',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_48': {
        'code': 'variant_value_48',
        'name': u'变量_48',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_49': {
        'code': 'variant_value_49',
        'name': u'变量_49',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_50': {
        'code': 'variant_value_50',
        'name': u'变量_50',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_51': {
        'code': 'variant_value_51',
        'name': u'变量_51',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_52': {
        'code': 'variant_value_52',
        'name': u'变量_52',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_53': {
        'code': 'variant_value_53',
        'name': u'变量_53',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_54': {
        'code': 'variant_value_54',
        'name': u'变量_54',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_55': {
        'code': 'variant_value_55',
        'name': u'变量_55',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_56': {
        'code': 'variant_value_56',
        'name': u'变量_56',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_57': {
        'code': 'variant_value_57',
        'name': u'变量_57',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_58': {
        'code': 'variant_value_58',
        'name': u'变量_58',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variant_value_59': {
        'code': 'variant_value_59',
        'name': u'变量_59',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'uid': {
        'code': 'uid',
        'name': u'用户ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'sid': {
        'code': 'sid',
        'name': u'用户密钥',
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
    'boxId': {
        'code': 'boxId',
        'name': u'BOX的ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variantIds': {
        'code': 'variantIds',
        'name': u'变量ID组合串',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variantId': {
        'code': 'variantId',
        'name': u'变量ID',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'variantVal': {
        'code': 'variantVal',
        'name': u'变量控制值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'realtimeDatas': {
        'name': u'获取变量实时数据响应',
        'type': '应答',
        'default': [],
        'element': ['variant_value_{}'.format(item) for item in range(60)],
        'type_dict': {}
    },
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'initToken': {
        'name': u'获取TOKEN上行',
        'type': '上行',
        'default': [],
        'element': ['uid', 'sid'],
        'type_dict': {}
    },
    'boxVariants': {
        'name': u'获取变量列表上行',
        'type': '上行',
        'default': [],
        'element': ['token'],
        'type_dict': {}
    },
    'realtimeDatas': {
        'name': u'获取变量实时数据上行',
        'type': '上行',
        'default': [],
        'element': ['token', 'variantIds'],
        'type_dict': {}
    },
    'setVariantValue': {
        'name': u'控制变量上行',
        'type': '上行',
        'default': [],
        'element': ['token', 'variantId', 'variantVal'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['realtimeDatas']

# 配置的CLASS
__CLASS__ = 'MingNewSettingInfo'


class MingNewSettingInfo(object):
    """
    获取明牛协议配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__root_url = 'http://mn.mingnew.com'
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

    def get_platform_2_device_protocol_dict(self, command):
        """
        获取平台至设备协议字典
        :param protocol:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
        else:
            return []

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

    def get_signature(self, uid, sid, random, timestamp):
        """
        获取签名
        :param uid:
        :param sid:
        :param random:
        :param timestamp:
        :return:
        """
        m = hashlib.md5()
        m.update(uid + sid + random + timestamp)
        return m.hexdigest().upper()


if __name__ == '__main__':
    setting_info = MingNewSettingInfo()
    uid = 'df19d6b987f6424089b3ad70a4a6b318'
    sid = '6f676ae32d624d5a890995ee8d119a73'
    random = setting_info.get_random()
    timestamp = setting_info.get_timestamp()
    signature = setting_info.get_signature(uid, sid, random, timestamp)

    print(uid)
    print(sid)
    print(random)
    print(timestamp)
    print(signature)
