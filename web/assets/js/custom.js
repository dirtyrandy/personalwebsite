function form_submission() {
    document.getElementById('submit').disabled = true;
}

function captcha_callback(response) {
    document.getElementById('submit').disabled = false;
}