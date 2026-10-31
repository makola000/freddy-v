const firebaseConfig = {
  apiKey: "AIzaSyCZTfMR94q2t4W1c0N7LK5YpN14M8iBVvA",
  authDomain: "freddy-v.firebaseapp.com",
  projectId: "freddy-v",
  storageBucket: "freddy-v.firebasestorage.app",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}
const db = firebase.firestore();

function compterVue(videoId, createurId) {
  const gainTotal = 0.01;
  const gainCreateur = gainTotal * 0.8;
  const gainFreddy = gainTotal * 0.2;
  db.collection("videos").doc(videoId).set({vues: firebase.firestore.FieldValue.increment(1)}, {merge:true});
  db.collection("revenus").doc(createurId).set({vuesTotales: firebase.firestore.FieldValue.increment(1), revenuTotal: firebase.firestore.FieldValue.increment(gainCreateur), monArgent: firebase.firestore.FieldValue.increment(gainCreateur)}, {merge:true});
  db.collection("revenus").doc("FREDDY-V-PLATFORM").set({partFreddyV: firebase.firestore.FieldValue.increment(gainFreddy)}, {merge:true});
}
