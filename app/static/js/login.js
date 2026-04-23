window.addEventListener('pageshow', (event) => {
    if (event.persisted){
        window.location.reload();
    }
})


async function submitCredentials(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    const response = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, password: password})
    });

    try {
    const data = await response.json();
    if (response.status !== 200){
        snackbar.className = "show-error";
        snackbar.innerText = data.message || "Login failed. Please try again.";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;
    }
    snackbar.className = "show-success";
    snackbar.innerText = data.message || "Login successful!";
    document.body.classList.add("is-loading")
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show-success", ""); }, 2000);
    setTimeout(function(){ window.location.href = "/expense" },2000);
    
    } catch (error){
        snackbar.className = "show-error";
        snackbar.innerText =  "An Error occurred";
        console.error(error);
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;

    } 
}