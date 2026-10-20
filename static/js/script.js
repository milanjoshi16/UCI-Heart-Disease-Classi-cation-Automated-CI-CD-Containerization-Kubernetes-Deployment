document.addEventListener("DOMContentLoaded", function () {
    if (typeof chartLabels !== 'undefined' && chartLabels.length > 0) {
        
        // Chart 1: Top Feature Importances (Bar)
        new Chart(document.getElementById('featureImpactChart').getContext('2d'), {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Model Feature Weight (%)',
                    data: chartValues,
                    backgroundColor: '#7c3aed',
                    borderRadius: 4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        // Chart 2: Advanced Statistical Scatter Plot (Seaborn Style - Input Value vs Weight)
        new Chart(document.getElementById('advancedScatterChart').getContext('2d'), {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Patient Input vs Model Weight',
                    data: scatterX.map((x, i) => ({ x: x, y: scatterY[i] })),
                    backgroundColor: '#db2777',
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: 'Patient Physiological Value' } },
                    y: { title: { display: true, text: 'Importance Weight (%)' } }
                }
            }
        });

        // Chart 3: Clinical Trend Line Chart (Seaborn Line/Trend Style)
        new Chart(document.getElementById('advancedTrendChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: trendLabels,
                datasets: [{
                    label: 'Patient Metrics',
                    data: trendPatientValues,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    fill: true,
                    tension: 0.3
                }, {
                    label: 'Normal Healthy Baseline',
                    data: trendNormalMeans,
                    borderColor: '#10b981',
                    borderDash: [5, 5],
                    fill: false
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        // Chart 4: Primary Risk Share Pie Chart
        new Chart(document.getElementById('riskFactorPieChart').getContext('2d'), {
            type: 'pie',
            data: {
                labels: chartLabels.slice(0, 3),
                datasets: [{
                    data: chartValues.slice(0, 3),
                    backgroundColor: ['#ef4444', '#f59e0b', '#8b5cf6']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
        });
    }
});