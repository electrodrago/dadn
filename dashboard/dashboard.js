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

// Get variable
var teacher_id = localStorage.getItem("T_id");
var course_name = localStorage.getItem("C_name");
var class_name = localStorage.getItem("Class_name");
var create_date = localStorage.getItem("Create_Date");
var semester = localStorage.getItem("Semester");

// Update last_access
const laRef = doc(
  db,
  "TEACHER",
  teacher_id,
  "COURSE",
  course_name,
  "CLASS",
  class_name
);
updateDoc(laRef, { last_access: serverTimestamp() });

console.log("Done !!!");
console.log("Teacher ID: ", teacher_id, " Course: ", course_name);
let Classes = [];
onSnapshot(colRef, async (snapshot) => {
  Classes.push({
    T_id: teacher_id,
    C_name: course_name,
    Class_name: class_name,
    Semester: semester,
  });
  console.log("Danh sach lop: ", Classes);
  document.getElementById("course_name").innerHTML += `${
    Classes[0].C_name +
    " - " +
    Classes[0].Class_name +
    " - " +
    Classes[0].Semester +
    ")"
  }`;
  var Score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; // so luong hoc sinh co diem tu 0 -> 10
  await getDocs(
    collection(
      db,
      "TEACHER",
      Classes[0].T_id,
      "COURSE",
      Classes[0].C_name,
      "CLASS",
      Classes[0].Class_name,
      "STUDENT"
    )
  ).then((snapshot) => {
    snapshot.docs.forEach((doc) => {
      // did = doc.id;
      Score[parseInt(doc.data().S_Point)] += 1;
      //console.log(doc.data().S_Point);
    });
  });
  console.log(Score);

  //localStorage.setItem("Score", Score);
  Draw_Bar(Score);
  Draw_Pie(Score);
});

function dynamicColors() {
  var r = Math.floor(Math.random() * 255);
  var g = Math.floor(Math.random() * 255);
  var b = Math.floor(Math.random() * 255);
  return "rgba(" + r + "," + g + "," + b + ", 0.6)";
}
function poolColors(a) {
  var pool = [];
  for (var i = 0; i < a; i++) {
    pool.push(dynamicColors());
  }
  return pool;
}

function Draw_Bar(yValues) {
  var xValues = [
    "0 Point",
    "1 Point",
    "2 Point",
    "3 Point",
    "4 Point",
    "5 Point",
    "6 Point",
    "7 Point",
    "8 Point",
    "9 Point",
    "10 Point",
  ];

  //var yValues = localStorage.getItem("Score");
  console.log("yValues: ", yValues);
  new Chart("myChart", {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [
        {
          label: "Number of students: ",
          backgroundColor: poolColors(yValues.length),
          borderColor: poolColors(yValues.length),
          data: yValues,
        },
      ],
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text:
          "Distribution of points in class: " +
          Classes[0].C_name +
          " - " +
          Classes[0].Class_name +
          " - " +
          Classes[0].Semester,
      },
    },
  });
}
google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(Draw_Pie);
function Draw_Pie(yValues) {
  var arr = [["Mark", "Total of students"]];
  for (let i = 0; i < yValues.length; i++) {
    arr.push([i + " point", yValues[i]]);
  }
  console.log(yValues);
  console.log(arr);
  var data = google.visualization.arrayToDataTable(arr);
  var options = {
    title:
      "Distribution of mark in class: " +
      Classes[0].C_name +
      " - " +
      Classes[0].Class_name +
      " - " +
      Classes[0].Semester,
    height: 400,
    width_units: "%",
  };

  var my_div = document.getElementById("piechart");
  var chart = new google.visualization.PieChart(
    document.getElementById("piechart")
  );
  google.visualization.events.addListener(chart, "ready", function () {
    my_div.innerHTML = '<img src="' + chart.getImageURI() + '">';
  });
  chart.draw(data, options);
  console.log("done");
}
