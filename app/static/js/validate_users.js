function axiosTest() {
    const registrationForm = document.forms['registration-form']
    const email = registrationForm['email'].value
    const data = {
        email: email
    }

    const promise = axios.post('/validate-email', data)
    const dataPromise = promise.then((response) => response.data)
    
    return dataPromise
}


function checkIfUserExists() {
    // response = {}
    axiosTest()
        .then(data=> {
            console.log(' DATA EXISTS ')
            console.log(data.user_exists)
            // response.json({ message: 'Request received!', data })
            valid = data.user_exists
            displayErr(valid)
        })
        .catch(err => console.log(err))
    return valid
}

// Username Taken Test Function
// Modify the display err function to take parameters to help it
//  figure which function its getting called from so it can work for 
//  both usernameTest and email validation to work with message sent from
// the Backend or anyone works

function usernameTest() {
    const registrationForm = document.forms['registration-form']
    const username = registrationForm['username'].value
    const data = {
        username: username
    }

    const promise = axios.post('/validate-username', data)
    const dataPromise = promise.then((response) => response.data)
    
    return dataPromise
}


function checkIfUserTaken() {
    usernameTest()
        .then(data=> {
            taken = data.taken
            document.getElementById("username-error").innerText = data.message
        })
        .catch(err => console.log(err))
    return taken
}


// End 

function formTest() {
    const reg_form = document.forms['registration-form']
    const data = {
        username: reg_form['username'].value,
        email: reg_form['email'].value,
        date_of_birth: reg_form['date_of_birth'].value
    }

    const promise = axios.post('/validate-inputs', data)
    const dataPromise = promise.then((response) => response.data)
    
    return dataPromise
}


function checkFormValidity() {
    formTest()
        .then(response => {
            console.log('Response')
            console.log(response)
            
            isValid = response.isValid
        })
        .catch(err => console.log(err))

    return isValid
}

function usernameValidate() {
    checkIfUserTaken()
    checkFormValidity()
}

function emailValidate() {
    checkIfUserExists()
    checkFormValidity()
}


function sendVerification() {
    const username = document.getElementById("form-username").innerText;
    const email = document.getElementById("form-email").innerText
    const data = {
        username: username,
        email: email
    }

    const promise = axios.post('/get-verification-code', data)
    const dataPromise = promise.then((response) => response.data)

    return dataPromise
}

function sendVerificationCode() {
    sendVerification()
        .then(response => {
            success = response.success
            
            console.log(response)
            console.log(response.success)
        })
        .catch(err => console.log(err))
    return success
}


function confirmVerification() {
    const registrationForm = document.forms['registration-form']
    const code = registrationForm['verification_code'].value
    console.log(code)
    const data = {
        code: code
    }
    const promise = axios.post('/confirm-verification-code', data)
    const dataPromise = promise.then((response) => response.data)

    return dataPromise
}

function confirmVerificationCode() {
    confirmVerification()
        .then(response => {
            verified = response.verified
            
            console.log(response)
            console.log(response.verified)
        })
        .catch(err => console.log(err))
    return verified
}


function displayErr(valid) {
    if (valid == true) {
        document.getElementById("email-error").innerText = "Sorry, this email already exists please Login!";
    } else {
        document.getElementById("email-error").innerText = "";
    }
}

