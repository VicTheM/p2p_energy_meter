
let stateText;
const switchFrame = document.querySelector('.frame');

function validateInput(input) {
    const amount = parseFloat(input.value);
    if (isNaN(amount) || amount <= 0) {
        alert('Invalid input: Please enter a positive number.');
        return false;
    }
    return true;
}

async function handleAction(state) {
    try {
        const response = await fetch(`/actions?state=${state}`, {
            method: 'POST'
        });
        const data = await response.json();
        // updatePage(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function handleCredit(event) {
    event.preventDefault();
    const amount = document.getElementById('amount').value;
    if (!validateInput(document.getElementById('amount'))) {
        return;
    }
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
        feedback.textContent = 'Credit successful!';
        feedback.style.display = 'inline';
        
        // Clear the input field
        document.getElementById('amount').value = '';

        // Hide the feedback after 3 seconds
        setTimeout(() => {
            feedback.style.display = 'none';
        }, 3000);
    } catch (error) {
        console.error('Error:', error);
    }
}

function handleToggle(newState, shouldPost) {
    if (newState === 3) {
        document.getElementById('offline-text').style.display = 'block';
        document.getElementById('share').checked = false;
        document.getElementById('receive').checked = false;
        document.getElementById('disconnect').checked = false;
    } else {
        const allToggles = switchFrame.querySelectorAll('input[type="checkbox"]'); 
        document.getElementById('offline-text').style.display = 'none';
        allToggles[0].checked = (newState === 0);
        allToggles[1].checked = (newState === 1);
        allToggles[2].checked = (newState === 2);
        
        stateText.textContent = newState;
        // allToggles.forEach((toggle) => {
        //     toggle.disabled = true;
        //     setTimeout(() => {
        //         toggle.disabled = false;
        //     }, 3000)
        // })
    }
    
    if(shouldPost) handleAction(newState);
}

function handleCheck(element, newState=undefined) {
    if ((element && element.checked) || newState !== undefined) {
        const switcher = (element && element.id) || newState
        // console.log(switcher)
        switch(switcher) {
        case 1:
        case "share":
            handleToggle(1, switcher==='share');
            break;
        case 2:
        case "receive":
            handleToggle(2, switcher==='receive');
            break;
        case 0:
        case "disconnect":
            handleToggle(0, switcher==='disconnect');
            break;
        default:
            handleToggle(3, switcher===3);
    }}
}

function updatePage(data) {
    console.log("In update page function")
    console.log(data);
    if ('error' in data) {
        alert(data.error);
        return;
    }
    if ('credit' in data) {
        document.getElementById('balance').textContent = data.credit;
    }
    if ('account_balance' in data) {
        document.getElementById('balance').textContent = data.account_balance;
    }
    if ('voltage' in data) {
        // console.log(data.voltage);
        document.getElementById('voltage').textContent = `${data.voltage.toFixed(2)}V`;
    }
    if ('current' in data) {
        document.getElementById('current').textContent = `${data.current.toFixed(2)}mA`;
    }
    if ('duration' in data) {
        document.getElementById('duration').textContent = `${data.duration}s`;
    }
    if ('current' in data && 'voltage' in data) {
        document.getElementById('power').textContent = `${(data.current * data.voltage / 1000).toFixed(2)}W`;
    }
    if ('totalPowerSent' in data) {
        document.getElementById('totalPowerSent').textContent = `${data.totalPowerSent.toFixed(2)}W`;
    }
    if ('totalPowerReceived' in data) {
        // console.log(data.totalPowerReceived);
        document.getElementById('totalPowerReceived').textContent = `${data.totalPowerReceived.toFixed(2)}W`;
    }
    if ('state' in data) {
        console.log(data.state, Number(stateText.textContent))
        // if (data.state !== Number(stateText.textContent)) {
        stateText.textContent = data.state;
        handleCheck(undefined, data.state);
    // }
    // if ('newstate' in data) {
    //     console.log(data.newstate);
    //     document.getElementById('state').textContent = data.newstate;
    // }
}}

async function fetchUpdates() {
    try {
        const response = await fetch('/updatepage');
        const data = await response.json();
        console.log(data);
        // if ('state' in data) {
            // if (state === 3) {
            //     document.getElementById('offline-text').style.display = 'block';
            //     document.getElementById('share').checked = false;
            //     document.getElementById('receive').checked = false;
            //     document.getElementById('disconnect').checked = false;
            // } else {
            //     document.getElementById('offline-text').style.display = 'none';
            //     document.getElementById('share').checked = (state === 1);
            //     document.getElementById('receive').checked = (state === 2);
            //     document.getElementById('disconnect').checked = (state === 0);
            // }
        // }
        updatePage(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

 // Set initial state from server-rendered variable
document.addEventListener("DOMContentLoaded", function() {
    stateText = document.getElementById('state');
    const state = Number(stateText.textContent);
    
    
// Schedule the fetchUpdates function to run every 30 seconds
    setInterval(fetchUpdates, 4000);
    // console.log(state);
    handleCheck(undefined, state);
});

switchFrame.addEventListener("click", function(event) {
    const elem = event.target;
    if (elem.closest('input[type="checkbox"]')) {
    // console.log(elem);
    handleCheck(elem);        
    }
});