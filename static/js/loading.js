var gifPaths = ["animation-loading-1.gif", "animation-loading-2.gif", "animation-loading-3.gif", "animation-loading-4.gif", "animation-loading-5.gif"];
var img = document.getElementById("gifDisplay")
function carrucel(){
    img.src = "/static/img/"+gifPaths[0]
    setTimeout(function(){
        img.src = "/static/img/"+gifPaths[1]
    },3750);
    setTimeout(function(){
        img.src = "/static/img/"+gifPaths[2]
    },3800+4500);
    setTimeout(function(){
        img.src = "/static/img/"+gifPaths[3]
    },3800+(4500*2));
    setTimeout(function(){
        img.src = "/static/img/"+gifPaths[4]
    },3800+(4500*3));
}

var PROGRESO = 0;
function barra_progreso_definido(){
    let doc_number = document.getElementById('doc_number').textContent;
    let progressBar_v2 = document.getElementById('Progress_v2');
    if(PROGRESO <= doc_number){
        progressBar_v2.style.width = PROGRESO/doc_number*100 + "%";
        document.getElementById('counterValue').textContent = PROGRESO;
        PROGRESO++;
    }
    
    
}

window.onload = function(){
    carrucel();
    setInterval(carrucel, 21850);
    document.getElementById("form").submit();
    setInterval(barra_progreso_definido, 800);
};