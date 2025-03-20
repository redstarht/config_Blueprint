export function toggleTree(ul,div){
    const icon = div.querySelector('i');
    
    if (ul.style.display === 'none'){
        ul.style.display == 'block';
        icon.className = 'bi bi-caret-down-fill me-2';
    }else{
        ul.style.display = 'none'
        icon.className = 'bi bi-caret-right-fill me-2';
    }
    }

    export function createTreeItem(name){
        const div = document.createElement('div');
        div.className= 'tree-item';
        div.innerHTML = `<i class="bi bi-caret-right-fill me-2"></i>${name}`;
        return div;
    }