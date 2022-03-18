import app from "../firebase.js"
import {
    getFirestore, collection, onSnapshot,
    addDoc, deleteDoc, doc,
    query, where,
    orderBy, serverTimestamp,
    updateDoc, setDoc, getDocs
  } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js'
  const db = getFirestore()
  const colRef = collection(db, 'TEACHER')

  onSnapshot(colRef, async (snapshot) => {
      let teachers = [];
      snapshot.docs.forEach((doc) => {


          teachers.push(doc.id)
      })
      console.log("teachers:" + teachers);
      let courses = [];
    //   var did;
       for(let i =0 ; i < teachers.length; i++){
        
          await getDocs(collection(db, 'TEACHER', teachers[i], 'COURSE'))
            .then(   (snapshot) => {
                // console.log(snapshot.docs)
               snapshot.docs.forEach( async (doc) => {
                    // console.log(courses);
                    // var docid = await {id:doc.id};
                    // var l = [docid]
                    // console.log(JSON.stringify(l));
                    courses.push({T_id: teachers[i],
                    C_name: doc.id});
                    //   console.log(courses)
                    


            })
         
        });
        
    
         
      }
       console.log(courses)
    //   let Classes = []
    //   for( let i = 0; i < courses.length; i++){
    //     await getDocs(collection(db, 'teacher', courses[i].T_id, 'COURSE', courses[i].C_name, 'CLASS'))
    //         .then((snapshot) => {
    //         snapshot.docs.forEach((doc) => {
    //             // did = doc.id;
    //             Classes.push({T_id: courses[i].T_id,
    //                 C_name: courses[i].C_name, 
    //                 Class_name:doc.id,
    //             Semester: doc.data().Class_Semester,
    //             Lass_Access: doc.data().lass_access,
    //             Create_Date: doc.data().create})
    //             //  console.log(doc)

    //         })
         
    //     });

    //     //   getDocs(collection(db, 'TEACHER', courses[i].T_id, 'COURSE', courses[i].T_id))
    //   }
    //   console.log(Classes)
  })