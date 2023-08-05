from datappkit.services.base_request import BaseRequest, GET_BATCHES, POST_BATCHES_PUBLISH, GET_BATCHES_CONFIG


class BatchesService:

    def get_batches(self, search, page, per_page):
        params = {
            "page": page,
            "per_page": per_page
        }
        if search:
            params['search'] = search
        res = BaseRequest('GET', GET_BATCHES, params).request()
        re_list = []
        for item in res['items']:
            re_list.append({
                'id': item['id'],
                'name': item['name'],
                'state': item['state'],
                'state_desc': item['state_desc'],
                'label_type_id': item['task_type_id'],
            })
        return {'pagination': res['pagination'], 'items': re_list}

    def get_batches_config(self, batch_id):
        uri = GET_BATCHES_CONFIG.format(batchId=batch_id)
        return BaseRequest('GET', uri, {}).request()

    def publish_batches(self, batch_ids):
        body = {
            "batch_ids": batch_ids
        }
        return BaseRequest('POST', POST_BATCHES_PUBLISH, {}, body=body)
