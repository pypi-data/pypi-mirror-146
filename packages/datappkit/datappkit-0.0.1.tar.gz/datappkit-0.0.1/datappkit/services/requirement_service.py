from datappkit.services.base_request import BaseRequest, GET_REQUIREMENT_DETAIL_URI, POST_REQUIREMENT_URI, GET_REQUIREMENT_URI, \
    PATCH_REQUIREMENT_URI


class RequirementService:

    def create(self, data):
        body = {
            "title": data['name'],
            "researcher_id": data['researcher_id'],
            "researcher_department_id": data['researcher_department_id'],
            "security_level": data['security_level'],
            "task_type_id": data['label_type_id'],
            "estimated_count": data['estimated_count'],
            "description": data['description'],
            "expect_start_at": data['start_time'],
            "expect_end_at": data['end_time'],
            "payer_allocation_list": data['payer_list'],
            "data_type_id": data['data_type_id'],

            "payer_allocation_type": 1 if len(data['payer_list']) > 1 else 0,
            "type": 1,  # 需求类型 1标注
        }
        return BaseRequest('POST', POST_REQUIREMENT_URI, {}, body=body).request()

    def patch(self, data):
        uri = PATCH_REQUIREMENT_URI.format(data['id'])
        body = {}
        if data.get('name'):
            body['title'] = data['name']
        if data.get('researcher_id'):
            body['researcher_id'] = data['researcher_id']
        if data.get('researcher_department_id'):
            body['researcher_department_id'] = data['researcher_department_id']
        if data.get('security_level'):
            body['security_level'] = data['security_level']
        if data.get('label_type_id'):
            body['task_type_id'] = data['label_type_id']
        if data.get('estimated_count'):
            body['estimated_count'] = data['estimated_count']
        if data.get('description'):
            body['description'] = data['description']
        if data.get('start_time'):
            body['expect_start_at'] = data['start_time']
        if data.get('end_time'):
            body['expect_end_at'] = data['end_time']
        if data.get('payer_list'):
            body['payer_allocation_list'] = data['payer_list']
        if data.get('data_type_id'):
            body['data_type_id'] = data['data_type_id']
        if data.get('payer_list'):
            body['payer_allocation_type'] = 1 if len(data['payer_list']) > 1 else 0
        if data.get('state'):
            body['state'] = data['state']
        return BaseRequest('PATCH', uri, {}, body=body).request()

    def get(self, requirement_id):
        uri = GET_REQUIREMENT_DETAIL_URI.format(requirement_id)
        res = BaseRequest('GET', uri, {}).request()
        return {
            "id": res['id'],
            "state": res['state'],
            "state_desc": res['state_object']['desc'],
            "create_time": res['created_at'],

            "name": res['title'],
            "label_type_id": res['task_type']['id'],
            "label_type_name": res['task_type']['name'],
            "estimated_count": res['estimated_count'],
            "start_time": res['expect_start_at'],
            "end_time": res['expect_end_at'],
            # todo 需要转换为bpp统一的值：1公开、2内部、3秘密、4绝密-低级、5绝密-高级（现在的值是：7内部、
            "security_level_id": res['security_level'],
            "payer_group_id": res['payer_group_id'],
            "data_manager": res['data_manager_id'],
            "researcher_id": res['researcher_id'],
            "employee_id": res['employee_id'],
            "comments": res['comments'],
            "description": res['description'],
            "email": "",
            "applicant_id": res['applicant_id'],
        }

    def get_list(self, page, per_page):
        params = {
            "page": page,
            "per_page": per_page
        }
        res = BaseRequest('GET', GET_REQUIREMENT_URI, params).request()
        re_list = []
        for item in res['items']:
            re_list.append({
                'id': item['id'],
                'name': item['title'],
                'state': item['state'],
                'label_type_id': item['task_type_id'],
                'applicant_username': item['applicant']['username'],
                'create_time': item['created_at'],
            })
        return {'pagination': res['pagination'], 'items': re_list}
