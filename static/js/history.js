document.addEventListener('DOMContentLoaded', function() {
    const socket = io({
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 2000,
        reconnectionDelayMax: 5000,
        timeout: 20000
    });

    // Parse history data from the template
    const historyData = JSON.parse(document.getElementById('history-data')?.getAttribute('data-history') || '[]');

    // Initialize charts
    initializeTrendChart();
    initializeDistributionChart();
    updateStatistics();

    // Initialize search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    // Time range filter
    const timeRangeSelect = document.getElementById('time-range');
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', handleTimeRangeChange);
    }

    // Export functionality
    const exportBtn = document.getElementById('export-data');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportData);
    }

    // Clear history functionality
    const clearHistoryBtn = document.getElementById('clear-history');
    const clearHistoryModal = document.getElementById('clear-history-modal');
    const confirmClearBtn = document.getElementById('confirm-clear');
    const cancelClearBtn = document.getElementById('cancel-clear');
    const closeModalBtn = document.querySelector('.close');

    if (clearHistoryBtn) {
        clearHistoryBtn.onclick = () => clearHistoryModal.style.display = 'block';
    }

    if (cancelClearBtn) {
        cancelClearBtn.onclick = () => clearHistoryModal.style.display = 'none';
    }

    if (closeModalBtn) {
        closeModalBtn.onclick = () => clearHistoryModal.style.display = 'none';
    }

    if (confirmClearBtn) {
        confirmClearBtn.onclick = clearHistory;
    }

    window.onclick = function(event) {
        if (event.target == clearHistoryModal) {
            clearHistoryModal.style.display = 'none';
        }
    }

    // Initialize trend chart
    function initializeTrendChart() {
        const chartData = prepareChartData();
        const layout = {
            template: 'plotly_dark',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            showlegend: true,
            legend: {
                orientation: 'h',
                y: -0.2
            },
            margin: { t: 10, r: 10, b: 50, l: 50 },
            xaxis: {
                showgrid: true,
                gridcolor: 'rgba(255,255,255,0.1)',
                title: 'Time'
            },
            yaxis: {
                showgrid: true,
                gridcolor: 'rgba(255,255,255,0.1)',
                title: 'Angle (degrees)'
            }
        };

        Plotly.newPlot('trend-chart', chartData, layout);
    }

    // Initialize distribution chart
    function initializeDistributionChart() {
        const { shoulderAngles, hipAngles, tiltAngles } = getAnglesArrays();

        const data = [
            {
                type: 'violin',
                x: shoulderAngles,
                name: 'Shoulder',
                side: 'positive',
                line: { color: '#1890ff' }
            },
            {
                type: 'violin',
                x: hipAngles,
                name: 'Hip',
                side: 'positive',
                line: { color: '#52c41a' }
            },
            {
                type: 'violin',
                x: tiltAngles,
                name: 'Tilt',
                side: 'positive',
                line: { color: '#faad14' }
            }
        ];

        const layout = {
            template: 'plotly_dark',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            showlegend: true,
            legend: {
                orientation: 'h',
                y: -0.2
            },
            margin: { t: 10, r: 10, b: 50, l: 50 },
            xaxis: {
                title: 'Angle (degrees)',
                showgrid: true,
                gridcolor: 'rgba(255,255,255,0.1)'
            },
            yaxis: {
                showticklabels: false,
                showgrid: false
            }
        };

        Plotly.newPlot('distribution-chart', data, layout);
    }

    function prepareChartData() {
        return [
            {
                name: 'Shoulder Angle',
                x: historyData.map(record => record.timestamp),
                y: historyData.map(record => record.measurements.shoulder_angle),
                type: 'scatter',
                mode: 'lines',
                line: { color: '#1890ff', shape: 'spline' }
            },
            {
                name: 'Hip Angle',
                x: historyData.map(record => record.timestamp),
                y: historyData.map(record => record.measurements.hip_angle),
                type: 'scatter',
                mode: 'lines',
                line: { color: '#52c41a', shape: 'spline' }
            },
            {
                name: 'Frame Tilt',
                x: historyData.map(record => record.timestamp),
                y: historyData.map(record => record.measurements.tilt_angle),
                type: 'scatter',
                mode: 'lines',
                line: { color: '#faad14', shape: 'spline' }
            }
        ];
    }

    function getAnglesArrays() {
        return {
            shoulderAngles: historyData.map(record => record.measurements.shoulder_angle),
            hipAngles: historyData.map(record => record.measurements.hip_angle),
            tiltAngles: historyData.map(record => record.measurements.tilt_angle)
        };
    }

    function updateStatistics() {
        const { shoulderAngles, hipAngles, tiltAngles } = getAnglesArrays();

        // Calculate averages
        const avgShoulder = calculateAverage(shoulderAngles);
        const avgHip = calculateAverage(hipAngles);
        const avgTilt = calculateAverage(tiltAngles);

        // Calculate trends
        const shoulderTrend = calculateTrend(shoulderAngles);
        const hipTrend = calculateTrend(hipAngles);
        const tiltTrend = calculateTrend(tiltAngles);

        // Update UI
        updateStatCard('avg-shoulder', avgShoulder.toFixed(1) + '°', shoulderTrend);
        updateStatCard('avg-hip', avgHip.toFixed(1) + '°', hipTrend);

        // Calculate and update posture score
        const goodPostures = historyData.filter(record =>
            Math.abs(record.measurements.shoulder_angle) <= 5 &&
            Math.abs(record.measurements.hip_angle) <= 5 &&
            Math.abs(record.measurements.tilt_angle) <= 2
        ).length;

        const score = (goodPostures / historyData.length * 100) || 0;
        document.getElementById('posture-score').textContent = score.toFixed(0) + '%';
    }

    function calculateAverage(array) {
        return array.length ? array.reduce((a, b) => a + Math.abs(b), 0) / array.length : 0;
    }

    function calculateTrend(array) {
        if (array.length < 2) return 'neutral';
        const halfLength = Math.floor(array.length / 2);
        const firstHalf = array.slice(0, halfLength);
        const secondHalf = array.slice(halfLength);
        const firstAvg = calculateAverage(firstHalf);
        const secondAvg = calculateAverage(secondHalf);
        return secondAvg < firstAvg ? 'down' : secondAvg > firstAvg ? 'up' : 'neutral';
    }

    function updateStatCard(id, value, trend) {
        const valueElement = document.getElementById(id);
        const trendElement = document.getElementById(id.replace('avg-', '') + '-trend');

        if (valueElement) valueElement.textContent = value;

        if (trendElement) {
            const trendIcon = trendElement.querySelector('.trend-icon');
            const trendText = trendElement.querySelector('.trend-text');

            if (trendIcon) {
                trendIcon.className = 'trend-icon ' + trend;
                trendIcon.innerHTML = trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→';
            }

            if (trendText) {
                trendText.textContent = trend === 'up' ? 'Increasing' : trend === 'down' ? 'Decreasing' : 'Stable';
            }
        }
    }

    function handleSearch(event) {
        const searchTerm = event.target.value.toLowerCase();
        const tbody = document.getElementById('history-table-body');

        if (!tbody) return;

        const rows = tbody.getElementsByTagName('tr');

        for (const row of rows) {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        }
    }

    function handleTimeRangeChange(event) {
        const timeRange = event.target.value;
        const now = new Date();
        let filteredData;

        switch(timeRange) {
            case '1h':
                filteredData = filterDataByTime(1);
                break;
            case '6h':
                filteredData = filterDataByTime(6);
                break;
            case '24h':
                filteredData = filterDataByTime(24);
                break;
            case '7d':
                filteredData = filterDataByTime(168);
                break;
            default:
                filteredData = historyData;
        }

        updateCharts(filteredData);
    }

    function filterDataByTime(hours) {
        const cutoff = new Date();
        cutoff.setHours(cutoff.getHours() - hours);
        return historyData.filter(record => new Date(record.timestamp) > cutoff);
    }

    function updateCharts(data) {
        // Update trend chart
        const update = {
            x: [
                data.map(record => record.timestamp),
                data.map(record => record.timestamp),
                data.map(record => record.timestamp)
            ],
            y: [
                data.map(record => record.measurements.shoulder_angle),
                data.map(record => record.measurements.hip_angle),
                data.map(record => record.measurements.tilt_angle)
            ]
        };

        Plotly.update('trend-chart', update);

        // Update distribution chart
        const distUpdate = {
            x: [
                data.map(record => record.measurements.shoulder_angle),
                data.map(record => record.measurements.hip_angle),
                data.map(record => record.measurements.tilt_angle)
            ]
        };

        Plotly.update('distribution-chart', distUpdate);
    }

    function exportData() {
        const data = historyData.map(record => ({
            timestamp: record.timestamp,
            shoulder_angle: record.measurements.shoulder_angle,
            hip_angle: record.measurements.hip_angle,
            tilt_angle: record.measurements.tilt_angle
        }));

        const csv = convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `posture_history_${new Date().toISOString().slice(0,10)}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }

    function convertToCSV(data) {
        const headers = Object.keys(data[0]);
        const rows = data.map(obj => headers.map(header => obj[header]));
        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }

    async function clearHistory() {
        try {
            const response = await fetch('/clear_history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                window.location.reload();
            } else {
                throw new Error('Failed to clear history');
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            alert('Failed to clear history. Please try again.');
        }
        document.getElementById('clear-history-modal').style.display = 'none';
    }

    // Handle real-time updates
    socket.on('measurements', function(data) {
        // Add new measurement to history
        const newRecord = {
            timestamp: new Date().toISOString(),
            measurements: {
                shoulder_angle: data.shoulder_angle,
                hip_angle: data.hip_angle,
                tilt_angle: data.tilt_angle
            }
        };

        historyData.push(newRecord);

        // Keep only last 100 records
        if (historyData.length > 100) {
            historyData.shift();
        }

        // Update charts and statistics
        updateCharts(historyData);
        updateStatistics();
    });
});
