'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Image from 'next/image';
import Script from 'next/script';

import styles from './page.module.css';
import { loginAluno, loginAlunoGoogle } from '@/app/services/service_aluno';

type UserType = 'aluno' | 'professor' | 'admin';

declare global {
  interface Window {
    google: any;
  }
}

export default function LoginForm() {
    const router = useRouter();
    const searchParams = useSearchParams();

    const [userType, setUserType] = useState<UserType>('aluno');
    const [matricula, setMatricula] = useState<string>('');
    const [senha, setSenha] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const googleId = "__GOOGLE_ID_PLACEHOLDER__";

    // ----------- LOGIN COM FORMULÁRIO -----------
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        setLoading(true);

        try {
            let aluno = await loginAluno(matricula, senha);

            if (!aluno) {
                setErrorMessage("Credenciais inválidas");
                setLoading(false);
                return;
            }
            console.log(aluno.role);
            const destino = '/chat';

            router.push(destino);

        } catch (error) {
            console.error('Erro no login:', error);
            setErrorMessage("Erro ao realizar login");
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = async (response: any) => {
        try {
            setLoading(true);

            const googleToken = response.credential;

            const aluno = await loginAlunoGoogle(googleToken);

            if (!aluno) {
                setErrorMessage("Falha no login com Google");
                setLoading(false);
                return;
            }

            const destino = '/chat';

            router.push(destino);

        } catch (error) {
            console.error("Erro no login Google:", error);
            setErrorMessage("Erro ao tentar login com Google");
        } finally {
            setLoading(false);
        }
    };

    const isDisabled = !matricula || !senha || loading;

    return (
        <div className={styles.contentContainer}>

            <h2 style={{ marginTop: '1rem', marginBottom: '1rem' }}>
                Bem vindo ao Tutor!
            </h2>

            <form className={styles.formContainer} onSubmit={handleSubmit}>

                <div className={styles.inputsGrid}>
                    <label htmlFor="matricula">Matrícula:</label>
                    <input
                        id="matricula"
                        name="matricula"
                        type="text"
                        required
                        className='inputItem'
                        placeholder="Matrícula"
                        value={matricula}
                        onChange={(e) => setMatricula(e.target.value)}
                    />

                    <label htmlFor="senha">Senha:</label>
                    <input
                        id="senha"
                        name="senha"
                        type="password"
                        required
                        className='inputItem'
                        placeholder="Senha"
                        value={senha}
                        onChange={(e) => setSenha(e.target.value)}
                    />
                </div>

                {errorMessage && (
                    <p style={{ color: 'red', marginTop: '0.5rem' }}>
                        {errorMessage}
                    </p>
                )}
                <div className={styles.inputsContainer}>
                    <div className={styles.rememberForgotContainer}>
                        <label className={styles.rememberLabel}>
                            <input type="checkbox" className={styles.roundCheckbox} />
                            <span>Lembre-se</span>
                        </label>
                        <a className={styles.forgotPasswordLink} href="#">
                            Esqueceu sua senha?
                        </a>
                    </div>
                </div>

                <div className={styles.buttonsContainer}>
                    <button
                        type="submit"
                        disabled={isDisabled}
                        className={styles.loginBtn}
                    >
                        {loading ? "Entrando..." : "Entrar"}
                    </button>
                    <div id="googleBtn" className={styles.googleBtn}></div>
                </div>

                <div className={styles.dividerContainer}>
                    <hr className={styles.dividerLine} />
                    <span className={styles.dividerText}>Ou</span>
                    <hr className={styles.dividerLine} />
                </div>

                <div className={styles.inputContainerRegister}>
                    <span className={styles.spanItem}>
                        Se não tem conta registre-se
                    </span>
                    <button
                        type="button"
                        className={styles.registerButton}
                        onClick={() => router.push('/register')}
                    >
                        Registrar
                    </button>
                </div>

                <div className={styles.inputContainer}>
                    <span className={styles.spanItem}>Termos de Uso</span>
                    <span className={styles.spanItem}>Política de Privacidade</span>
                </div>

            </form>

            <Script
                src="https://accounts.google.com/gsi/client"
                strategy="lazyOnload"
                onLoad={() => {
                    if (!window.google) return;

                    window.google.accounts.id.initialize({
                        client_id: googleId,
                        callback: handleGoogleLogin,
                    });

                    window.google.accounts.id.renderButton(
                    document.getElementById("googleBtn"),
                    {
                        type: "icon",
                        theme: "outline",
                        size: "large",
                        shape: "circle",
                        logo_alignment: "center",
                    }
                    );
                }}
            />

        </div>
    );
}
