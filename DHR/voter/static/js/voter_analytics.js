// Define API endpoint
const API_URL = 'http://127.0.0.1:8000/voter_analytics/';

// Fetch data from the Django API
async function fetchVoterData() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();

        // Update text values
        document.getElementById('totalVoters').textContent = data.total_voters;
        document.getElementById('checkedTrue').textContent = data.checked_true_count;
        document.getElementById('checkedFalse').textContent = data.checked_false_count;

        // Render the pie chart
        renderChart(data.checked_true, data.checked_false);
    } catch (error) {
        console.error('Error fetching voter data:', error);
    }
}

// Render the pie chart using Chart.js
function renderChart(checkedTrue, checkedFalse) {
    const ctx = document.getElementById('voterChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Checked True', 'Checked False'],
            datasets: [{
                data: [checkedTrue, checkedFalse],
                backgroundColor: ['#4caf50', '#f44336'],
                hoverBackgroundColor: ['#45a049', '#e53935'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.raw;
                            return label;
                        }
                    }
                }
            }
        }
    });
}

// Call the fetch function when the page loads
document.addEventListener('DOMContentLoaded', fetchVoterData);
console.log(Chart);

