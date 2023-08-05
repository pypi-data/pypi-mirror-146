import sys
sys.path.append("/Users/baojiarui/PycharmProjects/data-service-sdk/datappkit")

from common import config
from datapp import Datapp


def create():
    """
    test 创建需求
    """
    data = {
        "name": "sdk_test_0406b",
        "researcher_id": "100793",
        "researcher_department_id": "S461",
        "security_level": 3,
        "label_type_id": 1000,
        "estimated_count": 50,
        "description": "",
        "start_time": 1649174400,
        "end_time": 1683648000,
        "data_type_id": 0,
        "payer_list": [
            {
                "employee_id": "100793",
                "rate": 30,
                "payer_department_id": "S461",
            },
            {
                "employee_id": "101608",
                "rate": 70,
                "payer_department_id": "S461",
            }
        ],
    }
    create_res = datapp.create_requirement(data)
    print("create_res=", create_res)


def patch():
    """
    test 修改需求
    """
    data = {
        "id": 1079,
        "name": "sdk_test_0406b_update1",
        "payer_list": [
            {
                "employee_id": "100793",
                "rate": 30,
                "payer_department_id": "S461",
            },
            {
                "employee_id": "101608",
                "rate": 70,
                "payer_department_id": "S461",
            }
        ],
    }
    update_res = datapp.update_requirement(data)
    print("update_res=", update_res)


def get_detail():
    """
    test 获取需求详情
    """
    detail = datapp.get_requirement(1079)
    print("detail=", detail)


if __name__ == '__main__':
    datapp = Datapp()
    # try:
        # test jwt
    config.JWT = 'JWT eyJ0eXBlIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJ1c2VyX2lkIjozNywiaWF0IjoxNjQ5MjE1MjU0LCJleHBpcmVfYXQiOjE2NjczNTkyNTQsImRvbWFpbiI6Im1lZ3l1ZXlpbmcuY29tIiwicGxhdGZvcm1faWQiOjIxfQ.fQXfDbwvpg4N8U_2xoZaLKasi_zmH6uMvSILsEyhhz32tj5mxtlsJvueHZ5fYWbKT5OozLDEe-lHUEUsde8U8iE6nfL1XBFM4HvCbjDskFJt-G6yC2AgV6XEYZAMsOne9ni9kVlKwIG9_mqm1oiv0wE-LLhm732ySYfTf7s9DiDLEV-TLOjLPIkGYKHUN-Oi1XiLOf_gkNlGy4DVWLCh4CRsLZngD5ysz9ZkHj1cE8hqvk1IphwJ4D9a7H_nharumisS2SI4nVpQDr8Za_goIZmJ6KED3oS9WlX3cQPweQ0oX5oSFIyIEd7VVDcusoMp0ykFZYUjH9R_GbLQKaSYoA'

        # 创建需求
        # create()

        # 获取需求详情
    get_detail()

        # 修改需求
    # patch()

        # 获取需求list
        # re_list = datapp.get_requirements(1, 2)
        # print("re_list=", re_list)
    # except Exception as e:
    #     print(e)