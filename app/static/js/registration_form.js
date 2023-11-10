var currentTab = 0;

showTab(currentTab);

function showTab(n) {

    var x = document.getElementsByClassName('tab');
    x[n].style.display = "block";

    if (n == 0) {
        document.getElementById("close").style.display = 'inline';
        document.getElementById("prevBtn").style.display = "none";
    } else if (n == (x.length - 1)) {
        document.getElementById("close").style.display = 'none';
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("close").style.display = 'none';
        document.getElementById("prevBtn").style.display = "inline";
    }

    // Button color for Tab 3
    if (n == 2) {
        document.getElementById("nextBtn").classList.add("blued-btn");
        
    } else {document.getElementById("nextBtn").classList.remove("blued-btn");}
    // End of Button color for Tab 3

    if (n == (x.length - 1)) {
        document.getElementById("submitBtn").value = "Next";
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("submitBtn").style.display = "inline";
    } else if (n == 2) {
        document.getElementById("nextBtn").value = "Sign up";
        // document.getElementById("nextBtn").innerHTML = "Sign up";
    } else {
        // document.getElementById("nextBtn").innerHTML = "Next";
        document.getElementById("nextBtn").value = "Next"
    }

    if (n == 2) {
        const reg_form = document.forms['registration-form']
        document.getElementById("form-username").innerText = reg_form['username'].value
        document.getElementById("form-email").innerText = reg_form['email'].value.toLowerCase();
        document.getElementById("form-date_of_birth").innerText = reg_form['date_of_birth'].value
    }

    if (n == 3) {
        const reg_form = document.forms['registration-form']
        document.getElementById("user-email-data").innerText = reg_form['email'].value.toLowerCase()
    }

    if (n == 1) {
        agreeChecked()
    } else {
        document.getElementById("nextBtn").classList.remove("inactive-btn");
    }

    fixStepindicator(n);
}

function nextPrev(n) {
    var x = document.getElementsByClassName("tab");

    if (n == 1 && !validateForm()) return false;

    x[currentTab].style.display = 'none';
    currentTab = currentTab + n;

    if (currentTab >= x.length) {
        document.getElementById("regForm").submit();
        return false;
    }
    closeFlash()
    showTab(currentTab);
}

function validateForm() {
    var x = document.getElementsByClassName('tab');
    var valid = false

    // valid = checkIfUserExists()
    if (currentTab == 0) {
        // valid = True
        console.log('Current Tab is '+ currentTab)
        email_valid = !checkIfUserExists()
        // username_valid = !checkIfUserTaken()
        form_valid = checkFormValidity()

        if (email_valid == true && form_valid == true) {
            valid = true
        } else {
            // valid =  false
            message = "Invalid form inputs! Please check username or email and try again."
            flashPopup(message)
        }
    } else if (currentTab == 1) {
        checked = document.getElementById('terms-n-condition').checked;
        if (checked == true) {
            valid = true
        } else {
            valid = false
        }
    } else if (currentTab == 2) {
        success = sendVerificationCode()

        if (success == true) {
            valid = true
        }
    } else if (currentTab == 3) {
        verified = confirmVerificationCode()

        if (verified == true) {
            valid = true
        } 
    } else {
        valid = true
    }

    return valid;
}

function fixStepindicator(n) {
    var x = document.getElementsByClassName("tab");
    document.getElementById("step").innerHTML = 'Step ' + (currentTab+1) + ' of ' + x.length
}


// Trial for email send so it validates immediately