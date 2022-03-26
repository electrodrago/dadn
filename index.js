import app from "../firebase.js"
import { getAuth, onAuthStateChanged, signOut } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-auth.js';

const auth = getAuth()
onAuthStateChanged(auth, (user) => {
    if(user){
        alert("welcome user: " + user.uid);
        document.getElementById("Log").innerHTML  = `<p>Logout</p>`
    }
    else{
        document.getElementById("Log").innerHTML  = `<p>Login</p>`
       // window.location = '../login.html'
    }

}
)

const Log = document.querySelector('#Log')
Log.addEventListener('click', (e) => {
    e.preventDefault();
    const user = auth.currentUser;
    console.log("nam")
    if(user){
        let uid = user.uid;
        // console.log(uid)
        signOut(auth).then(() => {
        alert("user : " + uid + "have just logout");
        // window.location = './index.html'
     })
    }
    else{
        window.location = './login/login.html'
    }

})


