export { buildTreeView } from "/static/js/treeview.js"

// ツリー構造のデータを取得
export async function fetchTreeData() {
    try {
        const response = await fetch('/api/tree');
        const data = await response.json();
        console.log(`取得データ:`, JSON.stringify(data, null, 2));
        return data;
    } catch (error) {
        console.error('データ取得エラー', error);
        return null
    }


}