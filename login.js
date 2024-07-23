// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCZTJ07ur6pTnhbbkC9bmLGAWHQWvpSTRM",
    authDomain: "python-3146b.firebaseapp.com",
    projectId: "python-3146b",
    storageBucket: "python-3146b.appspot.com",
    messagingSenderId: "772268136643",
    appId: "1:772268136643:web:baf4c28dbeeaa9f19aaa76"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const auth = getAuth();


const submit = document.getElementById('submit');

submit.addEventListener("click", function (event) {
    event.preventDefault()
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed up 
            const user = userCredential.user;
            if (email === "admin@gmail.com" && password === "admin123") {
                // Redirect admin to admin page
                window.location.href = "admin.html";
            } else {
                // Redirect regular user to index page
                window.location.href = "index.html";
            }
            
            // ...
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(errorMessage)
            // ..
        });

})
