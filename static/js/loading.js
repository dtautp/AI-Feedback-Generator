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

async function fetchCounterSemaphoreValue() {
    let progressBar = document.getElementById('Progress');
    let progressBar_v2 = document.getElementById('Progress_v2');
    try {
        const response = await fetch('/get-counter-semaphore');
        const data = await response.json();
        
        // progressBar.value = data.counter_semaphore_value;
        if(data.counter_semaphore_value>=progressBar.value){
            progressBar.value = data.counter_semaphore_value;
            progressBar_v2.style.width = data.counter_semaphore_value/data.total_docs*100 + "%";
            document.getElementById('counterValue').textContent = data.counter_semaphore_value;
        }
        
    } catch (error) {
        console.error('Error fetching counter semaphore value:', error);
    }
}

window.onload = function(){
    carrucel();
    setInterval(carrucel, 21850);
    document.getElementById("form").submit();
    fetchCounterSemaphoreValue();
    setInterval(fetchCounterSemaphoreValue, 100); //
};