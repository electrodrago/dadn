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
const db = getFirestore();
const colRef = collection(db, "TEACHER");

onSnapshot(colRef, async (snapshot) => {
  let teachers = [];
  snapshot.docs.forEach((doc) => {
    teachers.push(doc.id);
  });
  console.log("teachers:" + teachers);
  let courses = [];
  //   var did;
  for (let i = 0; i < teachers.length; i++) {
    await getDocs(collection(db, "TEACHER", teachers[i], "COURSE")).then(
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
        "TEACHER",
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
          Semester: doc.data().Class_Semester,
          Last_Access: doc.data().last_access.toDate(),
          Create_Date: doc.data().create.toDate(),
        });
        //  console.log(doc)
      });
    });

    //   getDocs(collection(db, 'TEACHER', courses[i].T_id, 'COURSE', courses[i].T_id))
  }
  Classes.sort(function (a, b) {
    return b.Last_Access - a.Last_Access;
  });
  console.log("Classes: ", Classes);

  for (let i = 0; i < Classes.length; i++) {
    document.getElementById("--T-body").innerHTML += `
      <tr>
        <td>${Classes[i].T_id}</td>
        <td>${
          Classes[i].C_name +
          " - " +
          Classes[i].Class_name +
          " - " +
          Classes[i].Semester
        }</td>
        <td>${Classes[i].Create_Date}</td>
        <td>${Classes[i].Last_Access}</td>
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
      rows[i].onclick = function () {
        T_id = table.rows[this.i].cells[0].innerHTML;
        var temp = table.rows[this.i].cells[1].innerHTML;
        console.log(temp);
        C_name = temp.substr(0, temp.indexOf(" - "));
        Class_name = temp.slice(
          C_name.length + 3,
          temp.indexOf(" - ", C_name.length + 3)
        );
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
