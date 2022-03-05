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
document.getElementById("create_account_fire").addEventListener('submit', submit_create);

document.getElementById("sign_in_fire").addEventListener('submit', submit_sign_in);

function submit_create(e) {
	e.preventDefault();

	console.log(123);
}

function submit_sign_in(e) {
	e.preventDefault();

	console.log(456);
}