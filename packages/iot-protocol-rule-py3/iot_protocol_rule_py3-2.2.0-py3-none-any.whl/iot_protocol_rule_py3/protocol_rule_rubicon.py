# -*- coding: utf-8 -*-
"""
File Name  config_rubicon
Created on 2019/01/10

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'BATT_COS',
        'name': u'电池电压状态改变',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'BURST_COUNT',
        'name': u'从RTU所接受到的数据个数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'BURST_GATEPOS_COS',
        'name': u'BURST_GATEPOS_COS',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'CAB_TEMP',
        'name': u'基座温度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'COMM_STATUS',
        'name': u'和RTU的通信满意度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'CTRL_MODE',
        'name': u'站点控制模式',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'CTRL_SUSPENDED',
        'name': u'控制暂停',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'DSL_COS',
        'name': u'下流水位状态改变',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'DSL_VAL',
        'name': u'下流水位当前高度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'DSL1_SENS_OOR',
        'name': u'为1表示下游水位传感器检测到一个超过水位传感器测量范围的水位值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'DSS_STATUS',
        'name': u'下流水位状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'FG_CNT',
        'name': u'站点闸门孔数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'FLOW_ACU_TOTAL',
        'name': u'闸门站点自上次重置后的累计水量',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'FLOW_ACU_SR_COS',
        'name': u'站点闸门累计水量上报给数据库的更新区间',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'FLOW_COS',
        'name': u'流速状态改变',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'FLOW_SP',
        'name': u'站点流速设定值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'FLOW_VAL',
        'name': u'经过此站点的当前总流速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'FLOWMETER_COMMS',
        'name': u'为1时表示SlipMeter的流速已经小于低流量中的断值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'FLOWMETER_INSUFFICIENT_SUBMERGENCE',
        'name': u'为1时表示SlipMeter不能正确测量流速',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'LOW_FLOW',
        'name': u'为1时表示SlipMeter的流速已经小于低流量中的断值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'POLL_COUNT',
        'name': u'在抢修初始化后从RTU所接受到的数据个数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'RTU_SITE_ID',
        'name': u'站点唯一ID',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'USL_COS',
        'name': u'上流水位状态改变',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'USL_VAL',
        'name': u'上流水位当前高度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'USL1_SENS_OOR',
        'name': u'为1表示上游水位传感器检测到一个超过水位传感器测量范围的水位值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'USS_STATUS',
        'name': u'上游水位状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'G1_LOC_REM',
        'name': u'闸1本地控制',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'G1_OOS',
        'name': u'为1时表示闸1处以非工作状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'G1_SDB_FAULT',
        'name': u'为1时表示闸1太阳能驱动板失效',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'G1_UL',
        'name': u'为1时表示闸1闸门高度处于上限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'G1_OVTRQ',
        'name': u'为1时表示闸1闸门处于过扭状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'G1_LL',
        'name': u'为1时表示闸1闸门高度处于下限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'G1_COMMISSION',
        'name': u'为1时表示闸1闸门开度已经被正确的设置',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'G1_SERIAL_NO',
        'name': u'闸1序列号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'G1_BATT_VOLT',
        'name': u'闸1电池电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'G1_POS_SP',
        'name': u'闸1从完全关闭状态到所需要的开启位置的开度预定值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'G1_POS_VAL',
        'name': u'闸1从完全关闭状态到当前位置的闸门高度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'G1_MANUAL',
        'name': u'为1时表示闸1处于手动控制状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'G2_LOC_REM',
        'name': u'闸2本地控制',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'G2_OOS',
        'name': u'为1时表示闸2处于非工作状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'G2_SDB_FAULT',
        'name': u'为1时表示闸2太阳能驱动板失效',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'G2_UL',
        'name': u'为1时表示闸2闸门高度处于上限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '043': {
        'code': 'G2_OVTRQ',
        'name': u'为1时表示闸2闸门处于过扭状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'G2_LL',
        'name': u'为1时表示闸2闸门高度处于下限',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'G2_COMMISSION',
        'name': u'为1时表示闸2闸门开度已经被正确的设置',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'G2_SERIAL_NO',
        'name': u'闸2序列号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'G2_BATT_VOLT',
        'name': u'闸2电池电压',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'G2_POS_SP',
        'name': u'闸2从完全关闭状态到所需要的开启位置的开度预定值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '049': {
        'code': 'G2_POS_VAL',
        'name': u'闸2从完全关闭状态到当前位置的闸门高度',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '050': {
        'code': 'G2_MANUAL',
        'name': u'为1时表示闸2处于手动控制状态',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'siteId': {
        'code': 'siteId',
        'name': u'站点编号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'gateNo': {
        'code': 'gateNo',
        'name': u'闸门编号',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'sinceTimeStamp': {
        'code': 'sinceTimeStamp',
        'name': u'时间戳',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'milliSeconds': {
        'code': 'milliSeconds',
        'name': u'毫秒数',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    'setPoint': {
        'code': 'setPoint',
        'name': u'设定值',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'getSiteRegisterList': {
        'name': u'获取指定站点编号处的寄存器响应',
        'type': '应答',
        'default': [],
        'element': [str(index).zfill(3) for index in range(1, 51)],
        'type_dict': {}
    },
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {
    'getSiteList': {
        'name': u'获取闸门站点列表上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'getSiteGateCount': {
        'name': u'获取指定站点编号处的闸门数量上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getSiteType': {
        'name': u'获取指定站点编号处的闸门类型上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getSystemRegisterList': {
        'name': u'获取所有寄存器上行',
        'type': '上行',
        'default': [],
        'element': ['sinceTimeStamp'],
        'type_dict': {}
    },
    'getSiteRegisterList': {
        'name': u'获取指定站点编号处的寄存器上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'sinceTimeStamp'],
        'type_dict': {}
    },
    'getGateRegisterList': {
        'name': u'获取指定站点编号处的指定闸门编号处的寄存器上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo', 'sinceTimeStamp'],
        'type_dict': {}
    },
    'getControlMode': {
        'name': u'获取指定站点编号处的控制模式上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getFlow': {
        'name': u'获取指定站点编号处的流量上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getFlowSetpoint': {
        'name': u'获取指定站点编号处的流量设定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getUpstreamWaterLevel': {
        'name': u'获取指定站点编号处的上流水位上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getDownstreamWaterLevel': {
        'name': u'获取指定站点编号处的下流水位上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getVolume': {
        'name': u'获取指定站点编号处的体积上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getCommunicationStatus': {
        'name': u'获取指定站点编号处的通信状态上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getGatePositionSetpoint': {
        'name': u'获取指定站点阀门编号的位置设定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo'],
        'type_dict': {}
    },
    'getGatePosition': {
        'name': u'获取指定站点编号处的指定闸门编号处的闸门位置上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo'],
        'type_dict': {}
    },
    'getFlowCOS': {
        'name': u'获取指定站点编号处的流量预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getUpstreamLevelCOS': {
        'name': u'获取指定站点编号处的上流水位预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getDownstreamLevelCOS': {
        'name': u'获取指定站点编号处的下流水位预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getVolumeCOS': {
        'name': u'获取指定站点编号处的体积预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getBatteryCOS': {
        'name': u'获取指定站点编号处的电池预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getGatePositionCOS': {
        'name': u'获取指定站点编号处的闸门位置预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'getGateAutoStatus': {
        'name': u'获取指定站点阀门编号的自动状态上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo'],
        'type_dict': {}
    },
    'getAPIStatus': {
        'name': u'获取API状态上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'APISetpointWriteFrequncyError': {
        'name': u'获取API设定值写入频率错误上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    'setFlowControlMode': {
        'name': u'设置指定站点编号处的流量控制模式上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'setPositionControlMode': {
        'name': u'设置指定站点编号处的位置控制模式上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'setFlowSetpoint': {
        'name': u'设置指定站点编号处的流量设定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'setPoint'],
        'type_dict': {}
    },
    'setGatePositionSetpoint': {
        'name': u'设置指定站点编号处的指定闸门编号处的闸门位置设定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo', 'setPoint'],
        'type_dict': {}
    },
    'setGateAuto': {
        'name': u'设置指定站点编号处的指定闸门编号处为自动状态上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo'],
        'type_dict': {}
    },
    'setGateManual': {
        'name': u'设置指定站点编号处的指定闸门编号处为手动状态上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'gateNo'],
        'type_dict': {}
    },
    'setResetLevelSensors': {
        'name': u'设置重置水位传感器上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'setTime': {
        'name': u'设置设置指定站点编号处的时间上行',
        'type': '上行',
        'default': [],
        'element': ['siteId'],
        'type_dict': {}
    },
    'setFlowCOS': {
        'name': u'设置指定站点编号处的流量预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'setPoint'],
        'type_dict': {}
    },
    'setUpstreamLevelCOS': {
        'name': u'设置指定站点编号处的上流水位预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'setPoint'],
        'type_dict': {}
    },
    'setDownstreamLevelCOS': {
        'name': u'设置指定站点编号处的下流水位预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'setPoint'],
        'type_dict': {}
    },
    'setVolumeCOS': {
        'name': u'设置指定站点编号处的体积预定值上行',
        'type': '上行',
        'default': [],
        'element': ['siteId', 'setPoint'],
        'type_dict': {}
    },
    'setApiTimeout': {
        'name': u'设置API请求过期时间上行',
        'type': '上行',
        'default': [],
        'element': ['milliSeconds'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['getSiteRegisterList']

# 配置的CLASS
__CLASS__ = 'RubiconSettingInfo'


class RubiconSettingInfo(object):
    """
    获取RUBICON配置信息
    """

    def __init__(self):
        """
        配置信息初始化
        """
        self.__element_dict = ELEMENT_DICT
        self.__device_2_platform = DEVICE_2_PLATFORM
        self.__platform_2_device = PLATFORM_2_DEVICE
        self.__element_list = [ELEMENT_DICT[str(index).zfill(3)]['code'] for index in range(1, 51)]
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
    setting = RubiconSettingInfo()
    print(setting.get_element_list())
