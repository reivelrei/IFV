
function showControls(folding, logswitch, heatmap){
    showfolding(folding);
    showlogswitch(logswitch);
    showheatmap(heatmap);

}

function showfolding(show){
    let el = document.getElementById('labelFolding');
    let cl = document.getElementById('folding_select');
    if(show) {
        el.classList.remove('hide');
        cl.classList.remove('hide');
    }else{
         el.classList.add('hide');
        cl.classList.add('hide');
    }

}

function showlogswitch(show){
    let el = document.getElementById('loader');
     if(show) {
         el.classList.remove('hide');
    }else{
         el.classList.add('hide');
    }
}

function showheatmap(show){
    let el = document.getElementById('labelHeatmap');
    let cl = document.getElementById('heatmap');
     if(show) {
         el.classList.remove('hide');
         cl.classList.remove('hide');
    }else{
         el.classList.add('hide');
         cl.classList.add('hide');
    }
}