let categories = [];

function addCategory() {
    var name = document.getElementById("name").value;
    var date = document.getElementById("date").value;

    var table = document.getElementById("data-table");
    var row = table.insertRow();

    row.innerHTML = `
        <td>${table.rows.length}</td>
        <td>${name}</td>
        <td>${date}</td>
    `;

    fetch("/add_category", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body : JSON.stringify({name, date})
    }).then(response => response.json())
        .then(data => console.log("Category added:", data))
        .catch(error => console.error("Error :", error));

    closeForm();
}