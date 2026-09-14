// Firebase 初期化(CAE専用プロジェクト・Web SDK/JS版)。
// この firebaseConfig はアプリに埋め込む前提の公開情報。保護は Firestore セキュリティルールで行う。
import { initializeApp, getApps, getApp } from 'firebase/app';
import { initializeAuth, getAuth, type Auth } from 'firebase/auth';
// getReactNativePersistence は実行時には存在するが、firebase/auth の型定義から欠けるバージョンがある。
// @ts-ignore
import { getReactNativePersistence } from 'firebase/auth';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getFirestore, initializeFirestore, type Firestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: 'AIzaSyB4SsKJOeVehJuhqtdRwMtJcZMXkO37FGY',
  authDomain: 'cae-exam-5c6d9.firebaseapp.com',
  projectId: 'cae-exam-5c6d9',
  storageBucket: 'cae-exam-5c6d9.firebasestorage.app',
  messagingSenderId: '91189886602',
  appId: '1:91189886602:web:817fabb895c7eb743af773',
};

const app = getApps().length ? getApp() : initializeApp(firebaseConfig);

// initializeAuth は二重初期化(Fast Refresh 等)で例外を投げるため getAuth にフォールバック。
let auth: Auth;
try {
  auth = initializeAuth(app, {
    persistence: getReactNativePersistence(AsyncStorage),
  });
} catch {
  auth = getAuth(app);
}

export { app, auth };

// React Native では通常の接続方式で Firestore がつながらないことがあるため、
// 長ポーリングを強制する。initializeFirestore は二重初期化で例外→getFirestore にフォールバック。
let db: Firestore;
try {
  db = initializeFirestore(app, { experimentalForceLongPolling: true });
} catch {
  db = getFirestore(app);
}
export { db };
