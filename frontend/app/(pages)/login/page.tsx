import { Suspense } from 'react';
import LoginForm from './LoginForm';
import styles from './page.module.css';

export default function LoginPage() {
  return (
    <main className={styles.pageContainer}>
      <Suspense fallback={<div className={styles.contentContainer}>Carregando...</div>}>
        <LoginForm />
      </Suspense>
    </main>
  );
}