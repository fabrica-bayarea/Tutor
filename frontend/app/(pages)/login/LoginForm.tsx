'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import styles from './page.module.css';
import Image from 'next/image';

import { loginProfessor } from '@/app/services/service_professor';
import { loginAluno } from '@/app/services/service_aluno';

type UserType = 'aluno' | 'professor';

export default function LoginForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [userType, setUserType] = useState<UserType>('aluno');
    const [matricula, setMatricula] = useState<string>('');
    const [senha, setSenha] = useState<string>('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (userType === 'aluno') {
                await loginAluno(matricula, senha);
            } else if (userType === 'professor') {
                await loginProfessor(matricula, senha);
            }
            
            const returnTo = searchParams.get('returnTo') || `/${userType}`;
            router.push(returnTo);
        } catch (error) {
            console.error('Erro no login:', error);
        }
    };

    const isDisabled = !matricula || !senha;

    return (
        <div className={styles.contentContainer}>

            <h2 style={{marginTop:'1rem', marginBottom:'1rem'}}>Bem vindo ao Tutor!</h2>

            <form className={styles.formContainer} onSubmit={handleSubmit}>
                
                <div className={styles.inputsGrid}>
                    <label htmlFor="matricula">Login:</label>
                    <input
                        id="matricula"
                        name="matricula"
                        type="text"
                        required
                        title=''
                        className='inputItem'
                        placeholder="Login"
                        value={matricula}
                        onChange={(e) => setMatricula(e.target.value)}
                    />
                    <label htmlFor="senha">Senha:</label>
                    <input
                        id="senha"
                        name="senha"
                        type="password"
                        required
                        title=''
                        className='inputItem'
                        placeholder="Senha"
                        value={senha}
                        onChange={(e) => setSenha(e.target.value)}
                    />
                </div>

                <div className={styles.inputsContainer}>
                    <div className={styles.rememberForgotContainer}>
                        <label className={styles.rememberLabel}>
                        <input type="checkbox" className={styles.roundCheckbox} />
                        <span>Lembre-se</span>
                        </label>
                        <a className={styles.forgotPasswordLink} href="#">Esqueceu sua senha?</a>
                    </div>
                </div>

                <div className={styles.buttonsContainer}>
                    <button
                        type="submit"
                        disabled={isDisabled}
                        className={styles.loginBtn}
                    >
                        Entrar
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
                    <span className={styles.spanItem}>Se não tem conta registre-se</span>
                    <button
                        type="submit"
                        disabled={isDisabled}
                        className={styles.registerButton}
                    >
                        Registrar
                    </button>
                </div>

                <div className={styles.inputContainer}>
                    <span className={styles.spanItem}>Termos de Uso</span>
                    <span className={styles.spanItem}>Termos de Uso</span>
                </div>

            </form>
        </div>
    );
}