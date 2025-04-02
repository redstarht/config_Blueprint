from flask import Blueprint, render_template, request, jsonify, redirect,url_for,session
from .model import Accounts, Factory, Department, Section, Subsection, Production_line, Employee
from myapp import db
from flask_login import login_user,logout_user,login_required

main_bp = Blueprint('main', __name__)

# # ツリー用の配列オブジェクトデータ
# @main_bp.route('/api/tree', methods=['GET'])
# def get_tree():
#     factories = Factory.query.all()
#     # 返り値テスト
#     # confirm_json = []
#     # for factory in factories:
#     #     confirm_json.append(factory.to_dict())
#     # pprint.pprint(confirm_json)

#     return jsonify([factory.to_dict() for factory in factories])


# @main_bp.route('/api/subsections/<int:section_id>', methods=['GET', 'POST'])
# def manage_subsection(section_id):
#     if request.method == 'GET':
#         print(f"section_id={section_id}")
#         # 指定されたsection_idに紐づいた子係(subsections)を取得
#         subsections = Subsection.query.filter_by(section_id=section_id).all()

#         if not subsections:
#             print("データが見つかりませんでした[]を返します")
#             return jsonify([])

#         response = jsonify([sub.to_dict() for sub in subsections])
#         print(f"レスポンスデータ:{response.get_json}")
#         return response

#     # 更新・保存機能
#     elif request.method == 'POST':
#         data = request.json

        
        

#         if not data:
#             print("エラーです、リクエストデータがNone")
#             return jsonify({"error": "リクエストボディが空です"}, 400)
        
#         # リクエスト(reqeuest.json)からIDリストを取得
#         incoming_ids = [item.get('id') for item in data if 'id' in item]

#         exsiting_subsections = Subsection.query.filter_by(
#             section_id=section_id).all()
        
#         # 既存データを更新 or 削除
#         for sub in exsiting_subsections:
#             match_data=next((item for item in data if str(item.get('id'))==str(sub.id)),None)
#             if match_data:
#                 sub.name = match_data.get('name',sub.name)
#                 sub.updated_by = match_data.get('updated_by',sub.updated_by)
#             else:
#                 db.session.delete(sub)


#         # 新しいデータを追加（idが返り値でなかったら新規登録する)
#         for item in data:
#             if 'id' not in _by=item.get('updated_by')
#                 )
#                 db.session.add(new_sub)

#         db.session.commit()
#         print(
#             f"更新後のsubsections:{[sub.to_dict() for sub in Subsection.query.filter_by(section_id=section_id).all()]}")
#         return jsonify({"message": "subsections updated successfully"})

#                 new_sub=Subsection(
#                     section_id=section_id,
#                     name=item.get('name'),
#                     created_by=item.get('created_by'),
#                     updated

@main_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    '''
    HOMEは見る専の画面
    工場➡係➡選択肢で 人員 / 異常内容 までツリービューで選択
    人員 or 異常内容を選択したら、選択した内容を画面に表示する

    '''
    # print(f'{factories.name} {factories.code}')
    # factoryclass = repr(factories)
    # print(factoryclass)
    # リスト内包表記　factories_dict = [factory.to_dict() for factory in factories]　

    try:
        factories = Factory.query.all()
        print(f"取得した工場データ: {factories}")


    except Exception as e:
        print(f"データ取得エラー: {e}")
        return jsonify({"error": "データベースのクエリ実行時にエラーが発生しました"}), 500

    factories_dict = [factory.to_dict() for factory in factories]  # JSON変換用
    return render_template('index.html', factories=factories_dict)

# @main_bp.route('/login',methods=['GET','POST'])



@main_bp.route('/edit_subsection')
@login_required
def edit_unit():
    return render_template('edit_subsection.html')

@main_bp.route('/edit_employee')
@login_required
def edit_employee():
    return render_template('edit_employee.html')

@main_bp.route('/edit_productionline')
@login_required
def edit_productionline():
    return render_template('edit_productionline.html')

@main_bp.route('/edit_test')
def edit_test():
    return render_template('edit_test.html')


@main_bp.route('/departments/<int:factory_id>')
def departments(factory_id):
    departments = Department.query.filter_by(factory_id=factory_id).all()
    return render_template('departments.html', departments=departments)


@main_bp.route('/sections/<int:department_id>')
def sections(department_id):
    sections = Section.query.filter_by(department_id=department_id).all()
    return render_template('sections.html', sections=sections)


@main_bp.route('/subsections/<int:section_id>')
def subsections(section_id):
    subsections = Subsection.query.filter_by(section_id=section_id).all()
    return render_template('subsections.html', subsections=subsections)


@main_bp.route('/add_subsection/<int:section_id>', methods=['GET', 'POST'])
def add_subsection(section_id):
    if request.method == 'POST':
        name = request.form['name']
        new_subsection = Subsection(section_id=section_id, name=name)
        db.session.add(new_subsection)
        db.session.commit()
        return redirect(url_for('subsections', section_id=section_id))
    return render_template('add_subsection.html', section_id=section_id)


@main_bp.route('/edit_subsection/<int:subsection_id>', methods=['GET', 'POST'])
def edit_subsection(subsection_id):
    subsection = Subsection.query.get_or_404(subsection_id)
    if request.method == 'POST':
        subsection.name = request.form['name']
        db.session.commit()
        return redirect(url_for('subsections', section_id=subsection.section_id))
    return render_template('edit_subsection.html', subsection=subsection)
