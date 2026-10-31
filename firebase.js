// FREDDY-V FIREBASE SIMPLE - VERSION MOBILE
const firebaseConfig = {
  apiKey: "COLLE TON API KEY ICI",
  authDomain: "freddy-v.firebaseapp.com",
  projectId: "freddy-v",
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
    monArgent: firebase.firestore.FieldValue.increment(gain * 0.8),
    partFreddyV: firebase.firestore.FieldValue.increment(gain * 0.2)
  }, {merge:true});

  console.log("Vue + $0.01 OK");
}

// AFFICHER REVENUS dans revenus.html
function afficherRevenus(createurId) {
  db.collection("revenus").doc(createurId).onSnapshot((doc) => {
    if (doc.exists) {
      const d = doc.data();
      if(document.getElementById("vues-totales")) {
        document.getElementById("vues-totales").innerText = d.vuesTotales || 0;
        // Tu as "Vues totales: 0" dans ton HTML, on met à jour
      }
      // Pour ton HTML actuel avec texte complet
      const elVues = document.querySelector("body");
      if(elVues) {
        // On cherche et remplace
        document.body.innerHTML = document.body.innerHTML.replace(/Vues totales: \d+/, `Vues totales: ${d.vuesTotales||0}`);
      }
    }
  });
}
