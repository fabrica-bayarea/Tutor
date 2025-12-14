'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './page.module.css';
import Image from 'next/image';

import { criarAluno } from '@/app/services/service_aluno';

export default function RegisterForm() {
  const router = useRouter();

  const [nome, setNome] = useState('');
  const [matricula, setMatricula] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setLoading(true);

    try {
      const aluno = await criarAluno(matricula, nome, email, senha);
      router.push('/login');
    }
    catch (error: any) {
        if (error.response?.status === 409) {
            console.error("Usuário já existe:", error)  ;
            setErrorMessage("Email ou matrícula já cadastrados.");
        } else {
            console.error("Erro ao criar o aluno:", error);
            setErrorMessage("Erro ao criar o aluno.");
        }
        return null;
    }finally {
      setLoading(false);
    }
  };

  const isDisabled = !nome || !matricula || !email || !senha || loading;

  return (
    <div className={styles.contentContainer}>
      <h2 style={{ marginTop: '1rem', marginBottom: '1rem' }}>
        Crie sua conta no Tutor!
      </h2>

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

          <label htmlFor="matricula">Matrícula:</label>
          <input
            id="matricula"
            name="matricula"
            type="text"
            required
            placeholder="Matrícula"
            className="inputItem"
            value={matricula}
            onChange={(e) => setMatricula(e.target.value)}
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

        {errorMessage && (
          <p style={{ color: 'red', marginTop: '0.5rem' }}>{errorMessage}</p>
        )}

        <div className={styles.buttonsContainer}>
          <button
            type="submit"
            disabled={isDisabled}
            className={styles.registerButton}
          >
            {loading ? "Registrando..." : "Registrar"}
          </button>
        </div>

        <div className={styles.dividerContainer}>
          <hr className={styles.dividerLine} />
          <span className={styles.dividerText}>Ou</span>
          <hr className={styles.dividerLine} />
        </div>

        <div className={styles.inputContainerRegister}>
          <span className={styles.spanItem}>Já tem conta? <a href="/login">Faça login</a></span>
        </div>
        <div className={styles.inputContainer}>
          <span className={styles.spanItem}>Termos de Uso</span>
          <span className={styles.spanItem}>Política de Privacidade</span>
        </div>
      </form>
    </div>
  );
}
