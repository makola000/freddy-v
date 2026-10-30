// Freddy V - Firebase Connection - Durba
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getFirestore, collection, addDoc, getDocs, deleteDoc, doc } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCZTf68dJf0nir7IJ8QCPrVwB4EEEeclHM",
  authDomain: "freddy-v.firebaseapp.com",
  projectId: "freddy-v",
  storageBucket: "freddy-v.firebasestorage.app",
  messagingSenderId: "318263144332",
  appId: "1:318263144332:web:387b2ded7cf5b85d6eb0a9"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

// Fonctions pour Freddy V
export async function ajouterProduit(produit) {
  return await addDoc(collection(db, "produits"), produit);
}
export async function getProduits() {
  const snap = await getDocs(collection(db, "produits"));
  return snap.docs.map(d => ({id: d.id, ...d.data()}));
}
