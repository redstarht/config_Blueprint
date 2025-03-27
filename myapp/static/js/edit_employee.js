

export function setEmployeesSpreadsheet(spreadSheetId) {
    jspreadsheet(spreadSheetId, {
        data: [
            ['Hello', 13123, '', 'Yes', true, '#AA4411'],
            ['World!', 8, '', 'No', false, '#99BE23']
        ],
        columns: [
            { type: 'hidden'}, //管理ID 非表示
            { type: 'hidden'}, //所属係ID 非表示
            { type: 'text'},//名前
            { type: 'text'},//コード
            { type: 'dropdown', source: ['担当', '班長', '組長','課長','部長'] },//職位
            { type: 'hidden',},//sort_order 非表示
            { type: 'hidden',},//is_deleted 非表示
            { type: 'hidden',},//created_by 非表示
            { type: 'hidden',},//updated_by 非表示
            { type: 'hidden',},//created_at 非表示
            { type: 'hidden',},//updated_at 非表示
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
