from flask import Blueprint,jsonify
from myapp.model import Factory

tree_bp = Blueprint('factorytree',__name__)

# ツリー用の配列オブジェクトデータ
@tree_bp.route('/', methods=['GET'])
def get_tree():
    factories = Factory.query.all()
    # 返り値テスト
    # confirm_json = []
    # for factory in factories:
    #     confirm_json.append(factory.to_dict())
    # pprint.pprint(confirm_json)

    return jsonify([factory.to_dict() for factory in factories])

