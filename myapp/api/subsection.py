from flask import Blueprint, request, jsonify



subsection_bp = Blueprint('subsection',__name__)
@subsection_bp.route('/<int:section_id>', methods=['GET', 'POST'])
def manage_subsection(section_id):
    from myapp import db
    from ..model import Subsection
    if request.method == 'GET':
        print(f"section_id={section_id}")
        # 指定されたsection_idに紐づいた子係(subsections)を取得
        subsections = Subsection.query.filter_by(section_id=section_id).all()

        if not subsections:
            print("データが見つかりませんでした[]を返します")
            return jsonify([])

        response = jsonify([sub.to_dict() for sub in subsections])
        print(f"レスポンスデータ:{response.get_json}")
        return response

    # 更新・保存機能
    elif request.method == 'POST':
        data = request.json

        
        

        if not data:
            print("エラーです、リクエストデータがNone")
            return jsonify({"error": "リクエストボディが空です"}, 400)
        
        # リクエスト(reqeuest.json)からIDリストを取得
        incoming_ids = [item.get('id') for item in data if 'id' in item]

        exsiting_subsections = Subsection.query.filter_by(
            section_id=section_id).all()
        
        # 既存データを更新 or 削除
        for sub in exsiting_subsections:
            match_data=next((item for item in data if str(item.get('id'))==str(sub.id)),None)
            if match_data:
                sub.name = match_data.get('name',sub.name)
                sub.updated_by = match_data.get('updated_by',sub.updated_by)
            else:
                db.session.delete(sub)


        # 新しいデータを追加（idが返り値でなかったら新規登録する)
        for item in data:
            if 'id' not in item:
                new_sub=Subsection(
                    section_id=section_id,
                    name=item.get('name'),
                    created_by=item.get('created_by'),
                    updated_by=item.get('updated_by')
                )
                db.session.add(new_sub)

        db.session.commit()
        print(
            f"更新後のsubsections:{[sub.to_dict() for sub in Subsection.query.filter_by(section_id=section_id).all()]}")
        return jsonify({"message": "subsections updated successfully"})
