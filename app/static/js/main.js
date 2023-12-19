const notification = document.getElementById("notification");
const closeBtn = document.getElementById("close");
setBg()


// const pfp = document.getElementById("pfp")
// pfp.style.backgroundImage = pfp.dataset.content;

function setBg() {
    const pfp = document.getElementById("pfp");
    const userIcon = document.getElementById('user-icon')
    
    if (pfp){
        pfp.style.backgroundImage = pfp.dataset.content;
    }

    if (userIcon) {
        userIcon.style.backgroundImage = userIcon.dataset.content;
        console.log(userIcon.dataset.content)
    }
    console.log('Loaded')
}

// JavaScript for Flash Alert Canceling
function dataDismiss() {
    var x = document.getElementById("alert_id");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function agreeChecked() {
    // Check onclick if Terms and Condition tab is Checked 
    // ...and styles the button accordingly
    var checked = document.getElementById('terms-n-condition').checked;

    if (checked == true) {
        document.getElementById("nextBtn").classList.remove("inactive-btn");
        // document.getElementById("nextBtn").style.background = "#0095ff";
        // document.getElementById("nextBtn").style.color = "aliceblue";
    } else {
        document.getElementById("nextBtn").classList.add("inactive-btn");
        // document.getElementById("nextBtn").style.background = "#b0b0b071";
        // document.getElementById("nextBtn").style.color = "#000000d7";
    }
    
}


function closeFlash() {
    notification.classList.remove('notification-show');
}

function flashPopup(message) {
    console.log(message)
    const reg_form = document.forms['registration-form']
    const username = reg_form['username'].value
    const email = reg_form['email'].value
    const date_of_birth = reg_form['date_of_birth'].value

    if (username && email && date_of_birth != "") {
        document.getElementById('notification-mssg').innerText = message
        notification.classList.add('notification-show');
    }
}
