def prepare_data(pre_data):
    res = []
    for data in pre_data:
        item = {
            "id_tech": data.id_tech,
            "passport": data.passport,
            "status": data.status,
            "comments": data.comments,
            "details_fo_client": data.details_fo_client,
            "id_master": data.id_master,
            "acceptance_date": data.acceptance_date.strftime("%Y-%m-%d"),
        }
        res.append(item)
    return res
