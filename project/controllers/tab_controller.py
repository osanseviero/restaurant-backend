
from flask import Blueprint, request, abort, make_response, jsonify
from project.models.tab import Tab
from project.helpers import req_helper
from datetime import datetime

bp = Blueprint('tab', __name__)

@bp.route('/create', methods=['POST'])
def tab_create():
    user = req_helper.force_session_get_user()
    if not user.canEditTabs():
        req_helper.throw_not_allowed()
    
    data = req_helper.force_json_key_list('table')

    try:
        table = int(data['table'])
    except:
        req_helper.throw_operation_failed("Table must be an integer")

    if 'customers' in data and isinstance(data['customers'], list) and len(data['customers']) > 0:
        customers = data['customers']
    else:
        customers = None

    tab_id = Tab.create(user, table, datetime.now(), customers)

    if not tab_id:
        req_helper.throw_operation_failed("Could not create! Maybe check usernames!")
    else:
        return jsonify(message='Ok!', id=tab_id)