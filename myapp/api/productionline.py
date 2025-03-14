from flask import Blueprint, request, jsonify



productionline_bp = Blueprint('productionline',__name__)
@productionline_bp.route('/<int:subsection_id>', methods=['GET', 'POST'])
def manage_productionline(subsection_id):
    from myapp import db
    from ..model import Production_line
    if request.method == 'GET':
        print(f"subsection_id={subsection_id}")
        # 指定されたsection_idに紐づいた子係(subsections)を取得
        productionlines = Production_line.query.filter_by(subsection_id=subsection_id).all()

        if not productionlines:
            print("データが見つかりませんでした[]を返します")
            return jsonify([])
        # 指定されたsubsectionIDのprodlineのみを格納
        response = jsonify([prodline.to_dict() for prodline in productionlines])
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

        exsiting_prodlines = Production_line.query.filter_by(
            subsection_id=subsection_id).all()
        
        # 既存データを更新 or 削除
        for prodline in exsiting_prodlines:
            match_data=next((item for item in data if str(item.get('id'))==str(prodline.id)),None)
            if match_data:
                prodline.name = match_data.get('name',prodline.name)
                prodline.updated_by = match_data.get('updated_by',prodline.updated_by)
            else:
                db.session.delete(prodline)


        # 新しいデータを追加（idが返り値でなかったら新規登録する)
        for item in data:
            if 'id' not in item:
                new_sub=Production_line(
                    subsection_id=subsection_id,
                    name=item.get('name'),
                    created_by=item.get('created_by'),
                    updated_by=item.get('updated_by')
                )
                db.session.add(new_sub)

        db.session.commit()
        print(
            f"更新後のsubsections:{[prodline.to_dict() for prodline in Production_line.query.filter_by(subsection_id=subsection_id).all()]}")
        return jsonify({"message": "subsections updated successfully"})
