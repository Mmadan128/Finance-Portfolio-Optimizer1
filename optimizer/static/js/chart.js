// Include Chart.js via CDN in the HTML <head> or at the bottom of the HTML before the closing </body> tag
// <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

// Function to initialize the asset allocation pie chart
function initializeAssetAllocationChart() {
    var ctx = document.getElementById('assetChart').getContext('2d');

    var assetChart = new Chart(ctx, {
        type: 'pie', // Pie chart for Asset Allocation
        data: {
            labels: ['Stocks', 'Bonds', 'Real Estate'],
            datasets: [{
                label: 'Asset Allocation',
                data: [40, 35, 25], // You can dynamically update this data
                backgroundColor: ['#36A2EB', '#FFCE56', '#FF6384'],
                hoverBackgroundColor: ['#36A2EB', '#FFCE56', '#FF6384'],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top', // Position of the legend
                    labels: {
                        color: '#333' // Legend text color
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + '%';
                        }
                    }
                }
            }
        }
    });
}

// Function to initialize other charts (if needed)
function initializeOtherCharts() {
    var ctxBar = document.getElementById('barChart').getContext('2d');

    var barChart = new Chart(ctxBar, {
        type: 'bar', // Example bar chart for performance tracking
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Portfolio Performance',
                data: [5, 10, 8, 12, 9, 15], // Portfolio performance data over time
                backgroundColor: '#36A2EB'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#333' // Axis label color
                    }
                },
                x: {
                    ticks: {
                        color: '#333' // Axis label color
                    }
                }
            }
        }
    });
}

// Function to handle sidebar interactivity (optional)
function setupSidebarInteractivity() {
    const sidebarLinks = document.querySelectorAll('.sidebar ul li');

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remove active class from all links
            sidebarLinks.forEach(item => item.classList.remove('active'));
            // Add active class to the clicked link
            this.classList.add('active');

            // You can add interactivity here to switch between views, charts, or stats
            console.log(this.textContent + ' clicked');
        });
    });
}

// Initialize charts and interactivity when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAssetAllocationChart();
    setupSidebarInteractivity();
    initializeOtherCharts(); // If more charts are added
});
