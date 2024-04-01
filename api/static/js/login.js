function form_submition(){
    let loadingImg = document.getElementById("loading_img");
    loadingImg.style.display = "inline-block";
    let form = document.getElementById('form');
    form.submit();
}

function show_modal(){
    $('#multiSessionsModal').modal('show');
}

const button = document.getElementById('login-button');
button.addEventListener('click', function(event) {
    event.preventDefault();
    
    let loadingImg = document.getElementById("loading_img");
    loadingImg.style.display = "inline-block";

    let postData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    };

    fetch('/user_cheking', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response:', data);
            console.log(data);
            if(data['response']==400){
                let error_code = data['error_code'];
                if(error_code=='login_fail'){
                    loadingImg.style.display = "none";
                    document.getElementById('error_code').textContent = 'Usuario o contraseña incorrectos'
                }
                if(error_code=='multi_login'){
                    loadingImg.style.display = "none";
                    $('#multiSessionsModal').modal('show');
                }
            }
            if(data['response']==200){
                form_submition();
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});


