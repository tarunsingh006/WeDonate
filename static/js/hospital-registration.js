function checkpassword() {
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var submitBtn = document.getElementById('submit');
    var msgElement = document.getElementById('password-validation-msg');
    
    if (password1 && password2) {
        if (password1 === password2) {
            msgElement.innerHTML = '<span style="color: green;">Passwords match!</span>';
            submitBtn.disabled = false;
        } else {
            msgElement.innerHTML = '<span style="color: red;">Passwords do not match!</span>';
            submitBtn.disabled = true;
        }
    } else {
        msgElement.innerHTML = '';
        submitBtn.disabled = true;
    }
}

// Enable button when all required fields are filled
function checkForm() {
    var hospitalName = document.querySelector('input[name="hospital_name"]').value;
    var email = document.querySelector('input[name="email"]').value;
    var username = document.querySelector('input[name="username"]').value;
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var submitBtn = document.getElementById('submit');
    
    if (hospitalName && email && username && password1 && password2 && password1 === password2) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    var inputs = document.querySelectorAll('input[required]');
    inputs.forEach(function(input) {
        input.addEventListener('input', checkForm);
    });
    
    document.getElementById('password2').addEventListener('input', checkpassword);
});