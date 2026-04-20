// let expenses = [];

async function deleteData(event) {
    event.preventDefault();
    var row = event.target.closest('tr');
    // var 
    var expeseneId = event.target.getAttribute('data-id');
    var snackbar = document.getElementById("snackbar");
    try {
        const response = await fetch(`/expense?expense_id=${expeseneId}`,{
            method: 'DELETE'
        })
        const data = await response.json();
        if (response.status !== 200){
            snackbar.className = "show-error";
            snackbar.innerText = data.message || "An error occurred during deleting expesne.";
            setTimeout(function(){snackbar.className = snackbar.className.replace("show")}, 2000);
            return;
        }
        snackbar.className = "show-success";
        snackbar.innerText = data.message || "Expense deleted successfully!";
        setTimeout(function(){snackbar.className = snackbar.className.replace("show-success")}, 2000);
        row.remove()
    } catch (error){
        snackbar.className = "show-error";
        snackbar.innerText = "An error occurred during deleting expesne.";
        setTimeout(function(){snackbar.className = snackbar.className.replace("show")})
    }
}
async function addExpense(event) {
    event.preventDefault();
    var category = document.getElementById("category").value ;
    console.log(category);
    var amount = document.getElementById("amount").value;
    var date = document.getElementById("date").value;
    var description = document.getElementById("description").value || "A simple expense";
    var snackbar = document.getElementById("snackbar");
    var table = document.getElementById("data-table");
    var row = table.insertRow();

    try {
        const response = await fetch("/expense", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body : JSON.stringify({category, amount, date, description})
        });
        const data = await response.json();
        if (response.status !== 200) {
            snackbar.className = "show-error";
            snackbar.innerText = data.message || "An error occurred during adding expense.";
            setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
            return;
        }
        // new_date = data.get("date", date);
        console.log(data);
        snackbar.className = "show-success";
        new_date = data.date || date;
        snackbar.innerText = data.message || "Expense added successfully!";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-success", ""); }, 2000);

          row.innerHTML = `
            <td>${table.rows.length - 1}</td>
            <td>${amount}</td>
            <td>${category}</td>
            <td>${new_date}</td>
            <td>${description}</td>
            <td><button onclick="deleteData(event)" class="delete-button" data-id="${data.transaction_id}">Delete</button></td>
           
        `;
        
        // console.log("Expense added:", data);
    } catch (error) {
        snackbar.className = "show-error";
        snackbar.innerText = "An error occurred";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
        return;
    }

    closeForm();
}