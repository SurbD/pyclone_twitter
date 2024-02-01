const form = document.forms["edit-profile-form"];
const userName = form["name"];
const aboutMe = form["aboutMe"];
const location = form["location"];
const nameRegExp = /^([a-zA-Z])([a-zA-Z])/;

let saveBtnActive = false; // will be used to make the btn gray if no new change is made
let nameValid = true;

form.addEventListener("submit", (event) => {
    event.preventDefault();

    if (nameValid) {
        console.log('Form is ready for submission.')
        sendData()
            .then((data) => {
                const responds = data.status;
                console.log('Data')
            })
            .catch((err) => console.log(err))
    } else {
        console.log('Invalid form inputs, please check ')
    }
})

userName.addEventListener("input", () => {
    const isValid = userName.value.length == 0 || 
    (nameRegExp.test(userName.value) && userName.value.length >= 5);
    
    if (isValid) {
        nameValid = true;
        userName.classList.remove("invalid-form-field");
    } else {
        nameValid = false;
        userName.classList.add("invalid-form-field");
    }
})

function sendData() {
    const formData = {
        name: userName.value,
        aboutMe: aboutMe.value,
        location: location.value, 
    }
    const promise = axios.post("/edit-profile", formData);
    const resPromise = promise.then((response) => response.data);

    return resPromise;
}