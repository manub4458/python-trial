"use strict";

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyBKEZiWN-bNvSi17uaT4WkSetCEeg_tBe0",
    authDomain: "assignment-c2aa3.firebaseapp.com",
    projectId: "assignment-c2aa3",
    storageBucket: "assignment-c2aa3.appspot.com",
    messagingSenderId: "345611445983",
    appId: "1:345611445983:web:c917280d6e06796a6aeb6a"
};


window.addEventListener("load", function(){
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    document.getElementById("signup-btn").addEventListener("click", function(){

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {

            const user = userCredential.user;
            console.log("User has been created");

            user.getIdToken().then((token) => {
                    document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                    window.location = "/";
            });
        })
        .catch((error) => {
            console.log(error.code, error.message);
        });
    });
});
