# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2019/07/05

@author: gw
"""

# 元素列表
ELEMENT_DICT = {
    '001': {
        'code': 'user_card_number',
        'name': '用户卡号',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '002': {
        'code': 'recharge_count',
        'name': '充值次数',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '003': {
        'code': 'door_valve_flag',
        'name': '进出门开关阀标志',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_alarm_status', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '004': {
        'code': 'open_in_time',
        'name': '开泵（进门）时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '005': {
        'code': 'close_out_time',
        'name': '关泵（出门）时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '006': {
        'code': 'total_buy_money',
        'name': '总购金额',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '007': {
        'code': 'total_buy_water',
        'name': '总购水量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '008': {
        'code': 'remnant_money',
        'name': '剩余金额',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '009': {
        'code': 'remnant_water',
        'name': '剩余水量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '010': {
        'code': 'current_use_electric',
        'name': '本次用电量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '011': {
        'code': 'current_use_water',
        'name': '本次用水量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '012': {
        'code': 'year_total_use_electric',
        'name': '年累计用电量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '013': {
        'code': 'year_total_use_water',
        'name': '年累计用水量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '014': {
        'code': 'report_time',
        'name': '自报时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '015': {
        'code': 'total_use_water',
        'name': '累计用水量',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '016': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '017': {
        'code': 'alarm_status_1',
        'name': '报警状态_1',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_alarm_status', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '018': {
        'code': 'alarm_status_2',
        'name': '报警状态_2',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_alarm_status', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '019': {
        'code': 'total_use_electric',
        'name': '累计用电量',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '020': {
        'code': 'success_fail_flag',
        'name': '成功失败标志',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '021': {
        'code': 'current_network_recharge_money',
        'name': '本次网络充值金额',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'multiplied_by_100', 'return': ['msg_data']},
                    {'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '022': {
        'code': 'current_network_recharge_water',
        'name': '本次网络充值水量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'multiplied_by_100', 'return': ['msg_data']},
                    {'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '023': {
        'code': 'recharge_time',
        'name': '充值时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '024': {
        'code': 'take_card_time',
        'name': '刷卡取回时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '025': {
        'code': 'upload_time',
        'name': '上传时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '026': {
        'code': 'water_freeze_date_0',
        'name': '水量冻结时间_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '027': {
        'code': 'total_use_water_0',
        'name': '累计用水量_0',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '028': {
        'code': 'total_use_electric_0',
        'name': '累计用电量_0',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '029': {
        'code': 'water_meter_ststus_0',
        'name': '水表状态_0',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '030': {
        'code': 'water_meter_pressure_0',
        'name': '水表压力_0',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '031': {
        'code': 'controller_ststus_0',
        'name': '控制器状态_0',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '032': {
        'code': 'water_freeze_date_1',
        'name': '水量冻结时间_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '033': {
        'code': 'total_use_water_1',
        'name': '累计用水量_1',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '034': {
        'code': 'total_use_electric_1',
        'name': '累计用电量_1',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '035': {
        'code': 'water_meter_ststus_1',
        'name': '水表状态_1',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '036': {
        'code': 'water_meter_pressure_1',
        'name': '水表压力_1',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '037': {
        'code': 'controller_ststus_1',
        'name': '控制器状态_1',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '038': {
        'code': 'water_freeze_date_2',
        'name': '水量冻结时间_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '039': {
        'code': 'total_use_water_2',
        'name': '累计用水量_2',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '040': {
        'code': 'total_use_electric_2',
        'name': '累计用电量_2',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '041': {
        'code': 'water_meter_ststus_2',
        'name': '水表状态_2',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '042': {
        'code': 'water_meter_pressure_2',
        'name': '水表压力_2',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '043': {
        'code': 'controller_ststus_2',
        'name': '控制器状态_2',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '044': {
        'code': 'water_freeze_date_3',
        'name': '水量冻结时间_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '045': {
        'code': 'total_use_water_3',
        'name': '累计用水量_3',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '046': {
        'code': 'total_use_electric_3',
        'name': '累计用电量_3',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '047': {
        'code': 'water_meter_ststus_3',
        'name': '水表状态_3',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '048': {
        'code': 'water_meter_pressure_3',
        'name': '水表压力_3',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '049': {
        'code': 'controller_ststus_3',
        'name': '控制器状态_3',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '050': {
        'code': 'water_freeze_date_4',
        'name': '水量冻结时间_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '051': {
        'code': 'total_use_water_4',
        'name': '累计用水量_4',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '052': {
        'code': 'total_use_electric_4',
        'name': '累计用电量_4',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '053': {
        'code': 'water_meter_ststus_4',
        'name': '水表状态_4',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '054': {
        'code': 'water_meter_pressure_4',
        'name': '水表压力_4',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '055': {
        'code': 'controller_ststus_4',
        'name': '控制器状态_4',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '056': {
        'code': 'water_freeze_date_5',
        'name': '水量冻结时间_5',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '057': {
        'code': 'total_use_water_5',
        'name': '累计用水量_5',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '058': {
        'code': 'total_use_electric_5',
        'name': '累计用电量_5',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '059': {
        'code': 'water_meter_ststus_5',
        'name': '水表状态_5',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '060': {
        'code': 'water_meter_pressure_5',
        'name': '水表压力_5',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '061': {
        'code': 'controller_ststus_5',
        'name': '控制器状态_5',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '062': {
        'code': 'water_freeze_date_6',
        'name': '水量冻结时间_6',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '063': {
        'code': 'total_use_water_6',
        'name': '累计用水量_6',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '064': {
        'code': 'total_use_electric_6',
        'name': '累计用电量_6',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '065': {
        'code': 'water_meter_ststus_6',
        'name': '水表状态_6',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '066': {
        'code': 'water_meter_pressure_6',
        'name': '水表压力_6',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '067': {
        'code': 'controller_ststus_6',
        'name': '控制器状态_6',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '068': {
        'code': 'water_freeze_date_7',
        'name': '水量冻结时间_7',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '069': {
        'code': 'total_use_water_7',
        'name': '累计用水量_7',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '070': {
        'code': 'total_use_electric_7',
        'name': '累计用电量_7',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '071': {
        'code': 'water_meter_ststus_7',
        'name': '水表状态_7',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '072': {
        'code': 'water_meter_pressure_7',
        'name': '水表压力_7',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '073': {
        'code': 'controller_ststus_7',
        'name': '控制器状态_7',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '074': {
        'code': 'water_freeze_date_8',
        'name': '水量冻结时间_8',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '075': {
        'code': 'total_use_water_8',
        'name': '累计用水量_8',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '076': {
        'code': 'total_use_electric_8',
        'name': '累计用电量_8',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '077': {
        'code': 'water_meter_ststus_8',
        'name': '水表状态_8',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '078': {
        'code': 'water_meter_pressure_8',
        'name': '水表压力_8',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '079': {
        'code': 'controller_ststus_8',
        'name': '控制器状态_8',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '080': {
        'code': 'water_freeze_date_9',
        'name': '水量冻结时间_9',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_date_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '081': {
        'code': 'total_use_water_9',
        'name': '累计用水量_9',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '082': {
        'code': 'total_use_electric_9',
        'name': '累计用电量_9',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'water_data_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '083': {
        'code': 'water_meter_ststus_9',
        'name': '水表状态_9',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '084': {
        'code': 'water_meter_pressure_9',
        'name': '水表压力_9',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '085': {
        'code': 'controller_ststus_9',
        'name': '控制器状态_9',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '086': {
        'code': 'user_caed_number_0',
        'name': '用户卡号_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '087': {
        'code': 'start_time_0',
        'name': '开始时间_0',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '088': {
        'code': 'stop_time_0',
        'name': '停止时间_0',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '089': {
        'code': 'amount_used_this_time_0',
        'name': '本次使用金额_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '090': {
        'code': 'remnant_money_0',
        'name': '剩余金额量_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '091': {
        'code': 'current_use_water_0',
        'name': '本次用水量_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '092': {
        'code': 'flag_0',
        'name': '标志_0',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '093': {
        'code': 'annual_water_0',
        'name': '年度用水量_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '094': {
        'code': 'total_buy_money_0',
        'name': '总购金额_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '095': {
        'code': 'total_buy_water_0',
        'name': '总购水量_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '096': {
        'code': 'user_caed_number_1',
        'name': '用户卡号_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '097': {
        'code': 'start_time_1',
        'name': '开始时间_1',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '098': {
        'code': 'stop_time_1',
        'name': '停止时间_1',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '099': {
        'code': 'amount_used_this_time_1',
        'name': '本次使用金额_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '100': {
        'code': 'remnant_money_1',
        'name': '剩余金额量_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '101': {
        'code': 'current_use_water_1',
        'name': '本次用水量_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '102': {
        'code': 'flag_1',
        'name': '标志_1',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '103': {
        'code': 'annual_water_1',
        'name': '年度用水量_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '104': {
        'code': 'total_buy_money_1',
        'name': '总购金额_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '105': {
        'code': 'total_buy_water_1',
        'name': '总购水量_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '106': {
        'code': 'user_caed_number_2',
        'name': '用户卡号_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '107': {
        'code': 'start_time_2',
        'name': '开始时间_2',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '108': {
        'code': 'stop_time_2',
        'name': '停止时间_2',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '109': {
        'code': 'amount_used_this_time_2',
        'name': '本次使用金额_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '110': {
        'code': 'remnant_money_2',
        'name': '剩余金额量_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '111': {
        'code': 'current_use_water_2',
        'name': '本次用水量_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '112': {
        'code': 'flag_2',
        'name': '标志_2',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '113': {
        'code': 'annual_water_2',
        'name': '年度用水量_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '114': {
        'code': 'total_buy_money_2',
        'name': '总购金额_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '115': {
        'code': 'total_buy_water_2',
        'name': '总购水量_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '116': {
        'code': 'user_caed_number_3',
        'name': '用户卡号_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '117': {
        'code': 'start_time_3',
        'name': '开始时间_3',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '118': {
        'code': 'stop_time_3',
        'name': '停止时间_3',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '119': {
        'code': 'amount_used_this_time_3',
        'name': '本次使用金额_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '120': {
        'code': 'remnant_money_3',
        'name': '剩余金额量_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '121': {
        'code': 'current_use_water_3',
        'name': '本次用水量_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '122': {
        'code': 'flag_3',
        'name': '标志_3',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '123': {
        'code': 'annual_water_3',
        'name': '年度用水量_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '124': {
        'code': 'total_buy_money_3',
        'name': '总购金额_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '125': {
        'code': 'total_buy_water_3',
        'name': '总购水量_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '126': {
        'code': 'user_caed_number_4',
        'name': '用户卡号_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '127': {
        'code': 'start_time_4',
        'name': '开始时间_4',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '128': {
        'code': 'stop_time_4',
        'name': '停止时间_4',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '129': {
        'code': 'amount_used_this_time_4',
        'name': '本次使用金额_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '130': {
        'code': 'remnant_money_4',
        'name': '剩余金额量_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '131': {
        'code': 'current_use_water_4',
        'name': '本次用水量_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '132': {
        'code': 'flag_4',
        'name': '标志_4',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '133': {
        'code': 'annual_water_4',
        'name': '年度用水量_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '134': {
        'code': 'total_buy_money_4',
        'name': '总购金额_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '135': {
        'code': 'total_buy_water_4',
        'name': '总购水量_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '136': {
        'code': 'upload_time',
        'name': '上传时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '137': {
        'code': 'year_use_water',
        'name': '年度用水量',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '138': {
        'code': 'year_use_electric',
        'name': '年度用电量',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '139': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '140': {
        'code': 'relay_status',
        'name': '水泵状态',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '141': {
        'code': 'a_phase_voltage',
        'name': '当前A相电压值',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '142': {
        'code': 'b_phase_voltage',
        'name': '当前B相电压值',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '143': {
        'code': 'c_phase_voltage',
        'name': '当前C相电压值',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '144': {
        'code': 'a_phase_current',
        'name': '当前A相电流值',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '145': {
        'code': 'b_phase_current',
        'name': '当前B相电流值',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '146': {
        'code': 'c_phase_current',
        'name': '当前C相电流值',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '147': {
        'code': 'water_meter_address',
        'name': '水表地址',
        'length': 10,
        'de_plug': [{'params': ['srg_data'], 'code': 'convert_high_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '148': {
        'code': 'water_meter_base_number',
        'name': '水表底数',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '149': {
        'code': 'water_meter_status',
        'name': '水表状态',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '150': {
        'code': 'signal_strength',
        'name': '信号强度',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '151': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}, ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '152': {
        'code': 'user_total_use_water',
        'name': '用户总使用水量',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '153': {
        'code': 'electric_meter_base_number',
        'name': '电表底数（总电量）',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '154': {
        'code': 'program_version_number',
        'name': '程序版本号',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '155': {
        'code': 'meter_rate',
        'name': '光电水表倍率',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '156': {
        'code': 'average_coefficient_l',
        'name': '平均水电转换系数L',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '157': {
        'code': 'average_coefficient_h',
        'name': '平均水电转换系数H',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '158': {
        'code': 'temp_coefficient_l',
        'name': '临时水电转换系数L',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '159': {
        'code': 'temp_coefficient_h',
        'name': '临时水电转换系数H',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '160': {
        'code': 'placeholder',
        'name': '占位符',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '161': {
        'code': 'set_flag',
        'name': '设置标志',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '162': {
        'code': 'ip',
        'name': 'IP',
        'length': 8,
        'de_plug': [{'params': ['msg_data'], 'code': 'ip_hex_to_ip', 'return': ['msg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'ip_hex', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '163': {
        'code': 'port',
        'name': 'PORT',
        'length': 4,
        'de_plug': [{'params': ['msg_data'], 'code': 'port_hex_to_port', 'return': ['msg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'port_hex', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '164': {
        'code': 'apn',
        'name': 'APN',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '165': {
        'code': 'ccid',
        'name': 'CCID',
        'length': 20,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '166': {
        'code': 'water_meter_address',
        'name': '水表地址',
        'length': 10,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '167': {
        'code': 'water_meter_base_number',
        'name': '水表底数',
        'length': 6,
        'de_plug': [],
        'en_plug': [{'params': ['msg_data'], 'code': 'convert_high_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '168': {
        'code': 'recharge_count_0',
        'name': '充值次数_0',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '169': {
        'code': 'take_card_flag_0',
        'name': '刷卡取回标志_0',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '170': {
        'code': 'recharge_time_0',
        'name': '充值时间_0',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '171': {
        'code': 'current_network_recharge_money_0',
        'name': '本次网络充值金额_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '172': {
        'code': 'current_network_recharge_water_0',
        'name': '本次网络充值水量_0',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '173': {
        'code': 'take_card_time_0',
        'name': '刷卡取回时间_0',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '174': {
        'code': 'recharge_count_1',
        'name': '充值次数_1',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '175': {
        'code': 'take_card_flag_1',
        'name': '刷卡取回标志_1',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '176': {
        'code': 'recharge_time_1',
        'name': '充值时间_1',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '177': {
        'code': 'current_network_recharge_money_1',
        'name': '本次网络充值金额_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '178': {
        'code': 'current_network_recharge_water_1',
        'name': '本次网络充值水量_1',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '179': {
        'code': 'take_card_time_1',
        'name': '刷卡取回时间_1',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '180': {
        'code': 'recharge_count_2',
        'name': '充值次数_2',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '181': {
        'code': 'take_card_flag_2',
        'name': '刷卡取回标志_2',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '182': {
        'code': 'recharge_time_2',
        'name': '充值时间_2',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '183': {
        'code': 'current_network_recharge_money_2',
        'name': '本次网络充值金额_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '184': {
        'code': 'current_network_recharge_water_2',
        'name': '本次网络充值水量_2',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '185': {
        'code': 'take_card_time_2',
        'name': '刷卡取回时间_2',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '186': {
        'code': 'recharge_count_3',
        'name': '充值次数_3',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '187': {
        'code': 'take_card_flag_3',
        'name': '刷卡取回标志_3',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '188': {
        'code': 'recharge_time_3',
        'name': '充值时间_3',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '189': {
        'code': 'current_network_recharge_money_3',
        'name': '本次网络充值金额_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '190': {
        'code': 'current_network_recharge_water_3',
        'name': '本次网络充值水量_3',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '191': {
        'code': 'take_card_time_3',
        'name': '刷卡取回时间_3',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '192': {
        'code': 'recharge_count_4',
        'name': '充值次数_4',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '193': {
        'code': 'take_card_flag_4',
        'name': '刷卡取回标志_4',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '194': {
        'code': 'recharge_time_4',
        'name': '充值时间_4',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '196': {
        'code': 'current_network_recharge_money_4',
        'name': '本次网络充值金额_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '197': {
        'code': 'current_network_recharge_water_4',
        'name': '本次网络充值水量_4',
        'length': 6,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '198': {
        'code': 'take_card_time_4',
        'name': '刷卡取回时间_4',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '199': {
        'code': 'report_type',
        'name': '自报种类',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '200': {
        'code': 'time_interval',
        'name': '间隔时间',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'convert_high_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'convert_high_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '201': {
        'code': 'area_number',
        'name': '区域号',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '202': {
        'code': 'meter_number',
        'name': '表号',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '203': {
        'code': 'verification_code',
        'name': '加密验证码',
        'length': 4,
        'de_plug': [],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '204': {
        'code': 'recharge_fun_type',
        'name': '充值功能类型',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [{'params': ['msg_data'], 'code': 'int_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '205': {
        'code': 'recharge_time',
        'name': '充值时间',
        'length': 12,
        'de_plug': [],
        'en_plug': [{'params': [], 'code': 'current_time_hex_low', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '206': {
        'code': 'reason',
        'name': '原因',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '207': {
        'code': 'open_valve_time',
        'name': '开阀时间',
        'length': 12,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '208': {
        'code': 'close_valve_time',
        'name': '关阀时间',
        'length': 12,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_time_high', 'return': ['srg_data']}, ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '209': {
        'code': 'this_time_amount',
        'name': '本次使用金额',
        'length': 6,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '210': {
        'code': 'valve_state',
        'name': '阀门状态',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '211': {
        'code': 'this_time_water',
        'name': '本次使用水量',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
            {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '212': {
        'code': 'annual_cumulative_water_used',
        'name': '年度累积用水量',
        'length': 2,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '213': {
        'code': 'flow_cut_off_point1',
        'name': '流量分界点1',
        'length': 6,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '214': {
        'code': 'flow_cut_off_point2',
        'name': '流量分界点2',
        'length': 6,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '215': {
        'code': 'flow_cut_off_point3',
        'name': '流量分界点3',
        'length': 6,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '216': {
        'code': 'flow_cut_off_point4',
        'name': '流量分界点4',
        'length': 6,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '217': {
        'code': 'flow_cut_off_point5',
        'name': '流量分界点5',
        'length': 6,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '218': {
        'code': 'unit_price_cut_off_point1',
        'name': '单价分界点1',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '219': {
        'code': 'unit_price_cut_off_point2',
        'name': '单价分界点2',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '220': {
        'code': 'unit_price_cut_off_point3',
        'name': '单价分界点3',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '221': {
        'code': 'unit_price_cut_off_point4',
        'name': '单价分界点4',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '222': {
        'code': 'unit_price_cut_off_point5',
        'name': '单价分界点5',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '223': {
        'code': 'unit_price_cut_off_point6',
        'name': '单价分界点6',
        'length': 4,
        'de_plug': [
            {'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '224': {
        'code': 'water_meter_pressure',
        'name': '水表压力',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_100', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '225': {
        'code': 'controller_ststus',
        'name': '控制器状态',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'ststus_to_bin', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '226': {
        'code': 'water_meter_DS',
        'name': '表底数DS',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '227': {
        'code': 'instantaneous_flow_SL',
        'name': '瞬时流量SL',
        'length': 8,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '228': {
        'code': 'version_number',
        'name': '版本号',
        'length': 4,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']}, ],
        'msg_data': '',
        'srg_data': ''
    },
    '229': {
        'code': 'battery_voltage',
        'name': '电池电压',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'hex_int_low', 'return': ['srg_data']},
                    {'params': ['srg_data'], 'code': 'divided_by_10', 'return': ['srg_data']}, ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '230': {
        'code': 'terminal_time',
        'name': '终端时间',
        'length': 12,
        'de_plug': [],
        'en_plug': [{'params': ['msg_data'], 'code': 'set_terminal_time', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '231': {
        'code': 'password_and_time_tag',
        'name': '密码和时间标签',
        'length': 14,
        'de_plug': [],
        'en_plug': [{'params': ['msg_data'], 'code': 'set_password_and_time_tag', 'return': ['msg_data']}],
        'msg_data': '',
        'srg_data': ''
    },
    '232': {
        'code': 'switch_pump_label',
        'name': '开关泵标签',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '233': {
        'code': 'pump_state',
        'name': '水泵状态',
        'length': 2,
        'de_plug': [{'params': ['srg_data'], 'code': 'pump_state_transform', 'return': ['srg_data']}],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '234': {
        'code': 'water_meter_pressure',
        'name': '水表压力',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
}

# 平台至设备协议配置
DEVICE_2_PLATFORM = {
    'B4_28': {
        'name': '充值记录自动上报上行',
        'type': '上行',
        'default': [],
        'element': ['086', '168', '169', '170', '171', '172', '173', '096', '174', '175', '176', '177', '178', '179',
                    '106', '180', '181', '182', '183', '184', '185', '116', '186', '187', '188', '189', '190', '191',
                    '126', '192', '193', '194', '196', '197', '198'],
        'type_dict': {}
    },
    'B4_5A': {
        'name': '读取终端GPRS数据中心IP、端口号、APN命令应答',
        'type': '应答',
        'default': [],
        'element': ['162', '163', '164', '165'],
        'type_dict': {}
    },
    'B4_85': {
        'name': '刷卡后1分钟自报上行',
        'type': '上行',
        'default': [],
        'element': ['086', '087', '088', '089', '090', '091', '092', '093', '096', '097', '098', '099', '100', '101',
                    '102', '103', '106', '107', '108', '109', '110', '111', '112', '113', '116', '117', '118', '119',
                    '120', '121', '122', '123', '126', '127', '128', '129', '130', '131', '132', '133'],
        'type_dict': {}
    },
    'B4_87': {
        'name': '网络充值刷进用户卡上报上行',
        'type': '上行',
        'default': [],
        'element': ['001', '020', '002', '021', '022'],
        'type_dict': {}
    },
    'B4_88': {
        'name': '每日12时自报上行',
        'type': '上行',
        'default': [],
        'element': ['025', '026', '027', '028', '029', '030', '031', '032', '033', '034', '035', '036', '037', '038',
                    '039', '040', '041', '042', '043', '044', '045', '046', '047', '048', '049', '050', '051', '052',
                    '053', '054', '055', '056', '057', '058', '059', '060', '061', '062', '063', '064', '065', '066',
                    '067', '068', '069', '070', '071', '072', '073', '074', '075', '076', '077', '078', '079', '080',
                    '081', '082', '083', '084', '085'],
        'type_dict': {}
    },
    'B4_92': {
        'name': '远程启动水泵应答',
        'type': '应答',
        'default': [],
        'element': ['233'],
        'type_dict': {}
    },
    'B4_93': {
        'name': '远程停止水泵应答',
        'type': '应答',
        'default': [],
        'element': ['233'],
        'type_dict': {}
    },
    'B6_80': {
        'name': '水量定时自报上行',
        'type': '上行',
        'default': [],
        'element': ['014', '015', '016', '017', '018'],
        'type_dict': {}
    },
    'B6_81': {
        'name': '随机报警上行',
        'type': '上行',
        'default': [],
        'element': ['017', '018'],
        'type_dict': {}
    },
    'B6_89': {
        'name': '工作上报上行',
        'type': '上行',
        'default': [],
        'element': ['136', '001', '137', '138', '139', '009', '008', '140', '141', '142', '143', '144', '145', '146',
                    '147', '148', '149', '017', '018', '150', '151', '152', '153', '154'],
        'type_dict': {}
    },
    'B4_89': {
        'name': '工作上报上行',
        'type': '上行',
        'default': [],
        'element': ['136', '001', '137', '138', '139', '009', '008', '140', '141', '142', '143', '144', '145', '146',
                    '147', '148', '149', '224', '225', '150', '229', '211'],
        'type_dict': {}
    },
    'B4_8A': {
        'name': '入门开阀数据自报',
        'type': '上行',
        'default': [],
        'element': ['001', '002', '207', '208', '006', '008', '209', '149', '234', '210', '148'],
        'type_dict': {}
    },
    'B4_8B': {
        'name': '出门关阀数据自报',
        'type': '上行',
        'default': [],
        'element': ['001', '002', '207', '208', '006', '008', '209', '149', '234', '210', '211', '137'],
        'type_dict': {}
    },
    'B4_8C': {
        'name': '入门上报五阶六价参数',
        'type': '上行',
        'default': [],
        'element': ['201', '202', '001', '008', '002', '212', '213', '214', '215', '216', '217', '218', '219', '220',
                    '221', '222', '223'],
        'type_dict': {}
    },
    'B6_9C': {
        'name': '控制器半小时上报数据',
        'type': '上行',
        'default': [],
        'element': ['226', '227', '149', '224', '225', '150', '229', '228', '136'],
        'type_dict': {}
    },
}

# 设备至平台协议配置
PLATFORM_2_DEVICE = {
    '34_11': {
        'name': '设置终端时间',
        'type': '上行',
        'default': [],
        'element': ['230', '231'],
        'type_dict': {}
    },
    '34_1A': {
        'name': '设置终端GPRS数据中心IP、端口号、APN命令上行',
        'type': '上行',
        'default': [],
        'element': ['162', '163', '164'],
        'type_dict': {}
    },
    '34_53': {
        'name': '查询终端定时自报种类及间隔时间上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '34_5A': {
        'name': '读取终端GPRS数据中心IP、端口号、APN命令上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '34_66': {
        'name': '查询配对的水表地址及底数上行',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '34_92': {
        'name': '远程启动水泵上行',
        'type': '上行',
        'default': [],
        'element': ['232', '231'],
        'type_dict': {}
    },
    '34_93': {
        'name': '远程停止水泵上行',
        'type': '上行',
        'default': [],
        'element': ['232', '231'],
        'type_dict': {}
    },

}

# 入库的命令列表
IS_SAVE_LIST = ['B4_85', 'B6_81', 'B6_80', 'B4_88', 'B4_87', 'B6_89', 'B4_89']

# 配置的CLASS
__CLASS__ = 'XinTianValveSettingInfo'


class XinTianValveSettingInfo(object):
    """
    获取NewSkyWell协议配置信息
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
    setting_info = XinTianValveSettingInfo()
    print(setting_info.get_platform_2_device_protocol_dict('34_13'))

    print(len(PLATFORM_2_DEVICE))
