from flask import Blueprint, request, jsonify


employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/<int:subsection_id>', methods=['GET', 'POST'])
def manage_productionline(subsection_id):
    from myapp import db
    from ..model import Employee
    if request.method == 'GET':
        print(f"subsection_id={subsection_id}")
        # 指定されたsubsection_idに紐づいた子係(employees)を取得
        employees = Employee.query.filter_by(subsection_id=subsection_id).all()

        if not employees:
            print("データが見つかりませんでした[]を返します")
            return jsonify([])
        # 指定されたsubsectionIDのprodlineのみを格納
        response = jsonify([employee.to_dict() for employee in employees])
        print(f"レスポンスデータ:{response.get_json}")
        return response

    # 更新・保存機能
    elif request.method == 'POST':
        data = request.json

        if not data:
            print("エラーです、リクエストデータがNone")
            return jsonify({"error": "リクエストボディが空です"}, 400)

        # リクエスト(reqeuest.json)からIDリストを取得
        # incoming_ids = [item.get('id') for item in data if 'id' in item]

        exsiting_employees = Employee.query.filter_by(
            subsection_id=subsection_id).all()

        # 既存データを更新 or 削除

        for employee in exsiting_employees:
            # data を for文で回して、それぞれのidが既存データにあるかどうかを確認
            # あれば、そのデータを更新し、なければ削除する
            match_data = next((item for item in data if str(
                item.get('id')) == str(employee.id)), None)
            if match_data:
                employee.name = match_data.get('name', employee.name)
                employee.updated_by = match_data.get(
                    'updated_by', employee.updated_by)
            else:
                db.session.delete(employee)

        # 新しいデータを追加（idが返り値でなかったら新規登録する)
        for item in data:
            if 'id' not in item:
                new_employee = Employee(
                    subsection_id=subsection_id,
                    name=item.get('name'),
                    position_id=item.get('position_id'),
                    created_by=item.get('created_by'),
                    updated_by=item.get('updated_by')
                )
                db.session.add(new_employee)

        db.session.commit()
        print(
            f"更新後のsubsections:{[employee.to_dict() for employee in Employee.query.filter_by(subsection_id=subsection_id).all()]}")
        return jsonify({"message": "subsections updated successfully"})
