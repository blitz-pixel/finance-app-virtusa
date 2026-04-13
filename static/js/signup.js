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
    // event.preventDefault();
    console.log(" function called");
    var passwordTag = document.getElementById('password');
    var para = document.getElementById('password-para');
    var button = document.querySelector('button');
    passwordValidator(passwordTag, para, button);
}

function checkConfirmPassword() {
    console.log("checkConfirmPassword function called");
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
function submitForm(event) {
    event.preventDefault();
    console.log(event.defaultPrevented);
    console.log("submitForm function called");
    
    var form = document.querySelector('form');
    var username = form.elements['username'].value;
    var email = form.elements['email'].value;
    var password = form.elements['password'].value;
    var confirm_password = form.elements['confirm_password'].value;
    
    console.log(username, email, password);
    
    fetch('/signup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
        })
    }).then(data => {
          console.log('Success:', data);
          form.reset();
      }).catch(error => {
          console.error('Error:', error);
      });
}