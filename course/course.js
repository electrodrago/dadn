import app from "../firebase.js";
import {
  getFirestore,
  collection,
  onSnapshot,
  addDoc,
  deleteDoc,
  doc,
  query,
  where,
  orderBy,
  serverTimestamp,
  updateDoc,
  setDoc,
  getDocs,
} from "https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js";
import { getAuth, signOut } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-auth.js';

// SignOut Button 
const auth = getAuth()
const  logout = document.querySelector('#Logout')
logout.addEventListener('click', (e) => {
  e.preventDefault();
  const user = auth.currentUser;
  let uid = user.uid;
  // console.log(uid)
  signOut(auth).then(() => {
    alert("user : " + uid + "have just logout");
    window.location = '../index.html'
  })
})

const db = getFirestore();
const colRef = collection(db, "Sample_Teacher");

onSnapshot(colRef, async (snapshot) => {
  let teachers = [];
  snapshot.docs.forEach((doc) => {
    teachers.push(doc.id);
  });
  console.log("teachers:" + teachers);
  let courses = [];
  //   var did;
  for (let i = 0; i < teachers.length; i++) {
    await getDocs(collection(db, "Sample_Teacher", teachers[i], "COURSE")).then(
      (snapshot) => {
        //console.log(snapshot.docs);
        snapshot.docs.forEach(async (doc) => {
          courses.push({ T_id: teachers[i], C_name: doc.id });
          //console.log(courses);
        });
      }
    );
  }
  console.log("List khoa hoc:", courses);

  let Classes = [];
  for (let i = 0; i < courses.length; i++) {
    await getDocs(
      collection(
        db,
        "Sample_Teacher",
        courses[i].T_id,
        "COURSE",
        courses[i].C_name,
        "CLASS"
        
      )
    ).then((snapshot) => {
      snapshot.docs.forEach((doc) => {
        // did = doc.id;
        Classes.push({
          T_id: courses[i].T_id,
          C_name: courses[i].C_name,
          Class_name: doc.id,
          // Semester: doc.data().Class_Semester,
          // Last_Access: doc.data().last_access.toString(),
          // Create_Date: doc.data().create,
        });
          //console.log(doc.data().last_access)
      });
    });

    //   getDocs(collection(db, 'TEACHER', courses[i].T_id, 'COURSE', courses[i].T_id))
  }

let Semesters = []

for( let i = 0 ; i < Classes.length; i++){
  await getDocs(
    collection(
      db, 
      "Sample_Teacher",
      Classes[i].T_id,
      "COURSE",
      Classes[i].C_name,
      "CLASS",
      Classes[i].Class_name,
      "SEMESTER"
    )
  ).then((snapshot) => {
    snapshot.docs.forEach((doc) =>{
      Semesters.push({
        T_id:Classes[i].T_id,
        C_name: Classes[i].C_name,
        Class_name: Classes[i].Class_name,
        Semester: doc.id,
        Last_Access: doc.data().lass_access.toDate(),
        Create_Date: doc.data().create.toDate(),
      })
      // console.log(doc.data().create)
    } )
    console.log("semes: " + Classes)
  })
}

  Semesters.sort(function (a, b) {
    return b.Last_Access - a.Last_Access;
  });
  // console.log("Classes: ", String(Classes[0].Create_Date).split("(")[0]);

  for (let i = 0; i < Classes.length; i++) {
    document.getElementById("--T-body").innerHTML += `
      <tr>
        <td>${Semesters[i].T_id}</td>
        <td>${
          Semesters[i].C_name +
          " - " +
          Semesters[i].Class_name +
          " - " +
          Semesters[i].Semester
        }</td>
        <td>${String(Semesters[0].Create_Date).split("(")[0]}</td>
        <td>${String(Semesters[0].Last_Access).split("(")[0]}</td>
      </tr>
    `;
  }
  init();
});

function init() {
  addRowHandlers("table");
}
function addRowHandlers(tableId) {
  if (document.getElementById(tableId) != null) {
    var table = document.getElementById(tableId);
    var rows = table.getElementsByTagName("tr");
    var T_id = "";
    var C_name = "";
    var Class_name = "";
    var Semester = "";
    var Create_Date = "";
    var Last_Access = "";
    for (let i = 1; i < rows.length; i++) {
      rows[i].i = i;
      console.log(table.rows[i].cells[1].innerHTML)
      rows[i].onclick = function () {
        T_id = table.rows[this.i].cells[0].innerHTML;
        var temp = table.rows[this.i].cells[1].innerHTML;
        //console.log(temp);
        C_name = temp.substr(0, temp.indexOf(" - "));
        Class_name = temp.slice(
          C_name.length + 3,
          temp.indexOf(" - ", C_name.length + 3)
        );
        //console.log(Class_name)
        Semester = temp.substr(
          C_name.length + 3 + Class_name.length + 3,
          temp.length
        );
        Create_Date = table.rows[this.i].cells[2].innerHTML;
        Last_Access = table.rows[this.i].cells[3].innerHTML;

        // Update to localStorage to parse to dashboard.js
        localStorage.setItem("T_id", T_id);
        localStorage.setItem("C_name", C_name);
        localStorage.setItem("Class_name", Class_name);
        localStorage.setItem("Semester", Semester);
        localStorage.setItem("Create_Date", Create_Date);

        // alert(
        //   "T_id: " +
        //     T_id +
        //     " C_name: " +
        //     C_name +
        //     " Class_name: " +
        //     Class_name +
        //     " Semester: " +
        //     Semester +
        //     " Create_Date: " +
        //     Create_Date +
        //     " last_access: " +
        //     Last_Access
        // );

        // Update last access

        // db.collection("TEACHER")
        //   .doc(T_id)
        //   .collection("COURSE")
        //   .doc(C_name)
        //   .collection("CLASS")
        //   .doc("CC01")
        //   .update({
        //     last_access: new Date(),
        //   });

        window.location = "../dashboard/dashboard.html";
      };
    }
  }
}
