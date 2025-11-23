'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './page.module.css';
import Image from 'next/image';

// Aqui precisa implementar o service de registro
//import { registerAluno } from '@/app/services/service_aluno';
//import { registerProfessor } from '@/app/services/service_professor';

type UserType = 'aluno' | 'professor';

export default function RegisterForm() {
  const router = useRouter();
  const [userType, setUserType] = useState<UserType>('aluno');
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (userType === 'aluno') {
//        await registerAluno(nome, email, senha);
      } else {
//        await registerProfessor(nome, email, senha);
      }
      // Redireciona após registro
      router.push(`/${userType}`);
    } catch (error) {
      console.error('Erro no registro:', error);
    }
  };

  const isDisabled = !nome || !email || !senha;

  return (
    <div className={styles.contentContainer}>
      <h2 style={{ marginTop: '1rem', marginBottom: '1rem' }}>Crie sua conta no Tutor!</h2>

      <form className={styles.formContainer} onSubmit={handleSubmit}>
        <div className={styles.inputsGrid}>
          <label htmlFor="nome">Nome:</label>
          <input
            id="nome"
            name="nome"
            type="text"
            required
            placeholder="Nome completo"
            className="inputItem"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
          />

          <label htmlFor="email">Email:</label>
          <input
            id="email"
            name="email"
            type="email"
            required
            placeholder="Email"
            className="inputItem"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label htmlFor="senha">Senha:</label>
          <input
            id="senha"
            name="senha"
            type="password"
            required
            placeholder="Senha"
            className="inputItem"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
        </div>

        <div className={styles.buttonsContainer}>
          <button
            type="submit"
            disabled={isDisabled}
            className={styles.registerButton}
          >
            Registrar
          </button>

          <button className={styles.googleBtn}>
            <Image src="/googleIcon.png" width={30} height={30} alt="Ícone do Google" />
          </button>
        </div>

        <div className={styles.dividerContainer}>
          <hr className={styles.dividerLine} />
          <span className={styles.dividerText}>Ou</span>
          <hr className={styles.dividerLine} />
        </div>

        <div className={styles.inputContainerRegister}>
          <span className={styles.spanItem}>Já tem conta? Faça login</span>
        </div>

        <div className={styles.inputContainer}>
          <span className={styles.spanItem}>Termos de Uso</span>
          <span className={styles.spanItem}>Política de Privacidade</span>
        </div>
      </form>
    </div>
  );
}
