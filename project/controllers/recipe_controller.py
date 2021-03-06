from flask import Blueprint, request, abort, make_response, jsonify
from project.models.recipe import Recipe
from project.helpers import req_helper

bp = Blueprint('recipe', __name__)


@bp.route('/create', methods=['POST'])
def recipe_create():
    user = req_helper.force_session_get_user()
    if not user.canEditRecipes():
        req_helper.throw_not_allowed()

    data = req_helper.force_json_key_list('name', 'desc', 'detail', 'img_url', 'cost', 'ingredients', 'time', 'src',
                                          'category')

    if not data["name"].strip():
        req_helper.throw_operation_failed("Name cannot be empty!")

    if not isinstance(data['ingredients'], list) or len(data['ingredients']) < 1:
        req_helper.throw_operation_failed("Ingredients must be a nonempty list!")

    try:
        cost = float(data['cost'])
        time = int(data['time'])
    except:
        req_helper.throw_operation_failed("Cost and time need to be integers!")

    recipe_id = Recipe.create(data['name'], data['desc'], data['detail'], data['img_url'], cost, data['ingredients'],
                              data['src'], time, data['category'])

    if recipe_id:
        return jsonify(message="Ok!", id=str(recipe_id))
    else:
        req_helper.throw_operation_failed(
            "Could not create! Maybe check the ingredients ids or make sure quantities are numbers!")


@bp.route('/all', methods=['POST'])
def recipe_get_all():
    req_helper.force_session_get_user()
    recipes = [val.__dict__ for val in Recipe.query()]
    return jsonify(recipes)


@bp.route('/query/<name>', methods=['POST'])
def recipe_query_name(name):
    req_helper.force_session_get_user()
    recipes = [val.__dict__ for val in Recipe.query({'name': {'$regex': '(?i)' + name}})]
    return jsonify(recipes)


@bp.route('/categories', methods=['POST'])
def get_categories():
    req_helper.force_session_get_user()
    cats = Recipe.get_categories()
    return jsonify(cats)


@bp.route('/by-category/<category>', methods=['POST'])
def get_by_category(category):
    req_helper.force_session_get_user()
    recipes = [val.__dict__ for val in Recipe.query({'category': category.lower()})]
    return jsonify(recipes)


@bp.route('/by-id/<recipe_id>', methods=['POST'])
def get_by_id(recipe_id):
    req_helper.force_session_get_user()
    result = Recipe.query_id(recipe_id)
    if result is not None:
        return jsonify(result.__dict__)
    else:
        req_helper.throw_not_found()

