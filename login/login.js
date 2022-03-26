import app from "../firebase.js"
// import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, set, ref, update } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-auth.js';
// import { getAuth, createUserWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-auth.js'
// import { getFirestore  } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js'
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// const firebaseConfig = {
//   apiKey: "AIzaSyDy0vFrfvuXoi4xEa9zi7qlkNFy3haRtOI",
//   authDomain: "dadn-6c126.firebaseapp.com",
//   projectId: "dadn-6c126",
//   storageBucket: "dadn-6c126.appspot.com",
//   messagingSenderId: "768299472042",
//   appId: "1:768299472042:web:2bbf97516e7c06e092ecd3"
// };

// Initialize Firebase
// const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth()
SignUp.addEventListener('click', (e) => {
	var email = document.getElementById('submit_email_create').value;
	var password = document.getElementById('submit_pass_create').value;
	var username = document.getElementById('submit_username_create').value;
	createUserWithEmailAndPassword(auth, email, password)
		.then(async (userCredential) => {
			// Signed in 
			const user = userCredential.user;
			// console.log("nam");
			const dt = new Date();
			await set(ref(database, 'users/' + user.uid), {
				username: username,
				email: email,
				status: true,
				last_login: dt
			})

			alert('user created!');
			window.location = '../index.html'
			// ...
		})
		.catch((error) => {
			const errorCode = error.code;
			const errorMessage = error.message;

			alert(errorMessage)
			// ..
		});
});
const signin = document.querySelector('#SignIn')
signin.addEventListener('click', (e) => {
	var email = document.getElementById('submit_email_signin').value;
	var password = document.getElementById('submit_pass_signin').value;
	console.log("nam")

	signInWithEmailAndPassword(auth, email, password)
		.then((userCredential) => {
			// Signed in 
			const user = userCredential.user;

			const dt = new Date();
			update(ref(database, 'users/' + user.uid), {
				last_login: dt,
				status: true
			})

			alert('User loged in!');
			//window.location = '../homepage2/index2.html';
			window.location = '../index.html'
			// ...
		})
		.catch((error) => {
			const errorCode = error.code;
			const errorMessage = error.message;

			alert(errorMessage);
		});
})
// console.log(auth.currentUser)
// onAuthStateChanged(auth, (user) => {
// 	if (user) {
// 		// console.log("nam in here")

// 		window.location = '../homepage2/index2.html';
// 	}
// 	else {
// 		// console.log("nam not in here")
// 	}
// })
// const delete_user = auth.currentUser;




// onAuthStateChanged(auth, (user) => {
//   if(user){
// 	  console.log("nam in here");
// 	  window.location = '../homepage2/index2.html';
//   }
//   else{
//   }
// })


// Make auth, firestore
// const auth = getAuth();
// const db = getFirestore();
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

// Listen for create account form submit
// const create_form = document.querySelector("#create_account_fire");
// create_form.addEventListener('submit', submit_create);

// document.getElementById("sign_in_fire").addEventListener('submit', submit_sign_in);

// function submit_create(e) {
// 	e.preventDefault();

// 	const email = create_form['submit_email_create'].value;
// 	const password = create_form['submit_pass_create'].value;
// 	const re_pass = create_form['submit_pass_re'].value;
	
// 	console.log(123);

// 	const auth = getAuth();
// 	createUserWithEmailAndPassword(auth, email, password).then(cred => {
// 		console.log(cred)
// 	});
// }

// function submit_sign_in(e) {
// 	e.preventDefault();

// 	console.log(456);
// }