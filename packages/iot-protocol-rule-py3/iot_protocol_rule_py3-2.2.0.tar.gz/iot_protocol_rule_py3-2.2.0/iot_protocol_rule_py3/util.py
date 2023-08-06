# -*- coding: utf-8 -*-
"""
File Name  util
Created on 2019/08/20

@author: gw

"""

CREATE_FIELD_SQL = "`{code}` varchar(20) DEFAULT NULL COMMENT '{name}'"

CREATE_TABLE_SQL = """
    CREATE TABLE `{table_name}` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键标识',
      `equip_address` varchar(20) DEFAULT NULL COMMENT '设备地址',
      {fields},
      `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
      `receive_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '接收时间',
      PRIMARY KEY (`id`),
      KEY `rds_idx_{table_name}` (`equip_address`,`create_time`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class SettingFactory(object):
    def __init__(self, protocol):
        """
        协议规约配置工厂
        :param protocol:
        """
        self.setting_info = None
        self.__query_params = None
        self.__query_conditions = None
        self.__pageNum = None
        self.__pageSize = None
        self.__protocol = protocol
        self.__get_setting()

    def __get_setting(self):
        """
        根据协议编码，动态获取协议配置规范
        :return:
        """
        try:
            protocol_module = __import__('protocol_rule_{}'.format(self.__protocol), globals())
            self.setting_info = getattr(protocol_module, protocol_module.__CLASS__)()
        except Exception as e:
            print(e)

    def __str2int(self, data, default=0):
        """
        将字符串转为数字，
        将None或空字符串转为默认值（默认为0）
        :param data:
        :param default:
        :return:
        """
        try:
            return default if not data else int(data)
        except:
            return default

    def __filter(self, data):
        """
        过滤函数
        :param data:
        :return:
        """
        flg = False
        if self.__query_params and self.__query_conditions:
            for condition in self.__query_conditions:
                if self.__query_params in data[condition]:
                    flg = True
                    break
                else:
                    pass
        else:
            flg = True

        return flg

    def __paging(self, data_list):
        """
        分页函数
        :param data_list:
        :return:
        """
        if self.__pageNum == 'all':
            data_list = data_list
        else:
            pageNum = self.__str2int(self.__pageNum, 1)
            pageSize = self.__str2int(self.__pageSize, 10)
            begin_index = (pageNum - 1) * pageSize
            end_index = begin_index + pageSize
            data_list = data_list[begin_index: end_index]
        return data_list

    def get_element(self):
        """
        获取元素字典
        :return:
        """
        element_list = []
        element_dict = self.setting_info.get_element_dict()
        for key in sorted(element_dict):
            element_list.append({
                'index_code': key,
                'code': element_dict[key]['code'],
                'name': element_dict[key]['name'],
                'length': element_dict[key].get('length')
            })
        return element_list

    def get_device_2_platform(self):
        """
        获取设备至平台协议
        :return:
        """
        command_list = []
        command_dict = self.setting_info.get_device_2_platform()
        element_dict = self.setting_info.get_element_dict()
        for command_index in sorted(command_dict):
            command_code = command_index
            command_name = command_dict[command_index]['name']
            command_type = command_dict[command_index]['type']
            command_default = []
            command_element = []
            for default_index in command_dict[command_index]['default']:
                command_default.append({
                    'code': element_dict[default_index]['code'],
                    'name': element_dict[default_index]['name'],
                    'length': element_dict[default_index]['length']
                })
            for element_index in command_dict[command_index]['element']:
                command_element.append({
                    'code': element_dict[element_index]['code'],
                    'name': element_dict[element_index]['name'],
                    'length': element_dict[element_index]['length']
                })
            if command_dict[command_index]['type_dict']:
                for type_index in sorted(command_dict[command_index]['type_dict']):
                    command_type_code = type_index
                    command_type_name = command_dict[command_index]['type_dict'][type_index]['name']
                    command_type_type = command_dict[command_index]['type_dict'][type_index].get('type')
                    command_type_element = []
                    for command_type_index in command_dict[command_index]['type_dict'][type_index]['element']:
                        command_type_element.append({
                            'code': element_dict[command_type_index]['code'],
                            'name': element_dict[command_type_index]['name'],
                            'length': element_dict[command_type_index]['length']
                        })

                    command_list.append({
                        'code': '{}_{}'.format(command_code, command_type_code),
                        'name': '{}({})'.format(command_name, command_type_name),
                        'type': command_type_type if command_type_type else command_type,
                        'element': command_default + command_element + command_type_element
                    })
            else:
                command_list.append({
                    'code': command_code,
                    'name': command_name,
                    'type': command_type,
                    'element': command_default + command_element
                })
        return command_list

    def get_platform_2_device(self):
        """
        获取平台至设备协议
        :return:
        """
        command_list = []
        command_dict = self.setting_info.get_platform_2_device()
        element_dict = self.setting_info.get_element_dict()
        for command_index in sorted(command_dict):
            command_code = command_index
            command_name = command_dict[command_index]['name']
            command_type = command_dict[command_index]['type']
            command_default = []
            command_element = []
            for default_index in command_dict[command_index]['default']:
                command_default.append({
                    'code': element_dict[default_index]['code'],
                    'name': element_dict[default_index]['name'],
                    'length': element_dict[default_index]['length']
                })
            for element_index in command_dict[command_index]['element']:
                command_element.append({
                    'code': element_dict[element_index]['code'],
                    'name': element_dict[element_index]['name'],
                    'length': element_dict[element_index]['length']
                })
            if command_dict[command_index]['type_dict']:
                for type_index in sorted(command_dict[command_index]['type_dict']):
                    command_type_code = type_index
                    command_type_name = command_dict[command_index]['type_dict'][type_index]['name']
                    command_type_type = command_dict[command_index]['type_dict'][type_index].get('type')
                    command_type_element = []
                    for command_type_index in command_dict[command_index]['type_dict'][type_index]['element']:
                        command_type_element.append({
                            'code': element_dict[command_type_index]['code'],
                            'name': element_dict[command_type_index]['name'],
                            'length': element_dict[command_type_index]['length']
                        })

                    command_list.append({
                        'code': '{}_{}'.format(command_code, command_type_code),
                        'name': '{}({})'.format(command_name, command_type_name),
                        'type': command_type_type if command_type_type else command_type,
                        'element': command_default + command_element + command_type_element
                    })
            else:
                command_list.append({
                    'code': command_code,
                    'name': command_name,
                    'type': command_type,
                    'element': command_default + command_element
                })
        return command_list

    def get_api_data_command(self):
        """
        获取API数据服务爬取的命令列表
        :return:
        """
        command_list = []
        is_save_list = self.setting_info.get_save_list()
        for command in self.get_device_2_platform():
            if command['code'] in is_save_list:
                command_list.append(command)
            else:
                pass

        return command_list

    def get_api_order_command(self):
        """
        获取API命令服务爬取的命令列表
        :return:
        """
        command_list = []
        for k, v in self.setting_info.get_platform_2_device().items():
            if v['type'] == '上行':
                command_list.append(k)
            else:
                pass

        return command_list

    def get_create_table_sql(self):
        """
        获取API数据服务爬取的命令的建表语句
        :return:
        """
        table_list = []
        for command in self.get_api_data_command():
            table_name = '{}__{}'.format(self.__protocol, command['code'])
            field_list = []
            for element in command['element']:
                field_list.append(CREATE_FIELD_SQL.format(code=element['code'], name=element['name']))

            table_list.append({
                'table_name': table_name,
                'sql': CREATE_TABLE_SQL.format(table_name=table_name + '___{sub_rule}', fields=',\n  '.join(field_list))
            })
        return table_list

    def query(self, query_params, query_conditions, pageNum, pageSize, data_list):
        """
        查询(模糊查询，分页查询)
        :param query_params:
        :param query_conditions:
        :param pageNum:
        :param pageSize:
        :param data_list:
        :return:
        """
        self.__query_params = query_params
        self.__query_conditions = query_conditions
        self.__pageNum = pageNum
        self.__pageSize = pageSize

        data_list = filter(self.__filter, data_list)  # 先进行模糊查询
        total = len(data_list)  # 总条数
        data_list = self.__paging(data_list)  # 在进行分页查询

        return total, data_list


if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    protocol_list = ['grm_cmqzm']

    for protocol in protocol_list:
        print(protocol)
        setting_factory = SettingFactory(protocol)
        if setting_factory.setting_info:
            for item in setting_factory.get_create_table_sql():
                file_path = item['table_name'] + '.txt'
                f = open('../../timed_monitor/db/table/' + file_path, "a")
                f.write(item['sql'])
                f.close()
        else:
            print("=========请检查{}=========".format(protocol))

        print(setting_factory.get_api_order_command())
