import app from "../firebase.js"
import {
    getFirestore, collection, onSnapshot,
    addDoc, deleteDoc, doc,
    query, where,
    orderBy, serverTimestamp,
    updateDoc, setDoc
  } from 'https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js'
  const db = getFirestore()
  const colRef = collection(db, 'teacher')
  onSnapshot(colRef, (snapshot) => {
      let books = [];
      console.log(snapshot);
      snapshot.docs.forEach((doc) => {
          books.push({...doc.data(), id: doc.id})
      })
      console.log(books)
  })