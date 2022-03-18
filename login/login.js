
import { getFirestore  } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js'

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