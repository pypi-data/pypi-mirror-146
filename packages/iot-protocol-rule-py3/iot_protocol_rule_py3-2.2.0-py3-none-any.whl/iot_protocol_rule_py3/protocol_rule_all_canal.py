# -*- coding: utf-8 -*-
"""
File Name  config
Created on 2018/08/10

@author: gw
"""

# 元素字典
ELEMENT_DICT = {
    '0001': {
        'code': 'result',
        'name': '结果',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0002': {
        'code': 'pw',
        'name': '密码',
        'length': 4,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [
            {'code': 'make_pw', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0003': {
        'code': 'tp',
        'name': '时间标签',
        'length': 12,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []},
            {'code': 'hex_time', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [
            {'code': 'make_tp', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0004': {
        'code': 'software_version',
        'name': '软件版本',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0005': {
        'code': 'hardware_version',
        'name': '硬件版本',
        'length': 4,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0006': {
        'code': 'use_password',
        'name': '使用密码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0007': {
        'code': 'heartbeat',
        'name': '心跳',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0008': {
        'code': 'remote_local_mode',
        'name': '远程/现地模式',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0009': {
        'code': 'motion_state',
        'name': '运动状态',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0010': {
        'code': 'alarm_type',
        'name': '报警类型',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0011': {
        'code': 'alarm_state',
        'name': '报警状态',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0012': {
        'code': 'breakdown_type',
        'name': '故障类型',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0013': {
        'code': 'breakdown_state',
        'name': '故障状态',
        'length': 2,
        'de_plug': [
            {'code': 'update_command', 'params': ['msg_data'], 'return': []}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0014': {
        'code': 'upper_water_level',
        'name': '闸前水位',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0015': {
        'code': 'lower_water_level',
        'name': '闸后水位',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0016': {
        'code': 'gate_site',
        'name': '闸位',
        'length': 10,
        'de_plug': [
            {'code': 'hex_int_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0017': {
        'code': 'instantaneous_speed',
        'name': '瞬时流速',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0018': {
        'code': 'instantaneous_flow',
        'name': '瞬时流量',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0019': {
        'code': 'total_flow',
        'name': '累计流量',
        'length': 10,
        'de_plug': [
            {'code': 'hex_int_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0020': {
        'code': 'fluid_conductance_ratio',
        'name': '流体电导比',
        'length': 10,
        'de_plug': [
            {'code': 'hex_int_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0021': {
        'code': 'osmotic_water_pressure',
        'name': '渗透水压力',
        'length': 10,
        'de_plug': [
            {'code': 'hex_int_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0022': {
        'code': 'weight',
        'name': '荷重',
        'length': 10,
        'de_plug': [
            {'code': 'hex_int_low', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0023': {
        'code': 'temperature',
        'name': '温度',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0024': {
        'code': 'a_phase_voltage',
        'name': 'A项电压',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0025': {
        'code': 'b_phase_voltage',
        'name': 'B项电压',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0026': {
        'code': 'c_phase_voltage',
        'name': 'C项电压',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0027': {
        'code': 'a_phase_current',
        'name': 'A项电流',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0028': {
        'code': 'b_phase_current',
        'name': 'B项电流',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0029': {
        'code': 'c_phase_current',
        'name': 'C项电流',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0030': {
        'code': 'solar_panel_voltage',
        'name': '太阳能板电压',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0031': {
        'code': 'solar_panel_current',
        'name': '太阳能板电流',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0032': {
        'code': 'storage_battery_voltage',
        'name': '蓄电池电压',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0033': {
        'code': 'storage_battery_current',
        'name': '蓄电池电流',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0034': {
        'code': 'storage_battery_surplus_electric_quantity',
        'name': '蓄电池剩余电量',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0035': {
        'code': 'wife_signal_strength',
        'name': '无线信号强度',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0036': {
        'code': '4g_card_surplus_flow',
        'name': '4G卡剩余流量',
        'length': 6,
        'de_plug': [
            {'code': 'hex_int_high', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0037': {
        'code': 'terminal_address',
        'name': '终端地址',
        'length': 20,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0038': {
        'code': 'terminal_clock',
        'name': '终端时钟',
        'length': 12,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_terminal_clock', 'params': [], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0039': {
        'code': 'service_report_cycle',
        'name': '业务上报周期',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['srg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0040': {
        'code': 'work_report_cycle',
        'name': '工况上报周期',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['srg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0041': {
        'code': 'report_center',
        'name': '上报中心',
        'length': 12,
        'de_plug': [],
        'en_plug': [
            {'code': 'ip_port_hex', 'params': ['srg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0042': {
        'code': 'mode_swap_command_code',
        'name': '模式切换命令码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0043': {
        'code': 'command_control_code',
        'name': '命令控制码',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0044': {
        'code': 'set_value',
        'name': '设定值',
        'length': 8,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0045': {
        'code': 'upgrade_program_id',
        'name': '升级程序ID',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0046': {
        'code': 'upgrade_package_split_size',
        'name': '升级程序分割大小',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0047': {
        'code': 'upgrade_package_split_count',
        'name': '升级程序分割数量',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0048': {
        'code': 'current_package_index',
        'name': '当前包序号',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0049': {
        'code': 'current_package_size',
        'name': '当前包大小',
        'length': 4,
        'de_plug': [],
        'en_plug': [
            {'code': 'int_hex_high', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0050': {
        'code': 'current_package_data',
        'name': '升级数据',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0051': {
        'code': 'error_type',
        'name': '错误类型',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0052': {
        'code': 'start_time',
        'name': '开始时间',
        'length': 12,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_time', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0053': {
        'code': 'end_time',
        'name': '结束时间',
        'length': 12,
        'de_plug': [],
        'en_plug': [
            {'code': 'make_time', 'params': ['msg_data'], 'return': ['msg_data']}
        ],
        'msg_data': '',
        'srg_data': ''
    },
    '0054': {
        'code': 'end_flg',
        'name': '结束标识',
        'length': 2,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0055': {
        'code': 'subpackage_no',
        'name': '分包序号',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0056': {
        'code': 'data_count',
        'name': '数据条数',
        'length': 4,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0057': {
        'code': 'data_package',
        'name': '数据包',
        'length': None,
        'de_plug': [],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0058': {
        'code': 'water_level_1',
        'name': '水位1',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    },
    '0059': {
        'code': 'water_level_2',
        'name': '水位2',
        'length': 10,
        'de_plug': [
            {'code': 'hex_decimal', 'params': ['srg_data'], 'return': ['srg_data']}
        ],
        'en_plug': [],
        'msg_data': '',
        'srg_data': ''
    }
}

# 设备至平台协议配置，包括设备主动上报以及对平台的响应
DEVICE_2_PLATFORM = {
    '00': {
        'name': '通讯信息_注册',
        'type': '上行',
        'default': [],
        'element': ['0004', '0005', '0006', '0002', '0003'],
        'type_dict': {}
    },
    '01': {
        'name': '通讯信息_心跳',
        'type': '上行',
        'default': [],
        'element': ['0007', '0002', '0003'],
        'type_dict': {}
    },
    '10': {
        'name': '状态信息_远程/现地模式',
        'type': '上行',
        'default': [],
        'element': ['0008', '0002', '0003'],
        'type_dict': {}
    },
    '11': {
        'name': '状态信息_运动状态',
        'type': '上行',
        'default': [],
        'element': ['0009', '0016', '0002', '0003'],
        'type_dict': {}
    },
    '20': {
        'name': '报警故障_设备报警',
        'type': '上行',
        'default': [],
        'element': ['0010', '0011', '0002', '0003'],
        'type_dict': {}
    },
    '21': {
        'name': '报警故障_设备故障',
        'type': '上行',
        'default': [],
        'element': ['0012', '0013', '0002', '0003'],
        'type_dict': {}
    },
    '30': {
        'name': '综合数据_业务数据',
        'type': '上行',
        'default': [],
        'element': ['0014', '0015', '0016', '0017', '0018', '0019', '0020', '0021', '0022', '0023', '0008', '0009',
                    '0002', '0003'],
        'type_dict': {}
    },
    '31': {
        'name': '综合数据_工况数据',
        'type': '上行',
        'default': [],
        'element': ['0024', '0025', '0026', '0027', '0028', '0029', '0030', '0031', '0032', '0033', '0034', '0035',
                    '0036', '0002', '0003'],
        'type_dict': {}
    },
    '3A': {
        'name': '综合数据_闸后水位',
        'type': '上行',
        'default': [],
        'element': ['0058', '0059'],
        'type_dict': {}
    },
    '60': {
        'name': '数据召测_业务数据',
        'type': '应答',
        'default': [],
        'element': ['0014', '0015', '0016', '0017', '0018', '0019', '0020', '0021', '0022', '0023', '0008', '0009',
                    '0002', '0003'],
        'type_dict': {}
    },
    '61': {
        'name': '数据召测_工况数据',
        'type': '应答',
        'default': [],
        'element': ['0024', '0025', '0026', '0027', '0028', '0029', '0030', '0031', '0032', '0033', '0034', '0035',
                    '0036', '0002', '0003'],
        'type_dict': {}
    },
    '62': {
        'name': '数据召测_业务数据历史',
        'type': '应答',
        'default': [],
        'element': ['0054', '0055', '0056', '0057'],
        'type_dict': {}
    },
    '63': {
        'name': '数据召测_业务数据历史',
        'type': '应答',
        'default': [],
        'element': ['0054', '0055', '0056', '0057'],
        'type_dict': {}
    },
    '70': {
        'name': '参数设置_遥测终端地址',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '71': {
        'name': '参数设置_遥测终端时钟',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '72': {
        'name': '参数设置_终端远程/现地模式',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '73': {
        'name': '参数设置_终端上报周期',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '74': {
        'name': '参数设置_终端上报中心',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '75': {
        'name': '参数设置_终端重启',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '80': {
        'name': '控制指令_手动/自动模式切换',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '81': {
        'name': '控制指令_手动远程控制',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '82': {
        'name': '控制指令_自动远程控制',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '83': {
        'name': '控制指令_唤醒摄像头',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '90': {
        'name': '远程升级_设备升级',
        'type': '应答',
        'default': [],
        'element': ['0001', '0051', '0048'],
        'type_dict': {}
    }
}

# 平台至设备协议配置，包括平台主动下发以及对设备的响应
PLATFORM_2_DEVICE = {
    '00': {
        'name': '通讯信息_注册',
        'type': '应答',
        'default': [],
        'element': ['0001'],
        'type_dict': {}
    },
    '01': {
        'name': '通讯信息_心跳',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '10': {
        'name': '状态信息_远程/现地模式',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '11': {
        'name': '状态信息_运动状态',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '20': {
        'name': '报警故障_设备报警',
        'type': '应答',
        'default': [],
        'element': ['0010', '0011', '0002', '0003'],
        'type_dict': {}
    },
    '21': {
        'name': '报警故障_设备故障',
        'type': '应答',
        'default': [],
        'element': ['0012', '0013', '0002', '0003'],
        'type_dict': {}
    },
    '30': {
        'name': '综合数据_业务数据',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '31': {
        'name': '综合数据_工况数据',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '3A': {
        'name': '综合数据_闸后水位',
        'type': '应答',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '60': {
        'name': '数据召测_业务数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '61': {
        'name': '数据召测_工况数据',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '62': {
        'name': '数据召测_业务数据历史',
        'type': '上行',
        'default': [],
        'element': ['0052', '0053'],
        'type_dict': {}
    },
    '63': {
        'name': '数据召测_业务数据历史',
        'type': '上行',
        'default': [],
        'element': ['0052', '0053'],
        'type_dict': {}
    },
    '70': {
        'name': '参数设置_遥测终端地址',
        'type': '上行',
        'default': [],
        'element': ['0037', '0002', '0003'],
        'type_dict': {}
    },
    '71': {
        'name': '参数设置_遥测终端时钟',
        'type': '上行',
        'default': [],
        'element': ['0038', '0002', '0003'],
        'type_dict': {}
    },
    '72': {
        'name': '参数设置_终端远程/现地模式',
        'type': '上行',
        'default': [],
        'element': ['0008', '0002', '0003'],
        'type_dict': {}
    },
    '73': {
        'name': '参数设置_终端上报周期',
        'type': '上行',
        'default': [],
        'element': ['0039', '0040', '0002', '0003'],
        'type_dict': {}
    },
    '74': {
        'name': '参数设置_终端上报中心',
        'type': '上行',
        'default': [],
        'element': ['0041', '0002', '0003'],
        'type_dict': {}
    },
    '75': {
        'name': '参数设置_终端重启',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '80': {
        'name': '控制指令_手动/自动模式切换',
        'type': '上行',
        'default': [],
        'element': ['0042', '0002', '0003'],
        'type_dict': {}
    },
    '81': {
        'name': '控制指令_手动远程控制',
        'type': '上行',
        'default': [],
        'element': ['0042', '0002', '0003'],
        'type_dict': {}
    },
    '82': {
        'name': '控制指令_自动远程控制',
        'type': '上行',
        'default': [],
        'element': ['0043', '0044', '0002', '0003'],
        'type_dict': {}
    },
    '83': {
        'name': '控制指令_唤醒摄像头',
        'type': '上行',
        'default': [],
        'element': [],
        'type_dict': {}
    },
    '90': {
        'name': '远程升级_设备升级',
        'type': '上行',
        'default': [],
        'element': ['0045', '0046', '0047', '0048', '0049', '0050', '0002', '0003'],
        'type_dict': {}
    }
}

# 入库的命令列表
IS_SAVE_LIST = ['00', '01', '10', '11', '20', '21', '30', '31', '3A']

# 配置的CLASS
__CLASS__ = 'AllCanalSettingInfo'


class AllCanalSettingInfo(object):
    """
    获取全渠道测控一体化协议配置信息
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
