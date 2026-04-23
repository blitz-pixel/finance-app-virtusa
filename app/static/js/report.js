
let monthlyExpenseChart = null;
let yearlyExpenseChart = null;
let monthlyCatChart = null;
let yearlyCatChart = null;
let pieChart = null;

const COLORS = [
    'rgba(65, 175, 170, 0.75)',
    'rgba(70, 110, 180, 0.75)',
    'rgba(0, 160, 225, 0.75)',
    'rgba(230, 165, 50, 0.75)',
    'rgba(215, 100, 44, 0.75)',
    'rgba(175, 75, 145, 0.75)'
];

function shuffledColors() {
    const palette = [...COLORS];
    for (let i = palette.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [palette[i], palette[j]] = [palette[j], palette[i]];
    }
    return palette;
}

function destroyChart(chartInstance) {
    if (chartInstance) {
        chartInstance.destroy();
    }
}

function monthLabel(month, year) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[month - 1]} ${year}`;
}

function categoryChart(rows, frequency) {
    var labels = [];
    var categoryMap = new Map();
    const palette = shuffledColors();

    rows.forEach((row) => {
        const frequencyLabel = frequency ===  "month" ? monthLabel(row.month, row.year) : String(row.year);
        if (!labels.includes(frequencyLabel)) {
            labels.push(frequencyLabel);
        }

        if (!categoryMap.has(row.category_name)) {
            categoryMap.set(row.category_name, new Map());
        }
        categoryMap.get(row.category_name).set(frequencyLabel, row.totalAmount);
    });

    const dataset = Array.from(categoryMap.entries()).map(([categoryName, values], index) => ({
        label: categoryName,
        data: labels.map((label) => values.get(label) || 0),
        backgroundColor: palette[index % palette.length],
        borderColor: palette[index % palette.length].replace('0.75', '1'),
        borderWidth: 1,
    }));

    return { labels, datasets: dataset };
}

function PieChart(rows, selectedCategory) {
    var labels = [];
    var values = [];
    const palette = shuffledColors();

    if (selectedCategory) {
        const output = rows.filter((row) => row.category_name === selectedCategory);
        labels = output.map((row) => String(row.year));
        values = output.map((row) => row.totalAmount);
    } else {
        const categoryTotals = new Map();
        rows.forEach((row) => {
            categoryTotals.set(row.category_name, (categoryTotals.get(row.category_name) || 0) + row.totalAmount);
        });
        labels = Array.from(categoryTotals.keys());
        values = Array.from(categoryTotals.values());
    }

    return {
        labels,
        datasets: [{
            label: selectedCategory || 'All Categories',
            data: values,
            backgroundColor: labels.map((_, index) => palette[index % palette.length]),
             borderColor: labels.map((_, index) => palette[index % palette.length].replace('0.75', '1')),
            borderWidth: 2,
        }]
    };
}

function yearlySummary(yearlyRows, selectedCategory) {
    const summaryContainer = document.getElementById('yearlySummary');
    if (!summaryContainer) {
        return;
    }

    const yearlyMap = new Map();
    yearlyRows
        .filter((row) => !selectedCategory || row.category_name === selectedCategory)
        .forEach((row) => {
            yearlyMap.set(row.year, (yearlyMap.get(row.year) || 0) + row.totalAmount);
        });

    const sortedYears = Array.from(yearlyMap.keys()).sort((a, b) => a - b);
    summaryContainer.innerHTML = sortedYears.length
        ? sortedYears.map((year) => `
            <div class="summary-row">
                <span class="summary-year">${year}</span>
                <span class="summary-value">₹${yearlyMap.get(year).toFixed(2)}</span>
            </div>
        `).join('')
        : '<div class="summary-row"><span class="summary-year">No data</span><span class="summary-value">₹0.00</span></div>';
}

async function generateGraphs(event){
    event.preventDefault();

    const category = document.getElementById('category').value || null;

    let data = {};
    try{
        const response = await fetch('/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category: category })
        });
        data = await response.json();
        if (response.status !== 200){
            // snackbar.className = "show-error";
            // snackbar.innerText = data.message || "Failed to fetch data. Please try again.";
            // setTimeout(function(){snackbar.className = snackbar.className.replace("show-error", ""); }, 2000);
            return;
        }

    } catch (error){
        // snackbar.className = "show-error";
        // snackbar.innerText = "Erro Occured"
        // setTimeout(function(){snackbar.className = snackbar.className.replace("show-error","");},2000)
        return;
    }

    destroyChart(monthlyExpenseChart);
    destroyChart(yearlyExpenseChart);
    destroyChart(monthlyCatChart);
    destroyChart(yearlyCatChart);
    destroyChart(pieChart);

    const selectedCategory = category && category !== '' ? category : null;

    const monthlyCategoryData = categoryChart(
        selectedCategory
            ? data.monthly_category_totals.filter((row) => row.category_name === selectedCategory)
            : data.monthly_category_totals,
        'month'
    );
    monthlyCatChart = new Chart(document.getElementById('monthlyCategoryChart').getContext('2d'), {
        type: 'bar',
        data: monthlyCategoryData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    ticks: { color: '#e0e0e0', font: { size: 15, family: 'Times New Roman' } },
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        color : ' #e0e0e0',
                        font: { size: 16, family: 'Times New Roman' },
                        callback: function(value) {
                            return '₹' + value;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: selectedCategory ? `Monthly Category Data - ${selectedCategory}` : 'Monthly Category Data',
                    color: '#e0e0e0',
                    font: { size: 18, family: 'Times New Roman' }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#e0e0e0',
                        font: { size: 17, family: 'Times New Roman' }
                    }
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.y ?? 0;
                            return `${context.dataset.label}: ₹${value}`;
                        }
                    }
                }
            }
        }
    });

    const yearlyCategoryData = categoryChart(
        selectedCategory
            ? data.yearly_category_totals.filter((row) => row.category_name === selectedCategory)
            : data.yearly_category_totals,
        'year'
    );
    yearlyCatChart = new Chart(document.getElementById('yearlyCategoryChart').getContext('2d'), {
        type: 'bar',
        data: yearlyCategoryData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: { ticks: { color: ' #e0e0e0', font: { size: 15, family: 'Times New Roman' } },
                stacked: true },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        color: ' #e0e0e0',
                        font: { size: 16, family: 'Times New Roman' },
                        callback: function(value) {
                            return '₹' + value;
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: selectedCategory ? `Yearly Category Data - ${selectedCategory} ` : 'Yearly Category Data',
                    color: '#e0e0e0',
                     font: { size: 18, family: 'Times New Roman' }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                     labels: {
                        color: '#e0e0e0',
                        font: { size: 17, family: 'Times New Roman' }
                    }
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.y ?? 0;
                            return `${context.dataset.label}: ₹${value}`;
                        }
                    }
                }
            }
        }
    });

    const pieData = PieChart(data.yearly_category_totals, selectedCategory);
    pieChart = new Chart(document.getElementById('pieCategoryChart').getContext('2d'), {
        type: 'pie',
        data: pieData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: selectedCategory ? `Category Split - ${selectedCategory} (Yearly data)` : 'Category Split - All Categories (Yearly data)',
                    color: '#e0e0e0',
                    font: { size: 18, family: 'Times New Roman' }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                     labels: {
                        color: '#e0e0e0',
                        font: { size: 18, family: 'Times New Roman' }
                    }
                }
            }
        }
    });

    yearlySummary(data.yearly_category_totals, selectedCategory);
}