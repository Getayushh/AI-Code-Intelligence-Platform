// ═══════════════════════════════════════
//   firebase.js — Auth helpers for CodeIntel
// ═══════════════════════════════════════
 
// ✅ Both imports use the SAME version (10.7.1)
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile
} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBK1H4DnUWZHEvL0TmNwBdzggHwwttaDRU",
  authDomain: "ai-codeintelligence.firebaseapp.com",
  projectId: "ai-codeintelligence",
  storageBucket: "ai-codeintelligence.firebasestorage.app",
  messagingSenderId: "99981697205",
  appId: "1:99981697205:web:5c297b5768e384ad9b5efc"
};

  // Initialize Firebase
const app  = initializeApp(firebaseConfig);
const auth = getAuth(app);
 
// 🔐 Email Login  (defined once — was duplicated before)
export async function loginEmail(email, password) {
  return await signInWithEmailAndPassword(auth, email, password);
}
 
// 🆕 Email Signup
export async function signupEmail(email, password, name) {
  const userCred = await createUserWithEmailAndPassword(auth, email, password);
  await updateProfile(userCred.user, { displayName: name });
  return userCred;
}
 
// 🌐 Google Login
export async function loginGoogle() {
  const provider = new GoogleAuthProvider();
  return await signInWithPopup(auth, provider);
}
 
// 🔁 Auth State Listener
export function onAuthChange(callback) {
  onAuthStateChanged(auth, callback);
}
 
// 🚪 Logout
export async function logout() {
  return await signOut(auth);
}