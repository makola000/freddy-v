// FREDDY-V FIREBASE SIMPLE - VERSION MOBILE avec argent
const firebaseConfig = {
  apiKey: "AIzaSyCZTf68dJf0nir7IJ8QCPrVwB4EEEeclHM",
  authDomain: "freddy-v.firebaseapp.com",
  projectId: "freddy-v",
  storageBucket: "freddy-v.firebasestorage.app",
  messagingSenderId: "318263144332",
  appId: "1:318263144332:web:387b2ded7cf5b85d6eb0a9"
};

// Initialiser Firebase (mode compat pour mobile)
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}
const db = firebase.firestore();

// COMPTER UNE VUE = +$0.01
function compterVue(videoId, createurId) {
  const gain = 0.01;

  // 1. Augmente vues vidéo
  db.collection("videos").doc(videoId).set({
    vues: firebase.firestore.FieldValue.increment(1)
  }, {merge:true});

  // 2. Augmente revenus créateur
  db.collection("revenus").doc(createurId).set({
    vuesTotales: firebase.firestore.FieldValue.increment(1),
    revenuTotal: firebase.firestore.FieldValue.increment(gain),
    monArgent: firebase.firestore.FieldValue.increment(gain),
    partFreddyV: firebase.firestore.FieldValue.increment(0)
  }, {merge:true});

  console.log("Vue + $0.01 OK");
}

// AFFICHER REVENUS dans revenus.html
function afficherRevenus(createurId) {
  db.collection("revenus").doc(createurId).onSnapshot(doc => {
    if (doc.exists) {
      const data = doc.data();
      document.getElementById('monArgent').innerText = data.monArgent || 0;
      document.getElementById('vuesTotales').innerText = data.vuesTotales || 0;
    }
  });
}
