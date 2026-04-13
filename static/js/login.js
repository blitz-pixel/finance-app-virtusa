function submitCredentials() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, password: password})
    })
}