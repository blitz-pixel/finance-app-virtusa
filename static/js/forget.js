function passwordValidator(newPasswordTag, button,para) {
    newPasswordTag.style.borderStyle = 'solid';
    newPasswordTag.style.borderWidth = '2px';
    const regex =/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
    newPasswordTag.addEventListener('input', () => {
        if(regex.test(newPasswordTag.value)) {
            newPasswordTag.style.borderColor = 'green';
            button.disabled = false;
        } else {
            newPasswordTag.style.borderColor = 'red';
            button.disabled = true;
            para.innerHTML +=  `<small style="color: red;">
            Password must be at least 8 characters long and include at least one uppercase letter,
            one lowercase letter, one number, and one special character.</small>`;

        }
    })
    
}


function resetPassword(event) {
    event.preventDefault();
    var form = document.getElementById('forget-form');
    var emailTag = form.elements['email'];
    var para = form.querySelector('p');
    var button = form.querySelector('button');
   
    fetch('/forgot_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailTag.value })
    })
    .then( (response) => {
        if (response.status === 200){
                button.innerText = "Confirm New Password"; 
                button.disabled = true;
                
                para.innerHTML = `
                    <input type="password" name="new_password" id="new_password" 
                    placeholder="Enter new password" required><br>
                `;
                
                var newPasswordTag = form.elements['new_password'];
                passwordValidator(newPasswordTag, button, para);
        
                // button.innerText = "Confirm New Password"; 
                // button.disabled = true;
                
                // para.innerHTML = `
                //     <input type="password" name="new_password" id="new_password" placeholder="Enter new password" required><br>
                // `;
                
                // var newPasswordTag = form.elements['new_password'];
                // passwordValidator(newPasswordTag, button);
                // newPasswordTag.addEventListener('input',() => {
                //     if (newPasswordTag.value.trim().length > 0) {
                //         button.disabled = false;
                //     } else {
                //         button.disabled = true;
                //     }
                // });
        }
    }).catch( (error) => console.error(error));
}

