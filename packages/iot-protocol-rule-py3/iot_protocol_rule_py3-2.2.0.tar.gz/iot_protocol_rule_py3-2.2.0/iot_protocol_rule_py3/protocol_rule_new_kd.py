# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019年8月19日

@author: like

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'SW_VER',
        'name': u'软件版本',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'SITE_ID',
        'name': u'客户编号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'CUSTOMER_NO',
        'name': u'站点标示',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'MOTOR_CURRENT_MAX',
        'name': u'电机电流最大值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'MOTOR_CURRENT_VAL',
        'name': u'当前电机电流值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'MOTOR_CURRENT_ALARM',
        'name': u'过载报警信号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'CTRL_MODE_SP',
        'name': u'控制模式设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'CTRL_MODE_VAL',
        'name': u'控制模式当前值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'GPOS_OPEN_MAX',
        'name': u'闸门最大开度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'GPOS_OPEN_VAL',
        'name': u'闸门当前开度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'GPOS_OPEN_SP',
        'name': u'闸门开度设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'UWL_VAL',
        'name': u'当前上游水位',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'UWL_CTRL_SECS',
        'name': u'上游水位采样时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'FLOW_VAL',
        'name': u'当前瞬时流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'FLOW_VOL',
        'name': u'当前累计流量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'FLOW_CTRL_SECS',
        'name': u'当前累计流量采样时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'DWL_VAL',
        'name': u'当前下游水位',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'DWL_CTRL_SECS',
        'name': u'下游水位采样时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'SOLAR_ARRAY_VOLTAGE',
        'name': u'阵列电压(太阳能板)',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'BATTERY_VOLTAGE',
        'name': u'电池电压',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'LOAD_VOLTAGE',
        'name': u'负载电压',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'UNDERVOLTAGE_ALARM',
        'name': u'欠压告警信号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'CABINET_TEMPERATURE',
        'name': u'控制柜温度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'HTEMP_ALARM',
        'name': u'高温报警信号',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'UWL_OVERLIMIT_ALARM',
        'name': u'上游水位超限报警',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'DWL_OVERLIMIT_ALARM',
        'name': u'下游水位超限报警',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'WATER_SENSOR',
        'name': u'水位传感器异常报警',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'POSITION_SENSOR',
        'name': u'位置传感异常报警',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'SOLAR_SENSOR',
        'name': u'太阳能传感异常报警',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'CONTROL_MODE',
        'name': u'本地/远程控制',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'FLOW_SP',
        'name': u'流量模式设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'SILL_ELEV',
        'name': u'闸门下沿距离地面高度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'GPOS_WIDTH',
        'name': u'闸门宽度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'GPOS_CLOSE_CRUSH_TIME',
        'name': u'闸门关闭时间',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'GPOS_ELEV_VAL',
        'name': u'闸门高度',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'GPOS_ELEV_SP',
        'name': u'闸门高度设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'UWL_SP',
        'name': u'上游水位设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'UWL_CTRL_KP',
        'name': u'上游水位PID的P值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'UWL_CTRL_KI',
        'name': u'上游水位PID的I值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'UWL_CTRL_KI',
        'name': u'上游水位PID的D值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'UWL_CTRL_FLOW_MIN',
        'name': u'上游水位最小水位设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'UWL_CTRL_FLOW_MAX',
        'name': u'上游水位最大水位设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '043': {
        'code': 'UWL_RAW_VAL',
        'name': u'上游水位水位原始值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'UWL_RAW_GAIN',
        'name': u'上游水位水位计算系数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'UWL_RAW_ADJUST',
        'name': u'上游水位水位测量参照值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'FLOW_DB',
        'name': u'当前流量控制值百分制',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'DWL_SP',
        'name': u'下游水位设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'DWL_CTRL_KP',
        'name': u'下游水位PID的P值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '049': {
        'code': 'DWL_CTRL_KI',
        'name': u'下游水位PID的I值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '050': {
        'code': 'DWL_CTRL_KD',
        'name': u'下游水位PID的D值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '051': {
        'code': 'DWL_CTRL_FLOW_MIN',
        'name': u'下游水位最小水位设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '052': {
        'code': 'DWL_CTRL_FLOW_MAX',
        'name': u'下游水位最大水位设定值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '053': {
        'code': 'DWL_RAW_VAL',
        'name': u'下游水位最大水位原始值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '054': {
        'code': 'DWL_RAW_GAIN',
        'name': u'下游水位计算系数',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '055': {
        'code': 'DWL_RAW_ADJUST',
        'name': u'下游水位水位测量参照值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '056': {
        'code': 'BATTERY_CHARGE_CURRENT',
        'name': u'阵列电流',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '057': {
        'code': 'BATTERY_CHARGE_CURRENT_TODA',
        'name': u'日累计充电量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '058': {
        'code': 'BATTERY_DRAIN_CURRENT',
        'name': u'负载电流',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '059': {
        'code': 'BATTERY_DRAIN_CURRENT_TODAY',
        'name': u'日累计放电量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '060': {
        'code': 'BATTERY_LEVEL',
        'name': u'电池剩余电量',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'assetId': {
        'code': 'assetId',
        'name': u'闸门id',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'varName': {
        'code': 'varName',
        'name': u'控制模式',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'setValue': {
        'code': 'setValue',
        'name': u'目标值',
        'length': '',
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'getData': {
        'name': u'获取数据请求响应',
        'type': '应答',
        'default': [],
        'element': [str(index).zfill(3) for index in range(1, 61)],
        'type_dict': {}
    }
}
# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'getData': {
        'name': u'获取数据请求上行',
        'type': '上行',
        'default': [],
        'element': ['assetId'],
        'type_dict': {}
    },
    'setData': {
        'name': u'设置数据请求上行',
        'type': '上行',
        'default': [],
        'element': ['assetId', 'varName', 'setValue'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['getData']

# 配置的CLASS
__CLASS__ = 'NEWKDSettingInfo'


class NEWKDSettingInfo(object):
    """
    获取新科鼎配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__element_list = [ELEMENT_DICT[str(index).zfill(3)]['code'] for index in range(1, 61)]
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
        :param protocol:
        :return:
        """
        if command in self.__platform_2_device.keys():
            return [self.__element_dict[item] for item in self.__platform_2_device[command]['element']]
        else:
            return []


if __name__ == '__main__':
    setting = NEWKDSettingInfo()
    print(setting.get_element_list())
