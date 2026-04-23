// let categories = [];
;

async function deleteData(event) {
    event.preventDefault();
    var row = event.target.closest('tr');
    // var 
    var categoryId = event.target.getAttribute('data-id');
    var snackbar = document.getElementById("snackbar");
    try {
        const response = await fetch(`/category?category_id=${categoryId}`,{
            method: 'DELETE'
        })
        const data = await response.json();
        if (response.status !== 200){
            snackbar.className = "show-error";
            snackbar.innerText = data.message || "An error occurred during deleting category.";
            setTimeout(function(){snackbar.className = snackbar.className.replace("show")}, 2000);
            return;
        }
        snackbar.className = "show-success";
        snackbar.innerText = data.message || "Category deleted successfully!";
        setTimeout(function(){snackbar.className = snackbar.className.replace("show-success")}, 2000);
        row.remove()
    } catch (error){
        snackbar.className = "show-error";
        snackbar.innerText = "An error occurred during deleting category.";
        setTimeout(function(){snackbar.className = snackbar.className.replace("show")})
    }
}

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
        // console.log(response);
        if (response.status !== 200) {
            snackbar.className = "show-error";
            snackbar.innerText = data.message || "An error occurred during adding category.";
            setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
            return;
        }

        new_date = data.date || date;
        snackbar.className = "show-success";
        snackbar.innerText = data.message || "Category added successfully!";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-success", ""); }, 2000);
         row.innerHTML = `
            <td>${table.rows.length - 1}</td>
            <td>${name}</td>
            <td>${new_date}</td>
            <td><button onclick="deleteData(event)" class="delete-button" data-id="${data.category_id}">Delete</button></td>
        `;
    }catch (error) {
        snackbar.className = "show-error";
        snackbar.innerText = "An error occurred";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;
    }

    closeForm();
}