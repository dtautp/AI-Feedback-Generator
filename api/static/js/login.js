function form_submition(){
    let form = document.getElementById('form');
    let error_label = document.getElementById('error_code');
    if(error_label.textContent=='Multiples sesiones encontradas. Si inicia sesión aquí, las demás se cerrarán.'){
        let currentAction = form.getAttribute('action');
        form.setAttribute('action', currentAction + "?close_multi_session_confirmation=" + 1);
    }
    form.submit();
}
