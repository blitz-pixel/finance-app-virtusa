let expenses = [];

function addExpense() {
    var name = document.getElementById("name").value;
    var category = document.getElementById("category").value;
    var amount = document.getElementById("amount").value;
    var date = document.getElementById("date").value;

    var table = document.getElementById("data-table");
    var row = table.insertRow();

    row.innerHTML = `
        <td>${table.rows.length - 1}</td>
        <td>${name}</td>
        <td>${category}</td>
        <td>${amount}</td>
        <td>${date}</td>
    `;

    fetch("/add_expense", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body : JSON.stringify({name, category, amount, date})
    }).then(response => response.json())
        .then(data => console.log("Expense added:", data))
        .catch(error => console.error("Error adding expense:", error));

    closeForm();
}