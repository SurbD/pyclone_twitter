
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
