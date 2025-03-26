

export function setEmployeesSpreadsheet(spreadSheetId) {
    jspreadsheet(spreadSheetId, {
        worksheets: [{
            data: [
                ['Hello', 13123, '', 'Yes', true, '#AA4411'],
                ['World!', 8, '', 'No', false, '#99BE23']
            ],
            columns: [
                { type: 'text', title: 'Text' },
                { type: 'numeric', title: 'Numeric', mask: '$ #.##,00', decimal: ',' },
                { type: 'calendar', title: 'Calendar' },
                { type: 'dropdown', source: ['Yes', 'No', 'Maybe'] },
                { type: 'checkbox', title: 'Checkbox' },
                { type: 'color', title: 'Color', width: 50, render: 'square' }
            ]
        }]
    })
};
