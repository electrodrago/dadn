import app from "../firebase.js"
import {
    getFirestore, collection, onSnapshot,
    addDoc, deleteDoc, doc,
    query, where,
    orderBy, serverTimestamp,
    updateDoc, setDoc
  } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js'

  const db = getFirestore();
  const colRef = collection(db, 'teacher');

  
  Add.addEventListener('click', (e) => {
    e.preventDefault();
    var teacher_id = document.getElementById('exampleTeacherID').value ;
    var course_name = document.getElementById('exampleCourseName').value;
    var class_name = document.getElementById('exampleClassName').value;
    var semester = document.getElementById('exampleSemester').value;

    // console.log(document.getElementById('exampleFile').files[0]);
    Papa.parse(document.getElementById('exampleFile').files[0],{
      dowload: true,
      header: true,
      skipEmptyLines: true,
      complete: function(results){
        let lst = [];
        console.log(results.data.length)
        console.log(results.data)
        for(let i = 0; i < results.data.length; i++){
              lst.push(results.data[i].Key);
        }
        console.log(Object.values(lst));
        setDoc(doc(db,'teacher', teacher_id),{});
        setDoc(doc(db,'teacher', teacher_id, 'COURSE', course_name),{});
        setDoc(doc(db,'teacher', teacher_id, 'COURSE', course_name, 'CLASS',class_name),{});
        setDoc(doc(db,'teacher', teacher_id, 'COURSE', course_name, 'CLASS',class_name), {
          AnswerFile: lst,
          Class_Semester: semester,
          create: new Date(),
          lass_access: new Date(),
          })
        .then(() => {
          document.querySelector('.form-group').reset();
        })
        
      }
    })

    
  })

