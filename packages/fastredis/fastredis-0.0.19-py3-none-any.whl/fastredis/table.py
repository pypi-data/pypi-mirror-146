#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import fastredis
import copy
"""
基于Redis Hash实现的二维表缓存数据库

name作为列名
key作为数据的id
value作为数据的值

1个db认为是一张表
"""


def columns(
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env'
):
    """
    获取所有的列名，对应redis中的第一层key的列表
    """
    return fastredis.keys(
        db=db,
        con_info=con_info,
        env_file_name=env_file_name
    )


def query(
        res_columns: list = None,  # 查询结果需要的列，['col1', 'col2]
        exact_query: dict = None,  # 精确查询，{'col1': 'a'}
        fuzzy_query: dict = None,  # 模糊查询，{'col1': 'a'}
        range_query: dict = None,  # 范围查询，{'col1': [start value, end value]} 只支持int数字查询，如果是时间查询，用时间戳
        sort_by: dict = None,  # 排序依据，{'col1': 'desc'}, desc=降序，asc=升序
        db: int = None,
        con_info: dict = None,  # 若指定，将优先使用
        env_file_name: str = 'redis.env',
        auto_reconnect=False,
):
    """
    查询功能
    """
    res_list = list()
    res_dict = dict()
    query_list = list()
    query_keys = list()

    # 筛选返回列
    if res_columns is None:
        # 返回所有
        inner_res_columns = columns(
            db=db,
            con_info=con_info,
            env_file_name=env_file_name
        )
    else:
        inner_res_columns = res_columns

    # -------------- 查询条件区域 --------------
    if range_query is None:  # 第一优先级：范围查询
        pass
    else:
        query_keys.append(range_query.keys())

    if exact_query is None:  # 第二优先级：精确查询
        pass
    else:
        query_keys.append(exact_query.keys())

    if fuzzy_query is None:  # 第三优先级：模糊查询
        pass
    else:
        query_keys.append(fuzzy_query.keys())
    # -------------- 查询条件区域 --------------

    if sort_by is None:  # 排序
        pass
    else:
        query_keys.append(sort_by.keys())

    if len(query_keys) == 0:
        # 获取所有数据
        for each_name in inner_res_columns:
            all_value = fastredis.hash_get_all(
                name=each_name,
                db=db,
                con_info=con_info,
                env_file_name=env_file_name,
                auto_reconnect=auto_reconnect,
                decode=False
            )
            for _key, _value in all_value.items():
                _key_decode = _key.decode()
                _value_decode = _value.decode()
                if _key_decode in res_dict.keys():
                    res_dict[_key_decode][each_name] = _value_decode
                else:
                    res_dict[_key_decode] = {each_name: _value_decode}
        for res_key, res_value in res_dict.items():
            temp_dict = copy.deepcopy(res_value)
            temp_dict['id'] = res_key
            res_list.append(temp_dict)
    else:
        # 有查询条件
        print(
            query_keys
        )
        query_keys_single = set(query_keys)  # 对条件列去重，先将符合条件的值的id都找到，再拼出结果
        if range_query is None:  # 第一优先级：范围查询
            pass
        else:
            # 开始查询符合条件的id
            for
            query_keys.append(range_query.keys())

        if exact_query is None:  # 第二优先级：精确查询
            pass
        else:
            query_keys.append(exact_query.keys())

        if fuzzy_query is None:  # 第三优先级：模糊查询
            pass
        else:
            query_keys.append(fuzzy_query.keys())

    return res_list


test_res = query(
    res_columns=['hash2', 'hash3'],
    exact_query={'id': '222'}
)
print(test_res)
