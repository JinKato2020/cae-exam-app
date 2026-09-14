// Firebase Authentication の薄いラッパ。メール＋パスワードのサインイン/登録/ログアウト/削除。
// Google/Apple ログインは OAuth 設定後に別ファイルで追加する。
import {
  onAuthStateChanged,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  deleteUser,
  type User,
} from 'firebase/auth';
import { auth } from '../config/firebase';

export type { User };

// ログイン状態の変化を購読（起動時に保存済みセッションを自動復元）。返り値は購読解除関数。
export function onAuthChange(cb: (user: User | null) => void): () => void {
  return onAuthStateChanged(auth, cb);
}

export function currentUser(): User | null {
  return auth.currentUser;
}

export async function signUpEmail(email: string, password: string): Promise<User> {
  const cred = await createUserWithEmailAndPassword(auth, email.trim(), password);
  return cred.user;
}

export async function signInEmail(email: string, password: string): Promise<User> {
  const cred = await signInWithEmailAndPassword(auth, email.trim(), password);
  return cred.user;
}

export async function signOutUser(): Promise<void> {
  await signOut(auth);
}

// アカウント削除（App Store 審査で必須）。直近ログインが古いと requires-recent-login を投げる。
export async function deleteAccount(): Promise<void> {
  const u = auth.currentUser;
  if (!u) return;
  await deleteUser(u);
}

// Firebase のエラーコードを、素人にも分かるやさしい日本語に変換する。
export function authErrorMessage(e: any): string {
  const code: string = (e && e.code) || '';
  switch (code) {
    case 'auth/invalid-email':
      return 'メールアドレスの形式が正しくありません。';
    case 'auth/missing-password':
      return 'パスワードを入力してください。';
    case 'auth/weak-password':
      return 'パスワードは6文字以上にしてください。';
    case 'auth/email-already-in-use':
      return 'このメールアドレスは既に登録されています。「ログイン」をお試しください。';
    case 'auth/invalid-credential':
    case 'auth/wrong-password':
    case 'auth/user-not-found':
      return 'メールアドレスまたはパスワードが違います。';
    case 'auth/too-many-requests':
      return '試行が多すぎます。しばらく待ってから再度お試しください。';
    case 'auth/network-request-failed':
      return '通信に失敗しました。電波の良い場所で再度お試しください。';
    case 'auth/requires-recent-login':
      return '安全のため、一度ログインし直してから削除してください。';
    default:
      return 'エラーが発生しました。時間をおいて再度お試しください。';
  }
}
