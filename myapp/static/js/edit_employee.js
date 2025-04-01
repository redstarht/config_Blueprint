import { clearActiveTreeItems } from "/static/js/utils.js";

// 係を選択したときの処理(残す)
export function handleEmployees(selectedElement, subsectionId, subsectionName, factoryName, departmentName, sectionName) {

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


    const titleElement = [factoryTitle, departmentTitle, sectionName, subsectionName].filter(Boolean);
    document.getElementById('cardtitle-main').textContent = `「${titleElement.join('/')}」に所属する人員を編集`;

    // 選択状態のリセット
    clearActiveTreeItems();

    // 新しく選択した課にハイライトを適用
    selectedElement.classList.add('active');

    // フォームと保存ボタンを表示
    document.getElementById('saveButton').style.display = 'block';
    document.getElementById('spreadsheet').style.display = 'block';

    // 保存ボタンに subsection_id をセット
    console.log(subsectionId);
    document.getElementById('saveButton').dataset.subsectionId = subsectionId;

    // APIから所属係の人員データを取得
    fetchEmployees(subsectionId);
}   



// 人員データを取得して表示
function fetchEmployees(subsectionId) {
    fetch(`/api/employees/${subsectionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTPエラー! ステータス: ${response.status}`);
            }
            return response.json();
        })
        .then(employees => {
            console.log(employees)
            let formattedEmployees  = formatData(employees);
            let spreadSheetId = document.getElementById('spreadsheet');
            setEmployeesSpreadsheet(spreadSheetId, formattedEmployees);
        })
        .catch(error => console.error('取得エラー:', error));
}

// 係の各データを読み込み・フォーム書き出し（データがない場合でも要素が消えないようにする）
//  return fetchdata
function formatData(employees) {
    console.log(employees)
    let formattedEmployees = employees.map(employee =>[
        employee.id,
        employee.subsection_id,
        employee.name,
        employee.code,
        employee.position_id,
        employee.category,
        employee.sort_order,
        employee.is_deleted,
        employee.created_by,
        employee.updated_by,
        employee.created_at,
        employee.updated_at
    ]);

    return formattedEmployees;
    
}

// 保存ボタン処理
export function setupSaveButton() {
    document.getElementById('saveButton').addEventListener('click', () => {
        const subsectionId = document.getElementById('saveButton').dataset.subsectionId;

        if (!subsectionId) {
            console.error("エラー: subsectionIdが取得できませんでした");
            alert("エラー: subsectionIdが未設定です");
            return;
        }

        const productionLines = [];
        for (let i = 1; i <= 5; i++) {
            const input = document.getElementById(`lineName${i}`);
            const lineID = document.getElementById(`lineID${i}`);

            if (!input || !lineID) continue;

            let name = input.value.trim();
            const id = lineID.dataset.lineID;
            let created_by = window.sessionData.id;
            let updated_by = window.sessionData.id;

            if (lineID.dataset.lineID) {
                if (!input.value) {
                    name = '';
                }
            }

            // 既存データをID保持したまま送信(nameが空でも送る)
            if (id) {
                productionLines.push({ id, name, updated_by });
                // 新規データはnameがある場合のみ送る
            } else if (name) {
                productionLines.push({ name, created_by });
            }
        }

        saveproductionLines(subsectionId, productionLines);
    });
}

// 係データを保存
function saveproductionLines(subsectionId, productionLines) {
    fetch(`/api/productionlines/${subsectionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productionLines)
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
            fetchProductionLines(subsectionId); // 保存後にデータを再取得
        })
        .catch(error => {
            console.error('保存エラー', error);
            alert('データの取得に失敗しました');
        });
}




export function setEmployeesSpreadsheet(spreadSheetId,fetchdata) {
    jspreadsheet(spreadSheetId, {
        data: fetchdata,
        minDimensions: [3, 30],
        allowInsertColumn: false,
        columns: [
            { type: 'hidden',sort: false}, //管理ID 非表示
            { type: 'hidden',sort: false}, //所属係ID 非表示
            { type: 'text',title:'氏名',width:170,sort: false},//名前
            { type: 'numeric',title:'社員番号',width:90,sort: false},//コード(社員番号)
            { type: 'dropdown', title:'役職',width:170,source: ['一般(オペレータ)', '班長', '係長(工長)','課長','部長'],sort: false },//職位
            { type: 'hidden',sort: false},//sort_order 非表示
            { type: 'hidden',sort: false},//is_deleted 非表示
            { type: 'hidden',sort: false},//created_by 非表示
            { type: 'hidden',sort: false},//updated_by 非表示
            { type: 'hidden',sort: false},//created_at 非表示
            { type: 'hidden',sort: false},//updated_at 非表示
        ]
    })
};

// id hidden
// subsection_id hidden
// name text
// code text
// position_id dropdown
// sort_order hidden
// is_deleted hidden
// created_by hidden
// updated_by hidden
// created_at hidden
// updated_at hidden
