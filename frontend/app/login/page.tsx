'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import styles from './page.module.css';

import { loginProfessor } from '@/app/services/service_professor';
import { loginAluno } from '@/app/services/service_aluno';

type UserType = 'aluno' | 'professor';

export default function LoginPage() {
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
        <main className={styles.pageContainer}>
            <div className={styles.contentContainer}>
                <h2>Faça login</h2>
                <div className={styles.segmentedButtonContainer}>
                    <button
                        type="button"
                        onClick={() => setUserType('aluno')}
                        className={`${userType === 'aluno' ? styles.selected : ''}`}
                    >
                        Aluno
                    </button>
                    <button
                        type="button"
                        onClick={() => setUserType('professor')}
                        className={`${userType === 'professor' ? styles.selected : ''}`}
                    >
                        Professor
                    </button>
                </div>

                <form className={styles.formContainer} onSubmit={handleSubmit}>
                    <div className={styles.inputsContainer}>
                        <div className={styles.inputContainer}>
                            <label htmlFor="matricula" className="sr-only">
                                Matrícula
                            </label>
                            <input
                                id="matricula"
                                name="matricula"
                                type="text"
                                required
                                title='' // Para remover o title que aparece por padrão
                                placeholder="Matrícula"
                                value={matricula}
                                onChange={(e) => setMatricula(e.target.value)}
                            />
                        </div>
                        <div className={styles.inputContainer}>
                            <label htmlFor="password" className="sr-only">
                                Senha
                            </label>
                            <input
                                id="senha"
                                name="senha"
                                type="password"
                                required
                                title='' // Para remover o title que aparece por padrão
                                placeholder="Senha"
                                value={senha}
                                onChange={(e) => setSenha(e.target.value)}
                            />
                            <a className={styles.forgotPasswordLink} href="#">Esqueceu sua senha?</a>
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={isDisabled}
                            className={styles.loginButton}
                        >
                            Entrar
                        </button>
                    </div>
                </form>
            </div>
        </main>
    );
}
