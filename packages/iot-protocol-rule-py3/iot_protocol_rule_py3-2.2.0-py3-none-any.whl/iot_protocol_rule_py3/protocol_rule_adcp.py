# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/01/18

@author: gw

"""

# 元素字典
ELEMENT_DICT = {
    '001': {
        'code': 'measure_type',
        'name': '测量类型',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'malfunction_code',
        'name': '故障代码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'measure_count',
        'name': '测量次数',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'run_measure_flow_time',
        'name': '启动测流时间',
        'length': 10,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_ymdHM', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'stop_measure_flow_time',
        'name': '结束测流时间',
        'length': 10,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_ymdHM', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'data_package_identifier',
        'name': '数据包标示符',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'measure_flow_controller_voltage',
        'name': '测流控制器电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'drive_device_voltage',
        'name': '行车设备电压',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'temperature',
        'name': '温度',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'wind_speed',
        'name': '风速',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'wind_direction',
        'name': '风向',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'water_level_1',
        'name': '水位1',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'water_level_2',
        'name': '水位2',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'flow_data_flag',
        'name': '流量数据标志',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'measure_flow_grade',
        'name': '测流等级',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'section_number',
        'name': '断面编号',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'left_water_side_coefficient',
        'name': '左水边系数',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'right_water_side_coefficient',
        'name': '右水边系数',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'buoy_coefficient',
        'name': '浮标系数',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'shoreside_direction',
        'name': '岸边方向',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'flow',
        'name': '流量',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_1000', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'area',
        'name': '面积',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'surface_width',
        'name': '水面宽',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'max_water_depth',
        'name': '最大水深',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'average_water_depth',
        'name': '平均水深',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'average_flow_speed',
        'name': '平均流速',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'max_flow_speed',
        'name': '最大流速',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'measure_speed_vertical_line_total',
        'name': '测速垂线总数',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'data_1_hm',
        'name': '数据1_时分',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_HM', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'data_1_status',
        'name': '数据1_数据状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'data_1_start_point_distance',
        'name': '数据1_起点距',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'data_1_min_flow_speed',
        'name': '数据1_最小流速',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'data_1_max_flow_speed',
        'name': '数据1_最大流速',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'data_1_average_flow_speed',
        'name': '数据1_平均流速',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'data_1_water_level',
        'name': '数据1_水位',
        'length': 8,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'data_1_snr',
        'name': '数据1_信噪比',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_high', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'data_1_is_join_flow_calculate',
        'name': '数据1_是否参与流量计算',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置
DEVICE_2_PLATFORM = {
    'D1': {
        'name': '测流结果主动上报上行',
        'type': '上行',
        'default': [],
        'element': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014',
                    '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028',
                    '029', '030', '031', '032', '033', '034', '035', '036', '037'],
        'type_dict': {}
    }
}

# 平台至设备协议配置
PLATFORM_2_DEVICE = {}

# 入库的命令列表
IS_SAVE_LIST = ['D1']

# 配置的CLASS
__CLASS__ = 'ADCPSettingInfo'


class ADCPSettingInfo(object):
    """
    获取ADCP配置信息
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
        :param protocol:
        :return:
        """
        if command in self.__device_2_platform.keys():
            return [self.__element_dict[item] for item in self.__device_2_platform[command]['element']]
        else:
            return []


if __name__ == '__main__':
    setting_info = ADCPSettingInfo()
    print(setting_info.get_device_2_platform_protocol_dict('D1'))
