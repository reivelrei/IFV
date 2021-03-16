
function onElementInserted(containerSelector, elementClass, callback) {
    let onMutationsObserved = function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                for (let element of mutation.addedNodes) {
                    if(element.classList !== undefined && element.classList.contains(elementClass)) {
                        callback(element);
                    }
                }
            }
        });
    };

    let target = document.querySelector(containerSelector);
    let MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
    let observer = new MutationObserver(onMutationsObserved);
    let config = { childList: true, subtree: true };
    observer.observe(target, config);

}


function showLoader(){
    let el = document.getElementById('loader')
    el.classList.remove('hide')
}

let isFirstLoading = true;
function hideLoader(){
    setTimeout(()=>{
        let el = document.getElementById('loader')
        el.classList.add('hide')
        isFirstLoading = false;
    }, isFirstLoading ? 3000 : 500);

}

onElementInserted('body', '_dash-loading-callback', element => {
    showLoader()
});