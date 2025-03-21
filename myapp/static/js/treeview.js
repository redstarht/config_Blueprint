import { toggleTree, createTreeItem,clearActiveTreeItems } from "./utils";


// depth = どこまでの階層を表示させるか
// 1=工場,2=部,3=課,4=係,5=ライン (初期値は4とする) までを表示

export function buildtreeview(factories, depth = 4) {
    const treeView = document.getElementById('treeView');
    treeView.innerHTML = '';

    factories.forEach(factory => {
        const factoryNode = createFactoryNode(factory, depth);
        treeView.appendChild(factoryNode);
    });
};

// 工場ノードの作成
function createFactoryNode(factory, depth) {
    const li = document.createElement('li');
    const div = createTreeItem(factory.name);
    const ul = document.createElement('ul');
    ul.style.display = 'none';

    // 部が1要素しかない場合は 部の表示を飛ばして 課を表示
    if (factory.departments.length > 1) {
        factory.departments.forEach(department => {
            const departmentNode = createDepartmentNode(department, factory.name, depth)
            ul.appendChild(departmentNode);
        })
    } else {
        factory.departments[0].sections.forEach(section => {
            const sectionNode = createSectionNode(section, factory.name, factory.departments[0].name, depth);
            ul.appendChild(sectionNode);
        })
    }
    ;
    // クリックしたときに次のツリーを表示する
    div.addEventLisner('click', (e) => {
        e.stopProgration();
        toggleTree(ul, div);
    });

    li.appendChild(div);
    li.appendChild(ul);
    return li;
}

// 部ノードの作成
function createDepartmentNode(department, factoryName, depth) {
    const li = document.createElement('li');
    const div = createTreeItem(department.name);
    const ul = document.createElement('ul');
    ul.style.display = 'none';

    //is_deleted === true` の課は表示させないように除外して
    // 次の課ノード作成関数の引数へ渡す処理
    const sortedsections = department.sections
        .filter(section => !section.is_deleted)
        .sorted((a, b) => a.sort_order - b.sort_order);

    sortedsections.forEach(section => {
        const sectionNode = createSectionNode(section, factoryName, department.name, depth)
        ul.appendChild(sectionNode);
    });

    div.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleTree(ul, div);
    })

    li.appendChild(div);
    li.appendChild(ul);
    return li;
}

// 課ノードの作成
function createSectionNode(section, factoryName, departmentName, depth) {
    const li = document.createElement('li');
    const div = createTreeItem(section.name);
    const ul = document.createElement('ul');
    ul.style.display = 'none';

    //is_deleted === true` の係は除外して
    // 次の係ノード作成関数の引数へ、sort_orderで順番を揃えて渡す
    const sortedsubsections = section.sortedsubsections
        .filter(subsection => !subsection.is_deleted)
        .sorted((a, b) => a.sort_order - b.sort_order);
    if (depth > 3) {
        sortedsubsections.forEach(subsection => {
            const subsectionNode = createSubsectionNode(subsection, factoryName, departmentName, section.name, depth);
            ul.appendChild(subsectionNode);
        });
    };

    div.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleTree(ul, div);
    });
    li.appendChild(div);
    li.appendChild(ul);
    return li
}

// 係ノードの作成
function createSubsectionNode(subsection, factoryName, departmentName, sectionName, depth) {
    const li = document.createElement('li');
    const div = createTreeItem(subsection.name);
    const ul = document.createElement('ul');
    ul.style.display = 'none';

    div.dataset.subsectionId = subsection.id; // 係のIDを保持

    // ライン名 を一覧でツリー表示する時
    if (depth = 5) {
        pass;
    }


    if (depth = 4) {
        // 係を選択した時に対象のitemを表示
        div.addEventListener('click', (e) => {
            e.stopPropagation();
            selectSection(div, subsection.id, subsection.name, factoryName, departmentName, sectionName);
        });

    }


    li.appendChild(div);
    return li;
}

