import { Suspense } from 'react';
import RegisterForm from './RegisterForm';
import styles from './page.module.css';

export default function LoginPage() {
  return (
    <main className={styles.pageContainer}>
      <Suspense fallback={<div className={styles.contentContainer}>Carregando...</div>}>
        <RegisterForm />
      </Suspense>
    </main>
  );
}