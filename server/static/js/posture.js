document.addEventListener('DOMContentLoaded', function() {
    // Helper function to check if we're on a specific page
    function isOnPage(elementId) {
        return document.getElementById(elementId) !== null;
    }

    // Socket.IO configuration with improved connection handling
    const socket = io({
        reconnection: true,
        reconnectionAttempts: 10,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 20000,
        transports: ['websocket'],
        upgrade: false
    });

    // Loading overlay management
    const loadingOverlay = document.querySelector('.loading-overlay');
    const loadingText = document.querySelector('.loading-text');
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 10;

    function updateLoadingStatus(message, isError = false) {
        if (loadingOverlay && loadingText) {
            loadingText.innerHTML = message;
            if (isError) {
                loadingOverlay.classList.add('error');
            } else {
                loadingOverlay.classList.remove('error');
            }
        }
    }

    socket.on('connect', () => {
        console.log('Connected to server');
        reconnectAttempts = 0;
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    });

    socket.on('disconnect', (reason) => {
        console.log('Disconnected from server:', reason);
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
            updateLoadingStatus('<i class="fas fa-spinner fa-spin"></i> Connection lost. Reconnecting...', false);
        }
    });

    socket.on('connect_error', (error) => {
        console.log('Connection error:', error);
        reconnectAttempts++;

        if (reconnectAttempts >= maxReconnectAttempts) {
            updateLoadingStatus('<i class="fas fa-exclamation-triangle"></i> Unable to connect. Please refresh the page.', true);
            socket.disconnect();
        } else {
            updateLoadingStatus(`<i class="fas fa-sync fa-spin"></i> Attempting to reconnect... (${reconnectAttempts}/${maxReconnectAttempts})`, true);
        }
    });

    // Settings modal elements
    const modal = document.getElementById('settings-modal');
    const settingsBtn = document.getElementById('settings-button');
    const closeBtn = document.querySelector('.close');
    const thresholdForm = document.getElementById('threshold-form');

    let currentThresholds = {
        shoulder_threshold: 5.0,
        hip_threshold: 5.0,
        tilt_threshold: 2.0
    };

    // Download report functionality - only initialize on dashboard page
    if (isOnPage('download-report')) {
        document.getElementById('download-report').addEventListener('click', async function() {
            const button = this;
            const originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating report...';

            try {
                const response = await fetch('/generate_report');
                if (!response.ok) {
                    throw new Error(`Failed to generate report: ${response.statusText}`);
                }
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `posture_report_${new Date().toISOString().slice(0,19).replace(/[:-]/g, '')}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } catch (error) {
                console.error('Error downloading report:', error);
                alert('Failed to generate report. Please make sure you have active measurements and try again.');
            } finally {
                button.disabled = false;
                button.innerHTML = originalText;
            }
        });
    }

    // Settings functionality - only initialize on dashboard page
    if (isOnPage('settings-modal')) {
        // Fetch current thresholds on page load
        fetch('/get_thresholds')
            .then(response => response.json())
            .then(data => {
                currentThresholds = data;
                updateThresholdInputs();
                updateGaugeTooltips();
            })
            .catch(error => {
                console.error('Error fetching thresholds:', error);
                alert('Failed to load threshold settings. Using default values.');
            });

        // Show settings modal
        if (settingsBtn) {
            settingsBtn.onclick = function() {
                modal.style.display = "block";
                updateThresholdInputs();
            }
        }

        // Close modal
        if (closeBtn) {
            closeBtn.onclick = function() {
                modal.style.display = "none";
            }
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        // Handle threshold form submission
        if (thresholdForm) {
            thresholdForm.onsubmit = async function(e) {
                e.preventDefault();
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.innerHTML;
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

                try {
                    const formData = {
                        shoulder_threshold: parseFloat(document.getElementById('shoulder-threshold').value),
                        hip_threshold: parseFloat(document.getElementById('hip-threshold').value),
                        tilt_threshold: parseFloat(document.getElementById('tilt-threshold').value)
                    };

                    const response = await fetch('/update_thresholds', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(formData)
                    });

                    if (!response.ok) {
                        throw new Error('Failed to update thresholds');
                    }

                    const data = await response.json();
                    currentThresholds = data;
                    modal.style.display = "none";
                    updateGaugeTooltips();
                } catch (error) {
                    console.error('Error updating thresholds:', error);
                    alert('Failed to update thresholds. Please try again.');
                } finally {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }
            };
        }
    }

    function updateThresholdInputs() {
        const shoulderInput = document.getElementById('shoulder-threshold');
        const hipInput = document.getElementById('hip-threshold');
        const tiltInput = document.getElementById('tilt-threshold');

        if (shoulderInput) shoulderInput.value = currentThresholds.shoulder_threshold;
        if (hipInput) hipInput.value = currentThresholds.hip_threshold;
        if (tiltInput) tiltInput.value = currentThresholds.tilt_threshold;
    }

    function updateGaugeTooltips() {
        const containers = {
            shoulder: document.getElementById('shoulder-gauge-container'),
            hip: document.getElementById('hip-gauge-container'),
            tilt: document.getElementById('tilt-gauge-container')
        };

        if (containers.shoulder) {
            containers.shoulder.setAttribute('data-tooltip',
                `Ideal range: ±${currentThresholds.shoulder_threshold}°`);
        }
        if (containers.hip) {
            containers.hip.setAttribute('data-tooltip',
                `Ideal range: ±${currentThresholds.hip_threshold}°`);
        }
        if (containers.tilt) {
            containers.tilt.setAttribute('data-tooltip',
                `Ideal range: ±${currentThresholds.tilt_threshold}°`);
        }
    }

    function updateGauge(value, elementId, threshold) {
        const gauge = document.getElementById(elementId);
        const angleText = document.getElementById(`${elementId}-angle`);

        if (!gauge || !angleText) {
            console.error(`Missing elements for ${elementId}`);
            return;
        }

        const numericValue = parseFloat(value);
        if (isNaN(numericValue)) return;

        const percentage = Math.min(Math.abs(numericValue) / 90 * 100, 100);

        // Update progress bar with smoother animation
        gauge.style.transition = 'width 0.3s ease-out, background-color 0.3s ease-out';
        gauge.style.width = `${percentage}%`;

        // Update color based on threshold
        if (Math.abs(numericValue) <= threshold) {
            gauge.style.backgroundColor = 'var(--success-color)';
        } else if (Math.abs(numericValue) <= threshold * 2) {
            gauge.style.backgroundColor = 'var(--warning-color)';
        } else {
            gauge.style.backgroundColor = 'var(--error-color)';
        }

        // Update angle text
        angleText.textContent = `${numericValue.toFixed(1)}°`;
    }

    // Photo capture functionality
    const captureBtn = document.getElementById('capture-photo');
    const retryBtn = document.getElementById('retry-capture');
    const countdownOverlay = document.querySelector('.countdown-overlay');
    const countdownText = document.querySelector('.countdown-text');
    const capturedOverlay = document.querySelector('.captured-overlay');
    let lastMeasurements = null;
    let capturedMeasurements = null;  // New variable to store measurements at capture time

    socket.on('measurements', function(data) {
        if (!data) return;
        lastMeasurements = data;  // Store the latest measurements
        updateGauge(data.shoulder_angle, 'shoulder-gauge', currentThresholds.shoulder_threshold);
        updateGauge(data.hip_angle, 'hip-gauge', currentThresholds.hip_threshold);
        updateGauge(data.tilt_angle, 'tilt-gauge', currentThresholds.tilt_threshold);
    });

    function startCountdown() {
        let count = 5;
        countdownOverlay.style.display = 'flex';
        countdownText.textContent = count;

        const countInterval = setInterval(() => {
            count--;
            if (count > 0) {
                countdownText.textContent = count;
            } else {
                clearInterval(countInterval);
                capturePhoto();
            }
        }, 1000);
    }

    function capturePhoto() {
        countdownOverlay.style.display = 'none';
        if (lastMeasurements) {
            // Store the exact measurements at capture time
            capturedMeasurements = {
                shoulder_angle: lastMeasurements.shoulder_angle,
                hip_angle: lastMeasurements.hip_angle,
                tilt_angle: lastMeasurements.tilt_angle
            };
            
            // Update captured measurements display
            document.getElementById('captured-shoulder').textContent = 
                `${capturedMeasurements.shoulder_angle.toFixed(1)}°`;
            document.getElementById('captured-hip').textContent = 
                `${capturedMeasurements.hip_angle.toFixed(1)}°`;
            document.getElementById('captured-tilt').textContent = 
                `${capturedMeasurements.tilt_angle.toFixed(1)}°`;

            // Show captured overlay
            capturedOverlay.style.display = 'flex';
        }
    }

    if (captureBtn) {
        captureBtn.addEventListener('click', () => {
            startCountdown();
        });
    }

    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            capturedOverlay.style.display = 'none';
        });
    }

    // Save measurement functionality
    document.getElementById('save-capture').addEventListener('click', function() {
        if (!capturedMeasurements) {
            showNotification('No measurements available to save', 'error');
            return;
        }

        const measurements = {
            shoulder_angle: parseFloat(capturedMeasurements.shoulder_angle),
            hip_angle: parseFloat(capturedMeasurements.hip_angle),
            tilt_angle: parseFloat(capturedMeasurements.tilt_angle)
        };

        fetch('/capture_measurement', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(measurements)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showNotification('Measurement saved successfully!', 'success');
                capturedOverlay.style.display = 'none';
                
                // If we're on the history page, refresh to show new measurement
                if (window.location.pathname === '/history') {
                    window.location.reload();
                }
            } else {
                throw new Error(data.error || 'Failed to save measurement');
            }
        })
        .catch(error => {
            console.error('Error saving measurement:', error);
            showNotification('Failed to save measurement: ' + error.message, 'error');
        });
    });

    // Retry functionality
    document.getElementById('retry-capture').addEventListener('click', function() {
        capturedOverlay.style.display = 'none';
    });

    // Notification system
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Add animation class
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Initialize tooltips
    updateGaugeTooltips();
});
