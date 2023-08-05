from datappkit.services.base_request import BaseRequest, GET_LABEL_TYPE_URI, GET_LABEL_TASK


class LabelService:

    def get_label_type(self):
        res = BaseRequest('GET', GET_LABEL_TYPE_URI, {}).request()
        if res['code'] == 10000:
            type_list = []
            for item in res['data']['items']:
                if item['key'] == "task_type_id":
                    for label_type in item['options']:
                        if label_type['value']:
                            type_list.append({"id": label_type['value'], "name": label_type['text']})
            res['data'] = type_list
        return res

    def get_label_task(self, batch_id):
        uri = GET_LABEL_TASK.format(batchId=batch_id)
        res = BaseRequest('GET', uri, {}).request()
        if res['code'] == 10000:
            data = {
                "task_id": res['data']['data']['id'],
                "state": res['data']['data']['task_info']['state'],
                "state_desc": res['data']['data']['task_info']['state_desc'],
            }
            res['data'] = data
        return res
