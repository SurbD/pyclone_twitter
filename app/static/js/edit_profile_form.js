// Edit profile form logic and data transfer

let saveBtnActive = false; // will be used to make the btn gray if no new change is made
let nameValid = true;

const form = document.forms["edit-profile-form"];
const userName = form["name"];
const aboutMe = form["aboutMe"];
const userLocation = form["location"];
const nameRegExp = /^([a-zA-Z])([a-zA-Z])/;

form.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log("Submitting edit form ");

  if (nameValid) {
    console.log("Form is ready for submission.");
    sendData()
      .then((data) => {
        const response = data.status;
        console.log(`Form submitted. Result = ${response}`);
      })
      .catch((err) => console.log(err));
  } else {
    console.log("Invalid form inputs, please check ");
  }
});

userName.addEventListener("input", () => {
  const isValid =
    userName.value.length == 0 ||
    (nameRegExp.test(userName.value) && userName.value.length >= 5);

  if (isValid) {
    nameValid = true;
    console.log("Valid");
    userName.classList.remove("invalid-form-field");
  } else {
    nameValid = false;
    console.log("InValid");
    userName.classList.add("invalid-form-field");
  }
});

function sendData() {
  console.log("Entering sendData() in edit_profile js");
  const formData = {
    name: userName.value,
    aboutMe: aboutMe.value,
    location: userLocation.value,
  };
  const promise = axios.post("/edit-profile", formData);
  const resPromise = promise.then((response) => response.data);

  return resPromise;
}
