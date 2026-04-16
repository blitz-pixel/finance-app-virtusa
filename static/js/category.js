let categories = [];

async function addCategory(event) {
    event.preventDefault();
    var name = document.getElementById("name").value;
    var date = document.getElementById("date").value || new Date().toISOString().split('T')[0];

    var table = document.getElementById("data-table");
    var snackbar = document.getElementById("snackbar");
    var row = table.insertRow();

    try {
        const response = await fetch("/category", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({name, date})
        });
        const data = await response.json();
        console.log(response);
        if (response.status !== 200) {
            snackbar.className = "show-error";
            snackbar.innerText = data.message || "An error occurred during adding category.";
            setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
            return;
        }

        snackbar.className = "show-success";
        snackbar.innerText = data.message || "Category added successfully!";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-success", ""); }, 2000);
         row.innerHTML = `
            <td>${table.rows.length}</td>
            <td>${name}</td>
            <td>${date}</td>
        `;
    }catch (error) {
        snackbar.className = "show-error";
        snackbar.innerText = "An error occurred";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;
    }

    closeForm();
}