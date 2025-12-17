odoo.define('sales_dashboard.dashboard', function (require) {
    "use strict";

    var rpc = require('web.rpc');

    $(document).ready(function () {
        // Example static bar chart using Chart.js
        var ctx = document.getElementById('sales_chart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Monthly Sales',
                    data: [1200, 1900, 3000, 500, 2000, 3000],
                    backgroundColor: 'rgba(75, 192, 192, 0.6)'
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    });
});
