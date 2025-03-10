import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('SECRET_KEY'))  # .env に設定した SECRET_KEY が表示されるはず
print(os.getenv('DATABASE_URI')) 


@main_bp.route('/api/subsections/<int:section_id>', methods=['GET', 'POST'])
def manage_subsection(section_id):
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

        exsiting_subsections = Subsection.query.filter_by(
            section_id=section_id).all()

        # 既存データを更新 or 削除
        for i, sub in enumerate(exsiting_subsections):
            if i < len(data):
                # キーエラー防止
                sub.name = data[i].get('name', sub.name)
            else:
                # 余分なデータは削除
                db.session.delete(sub)

        # 新しいデータを追加
        for i in range(len(exsiting_subsections), len(data)):
            # section_id =flaskルーティング
            new_sub = Subsection(section_id=section_id, name=data[i]['name'])
            db.session.add(new_sub)

        db.session.commit()
        print(
            f"更新後のsubsections:{[sub.to_dict() for sub in Subsection.query.filter_by(section_id=section_id).all()]}")
        return jsonify({"message": "subsections updated successfully"})