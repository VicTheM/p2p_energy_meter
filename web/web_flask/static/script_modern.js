// Modern Energy Dashboard JavaScript

let stateText;

let accumulatedCredit = 0.0;
let creditPerWatt = 20.00; // Example rate: NGN 15.00 per watt-hour

const currFormatter = new Intl.NumberFormat('en-NG', { 
    style: 'currency', 
    currency: 'NGN', 
    currencyDisplay: 'narrowSymbol' 
});

function validateInput(input) {
    const amount = parseFloat(input.value);
    if (isNaN(amount) || amount <= 0) {
        showNotification('Invalid input: Please enter a positive number.', 'error');
        return false;
    }
    return true;
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 20px',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '9999',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease',
        maxWidth: '300px',
        wordWrap: 'break-word'
    });
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.backgroundColor = 'var(--primary)';
            break;
        case 'error':
            notification.style.backgroundColor = 'var(--destructive)';
            break;
        default:
            notification.style.backgroundColor = 'var(--secondary)';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 300);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

async function handleAction(state) {
    try {
        const response = await fetch(`/actions?state=${state}`, {
            method: 'POST'
        });
        const data = await response.json();
        updatePage(data);
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to update device state', 'error');
    }
}

async function handleCredit(event) {
    event.preventDefault();
    const amountInput = document.getElementById('amount');
    const amount = amountInput.value;
    
    if (!validateInput(amountInput)) {
        return;
    }
    
    // Show loading state
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalContent = submitButton.innerHTML;
    submitButton.innerHTML = '<i data-lucide="loader-2" class="btn-icon" style="animation: spin 1s linear infinite;"></i>Processing...';
    submitButton.disabled = true;
    lucide.createIcons();
    
    try {
        const response = await fetch(`/actions?credit=${amount}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        updatePage(data);

        // Show success feedback
        const feedback = document.getElementById('credit-feedback');
        if (feedback) {
            feedback.textContent = `Successfully added ${currFormatter.format(parseFloat(amount))}!`;
            feedback.classList.remove('hidden');
            
            // Hide the feedback after 3 seconds
            setTimeout(() => {
                feedback.classList.add('hidden');
            }, 3000);
        }
        
        showNotification(`Successfully added ${currFormatter.format(parseFloat(amount))}`, 'success');
        
        // Clear the input field
        amountInput.value = '';
        
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to add credit', 'error');
    } finally {
        // Restore button state
        submitButton.innerHTML = originalContent;
        submitButton.disabled = false;
        lucide.createIcons();
    }
}

function updateOnlineStatus(isOnline) {
    const badge = document.querySelector('.badge');
    const offlineNotice = document.getElementById('offline-text');
    
    if (badge) {
        if (isOnline) {
            badge.className = 'badge badge-online body-medium';
            badge.textContent = 'Online';
        } else {
            badge.className = 'badge badge-offline body-medium';
            badge.textContent = 'Offline';
        }
    }
    
    if (offlineNotice) {
        if (isOnline) {
            offlineNotice.classList.add('hidden');
        } else {
            offlineNotice.classList.remove('hidden');
        }
    }
}

function handleToggle(newState, shouldPost) {
    const isOnline = newState !== 3;
    updateOnlineStatus(isOnline);
    
    if (newState === 3) {
        // Device offline
        document.getElementById('share').checked = false;
        document.getElementById('receive').checked = false;
        document.getElementById('disconnect').checked = false;
        
        // Disable all switches
        document.querySelectorAll('.switch input').forEach(input => {
            input.disabled = true;
        });
    } else {
        // Device online
        document.getElementById('disconnect').checked = (newState === 0);
        document.getElementById('share').checked = (newState === 1);
        document.getElementById('receive').checked = (newState === 2);

        if (newState === 0 && accumulatedCredit > 0) {
            const balanceElement = document.querySelector('.balance-amount');
            if (balanceElement) {
                let currentBalance = parseFloat(balanceElement.textContent.replace(/[^0-9.-]+/g,"")) || 0;
                let newBalance = currentBalance + accumulatedCredit;
                balanceElement.textContent = currFormatter.format(newBalance);
            }
            // Post the accumulated amount to the server
            handleActionWithCredit(accumulatedCredit);
            accumulatedCredit = 0.0; // Reset after sending
            updateAccumulatedCreditDisplay();
        }

        // Enable switches based on device ID
        document.querySelectorAll('.switch input').forEach(input => {
            input.disabled = false;
        });
        
        // Re-apply device-specific restrictions
        const deviceId = document.querySelector('.header-subtitle').textContent.replace('Device ', '');
        if (deviceId === "002") {
            document.getElementById('share').disabled = true;
        }
        if (deviceId === "001") {
            document.getElementById('receive').disabled = true;
        }
        
        if (stateText) {
            stateText.textContent = getStateText(newState);
        }
    }
    
    if (shouldPost) {
        handleAction(newState);
    }
}


function getStateText(state) {
    switch(state) {
        case 0: return 'Disconnected';
        case 1: return 'Sharing';
        case 2: return 'Receiving';
        case 3: return 'Offline';
        default: return 'Active';
    }
}

function handleCheck(element, newState = undefined) {
    if ((element && element.checked) || newState !== undefined) {
        const switcher = (element && element.id) || newState;
        
        switch(switcher) {
            case 1:
            case "share":
                handleToggle(1, switcher === 'share');
                break;
            case 2:
            case "receive":
                handleToggle(2, switcher === 'receive');
                break;
            case 0:
            case "disconnect":
                handleToggle(0, switcher === 'disconnect');
                break;
            default:
                handleToggle(3, switcher === 3);
        }
    }
}

function updatePage(data) {
    console.log("Updating page with data:", data);
    
    if ('error' in data) {
        showNotification(data.error, 'error');
        return;
    }
    
    if ('credit' in data) {
        const balanceElement = document.querySelector('.balance-amount');
        if (balanceElement) {
            balanceElement.textContent = currFormatter.format(data.credit);
        }
    }
    
    if ('account_balance' in data) {
        const balanceElement = document.querySelector('.balance-amount');
        if (balanceElement) {
            balanceElement.textContent = currFormatter.format(data.account_balance);
        }
    }
    
    if ('voltage' in data) {
        const voltageElement = document.getElementById('voltage');
        if (voltageElement) {
            voltageElement.textContent = data.voltage.toFixed(2);
        }
    }
    
    if ('current' in data) {
        const currentElement = document.getElementById('current');
        if (currentElement) {
            currentElement.textContent = data.current.toFixed(2);
        }
    }
    
    if ('duration' in data) {
        const durationElement = document.getElementById('duration');
        if (durationElement) {
            durationElement.textContent = data.duration;
        }
    }
    
    if ('current' in data && 'voltage' in data) {
        const powerElement = document.getElementById('power');
        if (powerElement) {
            powerElement.textContent = (data.current * data.voltage / 1000).toFixed(2);
        }
    }
    
    if ('totalPowerSent' in data) {
        const sentElement = document.getElementById('totalPowerSent');
        if (sentElement) {
            sentElement.textContent = data.totalPowerSent.toFixed(2);
        }
    }
    
    if ('totalPowerReceived' in data) {
        const receivedElement = document.getElementById('totalPowerReceived');
        if (receivedElement) {
            receivedElement.textContent = data.totalPowerReceived.toFixed(2);
        }
    }
    
    if ('state' in data) {
        console.log('New state:', data.state, 'Current state:', stateText ? stateText.textContent : 'N/A');
        if (stateText) {
            const newStateText = getStateText(data.state);
            stateText.textContent = newStateText;
        }
        handleCheck(undefined, data.state);
    }
}

async function fetchUpdates() {
    try {
        const response = await fetch('/updatepage');
        const data = await response.json();
        console.log('Fetched updates:', data);

        if (data.state === 1 && data.totalPowerSent) {
            // Calculate new credit based on the change in total power sent
            // This requires storing the previous value.
            const prevPowerSent = parseFloat(document.getElementById('totalPowerSent').textContent) || 0;
            const newPowerSent = data.totalPowerSent;
            const powerDifference = newPowerSent - prevPowerSent;
            
            // Assuming power is in Watts and credit is per Watt-hour, we need to convert.
            // Power (W) * Time (s) / 3600 (s/h) * Rate (NGN/Wh)
            const timeInterval = 5; // fetchUpdates runs every 5 seconds
            const creditToAdd = (powerDifference * timeInterval / 3600) * creditPerWatt;
            
            accumulatedCredit += creditToAdd;
            updateAccumulatedCreditDisplay();
        }
        
        updatePage(data);
    } catch (error) {
        console.error('Error fetching updates:', error);
        // Don't show notification for fetch errors to avoid spam
    }
}

// Initialize the application
document.addEventListener("DOMContentLoaded", function() {
    // Initialize Lucide icons
    lucide.createIcons();
    
    // Get state element
    stateText = document.getElementById('state');
    
    if (stateText) {
        const state = parseInt(stateText.textContent) || 0;
        console.log('Initial state:', state);
        handleCheck(undefined, state);
    }
    
    // Set up periodic updates
    setInterval(fetchUpdates, 1000);
    
    // Add event listeners for switches
    document.querySelectorAll('.switch input[type="checkbox"]').forEach(switchInput => {
        switchInput.addEventListener('change', function(event) {
            handleCheck(event.target);
        });
    });
    
    // Add smooth transitions to cards
    document.querySelectorAll('.card').forEach(card => {
        card.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';
        
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px 0 rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
        });
    });
    
    // Add loading animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .notification {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
    `;
    document.head.appendChild(style);
});

// Export functions for potential external use
window.EnergyDashboard = {
    handleCredit,
    handleAction,
    updatePage,
    showNotification
};


// Function to update the accumulated credit display.
function updateAccumulatedCreditDisplay() {
    const accCreditElement = document.getElementById('accumulatedCredit');
    if (accCreditElement) {
        accCreditElement.textContent = currFormatter.format(accumulatedCredit);
    }
}

// A new function to post accumulated credit.
async function handleActionWithCredit(amount) {
    try {
        // Round to 2 decimal places
        const roundedAmount = parseFloat(amount.toFixed(2));

        const response = await fetch(`/actions?credit=${roundedAmount}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        updatePage(data);
        showNotification(
            `Successfully added ${currFormatter.format(roundedAmount)} accumulated credit to your balance.`,
            'success'
        );
    } catch (error) {
        console.error('Error:', error);
        // showNotification('Failed to add accumulated credit', 'error');
    }
}

