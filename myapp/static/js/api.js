export {buildTreeView} from "./treeview"

 // ツリー構造のデータを取得
export function fetchTreeData(depth){
    fetch('/api/tree')
        .then(response => response.json())
        .then(data => {
            console.log(`取得データ:`,JSON.stringify(data,null,2));
            test = data ;
            buildTreeView(data,depth);
        })
        .catch(error => console.error('データ取得エラー',error));
}
