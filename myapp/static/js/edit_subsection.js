import { clearActiveTreeItems } from "./utils.js";

// 課を選択したときの処理
export function selectSection(selectedElement,sectionId, sectionName, factoryName, departmentName) {
    // 課名をヘッダーに反映
    console.log(factoryName.name, departmentName.name, sectionName);
    console.log(factoryName, departmentName, sectionName);
    
    let factoryTitle
    let departmentTitle


    // オブジェクト型かどうか精査
    if (typeof factoryName === "object" && factoryName !== null) {
        factoryTitle = factoryName.name;
    } else {
        factoryTitle = factoryName;
    };
    if (typeof departmentName === "object" && departmentName !== null) {
        departmentTitle = departmentName.name;
    } else {
        departmentTitle = departmentName;
    }


    const titleElement = [factoryTitle, departmentTitle, sectionName].filter(Boolean);
    document.getElementById('cardtitle').textContent = `「${titleElement.join('/')}」に所属する係を編集`;

    // 選択状態のリセット
    clearActiveTreeItems();

    // 新しく選択した課にハイライトを適用
    selectedElement.classList.add('active');

    // フォームと保存ボタンを表示
    document.getElementById('editform').style.display = 'block';
    document.getElementById('saveButton').style.display = 'block';

    // 保存ボタンに section_id をセット
    console.log(sectionId);
    document.getElementById('saveButton').dataset.sectionId = sectionId;

    // APIから係のデータを取得
    fetchSubsections(sectionId);
}

// 係データを取得して表示
function fetchSubsections(sectionId) {
    fetch(`/api/subsections/${sectionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTPエラー! ステータス: ${response.status}`);
            }
            return response.json();
        })
        .then(subsections => {
            updateSubsectionForm(subsections);
        })
        .catch(error => console.error('subsectionsの取得エラー:', error));
}

// 係の各データを読み込み・フォーム書き出し（データがない場合でも要素が消えないようにする）
function updateSubsectionForm(subsections) {
    for (let i = 1; i <= 5; i++) {
        const input = document.getElementById(`item${i}`);
        const subsectionID = document.getElementById(`subsectionID${i}`);
        const createdAt = document.getElementById(`createdAt${i}`);
        const creator = document.getElementById(`creator${i}`);
        const updatedAt = document.getElementById(`updatedAt${i}`);
        const updater = document.getElementById(`updater${i}`);


        if (!input || !subsectionID || !createdAt || !updatedAt) {
            continue;
        }

        if (subsections[i - 1]) {
            input.value = subsections[i - 1].name;
            subsectionID.dataset.subsectionID = subsections[i - 1].id || '';
            subsectionID.textContent = `SubsectionID: ${subsections[i - 1].id || '未定義'} `;
            createdAt.textContent = `/ 作成: ${subsections[i - 1].created_at || '不明'}`;
            creator.textContent = `/ 作成者: ${subsections[i - 1].created_by_username || 'ユーザー不明'}`;
            updatedAt.textContent = `/ 更新: ${subsections[i - 1].updated_at || '未更新'}`;
            updater.textContent = `/ 更新者:${subsections[i - 1].updated_by_username || 'ユーザー不明'}`;
        } else {
            input.value = '';
            subsectionID.dataset.subsectionID = '';
            subsectionID.textContent = `SubsectionID: -`;
            createdAt.textContent = '/ 作成: -';
            creator.textContent = '/ 作成者: -';
            updatedAt.textContent = '/ 更新: -';
            updater.textContent = '/ 更新者: -';
        }
    }
}

// 保存ボタン処理
export function setupSaveButton() {
    document.getElementById('saveButton').addEventListener('click', () => {
        const sectionId = document.getElementById('saveButton').dataset.sectionId;

        if (!sectionId) {
            console.error("エラー: sectionIdが取得できませんでした");
            alert("エラー: sectionIdが未設定です");
            return;
        }

        const subsections = [];
        for (let i = 1; i <= 5; i++) {
            const input = document.getElementById(`item${i}`);
            const subsectionID = document.getElementById(`subsectionID${i}`);

            if (!input || !subsectionID) continue;

            let name = input.value.trim();
            const id = subsectionID.dataset.subsectionID;
            let created_by = window.sessionData.id;
            let updated_by = window.sessionData.id;

            if (subsectionID.dataset.subsectionID) {
                if (!input.value) {
                    name = '';
                }
            }

            // 既存データをID保持したまま送信(nameが空でも送る)
            if (id) {
                subsections.push({ id, name, updated_by });
                // 新規データはnameがある場合のみ送る
            } else if (name) {
                subsections.push({ name, created_by });
            }
        }

        saveSubsections(sectionId, subsections);
    });
}
// 係データを保存
function saveSubsections(sectionId, subsections) {
    fetch(`/api/subsections/${sectionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(subsections)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTPエラー status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('保存成功:', data);
            alert('保存しました');
            fetchSubsections(sectionId); // 保存後にデータを再取得
        })
        .catch(error => {
            console.error('保存エラー', error);
            alert('データの取得に失敗しました');
        });
}
