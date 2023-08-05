from datappkit.services.base_request import BaseRequest, CURRENT_YUEYING_USER_URI, YUEYING_LOGIN_URI, SEARCH_EMPLOYEE, \
    SEARCH_GUC_COMPANY_USER, SEARCH_PROJECT_USER, SEARCH_COMPANY_USER


class UserService:

    def login(self, account, password):
        body = {'account': account, 'password': password}
        return BaseRequest('POST', YUEYING_LOGIN_URI, {}, body=body).request()

    def search_user(self, search, role):
        # 1研究员、2DPM、3费用接口人、4需求方成员、5项目经理、6执行人员
        res = {"code": 0, "error_message": "error", "data": {}}
        if role in (0, 1, 3):
            uri = SEARCH_EMPLOYEE
            params = {
                "origin": 2,
                "name": search
            }
            res = BaseRequest('GET', uri, params).request()
            if res['code'] == 10000:
                users = []
                for item in res['data']:
                    users.append({
                        "user_id": item['employeeId'],
                        "user_name": item['name'],
                        "user_account": item['username'],
                        "department_id": item['departmentId']
                    })
                res['data'] = users
        elif role in (2, 4):
            uri = SEARCH_GUC_COMPANY_USER
            params = {}
        elif role == 5:
            uri = SEARCH_PROJECT_USER
            params = {}
        elif role == 6:
            uri = SEARCH_COMPANY_USER
            params = {}
        else:
            uri = SEARCH_EMPLOYEE
            params = {}
        return res

    def current_user(self):
        return BaseRequest('GET', CURRENT_YUEYING_USER_URI, {}).request()
