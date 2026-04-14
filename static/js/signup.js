window.addEventListener('pageshow', (event) => {
    if (event.persisted){
        window.location.reload();
    }
})



function passwordValidator(newPasswordTag, para, button) {
    newPasswordTag.style.borderStyle = 'solid';
    newPasswordTag.style.borderWidth = '2px';
    const regex =/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
    newPasswordTag.addEventListener('input', () => {
        if(regex.test(newPasswordTag.value)) {
            newPasswordTag.style.borderColor = 'green';
            para.innerHTML = '';
            button.disabled = false;
        } else {
            newPasswordTag.style.borderColor = 'red';
            para.innerHTML =  `<small style="color: red;">
            Password must be at least 8 characters long and include at least one uppercase letter,
            one lowercase letter, one number, and one special character.</small>`;
            button.disabled = true;
        }
    })
    
}


function checkPassword() {
    // console.log("checkPassword function called");
    var passwordTag = document.getElementById('password');
    var para = document.getElementById('password-para');
    var button = document.querySelector('button');
    passwordValidator(passwordTag, para, button);
}

function checkConfirmPassword() {
    // console.log("checkConfirmPassword function called");
    var passwordTag = document.getElementById('password');
    var confirmPasswordTag = document.getElementById('confirm_password');
    var para = document.getElementById('confirm-password-para');
    var button = document.querySelector('button');
     confirmPasswordTag.addEventListener('input', () => {
        if (confirmPasswordTag.value !== passwordTag.value) {
               para.innerHTML = `<small style="color: red;">Passwords do not match.</small>`;
               button.disabled = true;
        } else {
            para.innerHTML = '';
            button.disabled = false;
        }});
    }

async function submitForm(event) {
    event.preventDefault();
    // console.log("submitForm function called");
    
    var form = document.querySelector('form');
    var username = form.elements['username'].value;
    var email = form.elements['email'].value;
    var password = form.elements['password'].value;
    var confirm_password = form.elements['confirm_password'].value;
    var snackbar = document.getElementById("snackbar");

    if (password !== confirm_password) {
        snackbar.className = "show-error";
        snackbar.innerText = "Passwords do not match.";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 3000);
        return;
    }
    
    const response = await fetch('/signup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
        })
    });

    try {
    const data = await response.json();
    if (response.status !== 200) {
        snackbar.className = "show-error";
        snackbar.innerText = data.message || "An error occurred during registration";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;
    }
    snackbar.className = "show-success";
    snackbar.innerText = data.message || "User registered successfully";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show-success", ""); }, 2000);
    setTimeout(function(){ window.location.href = '/expense'; }, 1000);   // dummy redirect
    } catch (error) {
        snackbar.className = "show-error";
        snackbar.innerText = "An error occurred during registration";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;
    }
}