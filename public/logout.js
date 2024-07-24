"use strict";

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";

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
    document.getElementById("logout-btn").addEventListener(("click"), function() {
        signOut(auth)
        .then((output) => {
            document.cookie = "token=;path=/;SameSite=Strict";
            window.location = "/";
        })
    });
});