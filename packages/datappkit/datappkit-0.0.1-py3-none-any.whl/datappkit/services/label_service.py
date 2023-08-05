from datappkit.services.base_request import BaseRequest, GET_LABEL_TYPE_URI, GET_LABEL_TASK


class LabelService:

    def get_label_type(self):
        res = BaseRequest('GET', GET_LABEL_TYPE_URI, {}).request()
        type_list = []
        for item in res['items']:
            if item['key'] == "task_type_id":
                for label_type in item['options']:
                    if label_type['value']:
                        type_list.append({"id": label_type['value'], "name": label_type['text']})
        return type_list

    def get_label_task(self, batch_id):
        uri = GET_LABEL_TASK.format(batchId=batch_id)
        res = BaseRequest('GET', uri, {}).request()
        return {
            "task_id": res['data']['id'],
            "state": res['data']['task_info']['state'],
            "state_desc": res['data']['task_info']['state_desc'],
        }
