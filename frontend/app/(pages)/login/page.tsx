'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Script from 'next/script';
import { useAuth } from '@/utils/auth';

import styles from './page.module.css';
import { loginAluno, loginAlunoGoogle, LoginErrorCode } from '@/app/services/service_aluno';
import { BookMarked } from 'lucide-react';
import { FcGoogle } from 'react-icons/fc';
import Input from '@/app/components/Input/Input';
import Button from '@/app/components/Button/Button';
import Toast from '@/app/components/Toast/Toast';

declare global {
  interface Window {
    google: any;
  }
}

function LoginContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const { refreshUser, isStudent, isProfessor, isAdmin } = useAuth();
    const [matricula, setMatricula] = useState<string>('');
    const [senha, setSenha] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [showSessionExpiredToast, setShowSessionExpiredToast] = useState<boolean>(false);
    const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

    useEffect(() => {
        if (searchParams?.get('returnTo')) {
            setShowSessionExpiredToast(true);
        }
    }, [searchParams]);

    const messageForError = (code: LoginErrorCode): string => {
        switch (code) {
            case "deactivated":
                return "Sua conta está desativada. Entre em contato com o administrador da sua instituição para reativá-la.";
            case "invalid_credentials":
                return "Matrícula ou senha incorretos. Verifique e tente novamente.";
            default:
                return "Erro ao realizar login. Tente novamente em instantes.";
        }
    };

    const redirectAfterLogin = () => {
        let destino = "";
        if (isAdmin) destino = "/admin";
        else if (isProfessor) destino = "/professor";
        else if (isStudent) destino = "/chat";

        router.push(destino);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        setLoading(true);

        try {
            const result = await loginAluno(matricula, senha);

            if (!result.ok) {
                setErrorMessage(messageForError(result.error));
                return;
            }

            await refreshUser();
            redirectAfterLogin();

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
            const result = await loginAlunoGoogle(googleToken);

            if (!result.ok) {
                setErrorMessage(messageForError(result.error));
                return;
            }

            await refreshUser();
            redirectAfterLogin();

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

            <div className={styles.brandHeader}>
                <div className={styles.asideLogo}>
                    <BookMarked size={22} strokeWidth={2.4} />
                </div>
                <span className={styles.asideBrandName}>Tutor</span>
            </div>

            <h2 className={styles.welcomeTitle}>Bem-vindo ao Tutor</h2>
            <p className={styles.welcomeSubtitle}>Faça login para continuar</p>

            <form className={styles.formContainer} onSubmit={handleSubmit}>

                <Input
                    id="matricula"
                    name="matricula"
                    label="Matrícula"
                    type="text"
                    required
                    value={matricula}
                    onChange={(e) => setMatricula(e.target.value)}
                    disabled={loading}
                    invalid={!!errorMessage}
                />

                <Input
                    id="senha"
                    name="senha"
                    label="Senha"
                    type="password"
                    required
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                    disabled={loading}
                    invalid={!!errorMessage}
                />

                <a className={styles.forgotPasswordLink} href="#">
                    Esqueci minha senha
                </a>

                <Button
                    type="submit"
                    style="filled"
                    action="primary"
                    fullWidth
                    label={loading ? "Entrando..." : "Entrar"}
                    isDisabled={isDisabled}
                />

                <div className={styles.dividerContainer}>
                    <hr className={styles.dividerLine} />
                    <span className={styles.dividerText}>ou</span>
                    <hr className={styles.dividerLine} />
                </div>

                <div className={styles.googleBtnWrapper}>
                    <Button
                        type="button"
                        style="filled"
                        action="secondary"
                        fullWidth
                        icon={<FcGoogle size={20} />}
                        label="Continuar com Google"
                        isDisabled={loading}
                    />
                    <div
                        id="googleBtn"
                        className={`${styles.googleBtnOverlay} ${loading ? styles.googleBtnDisabled : ''}`}
                        aria-hidden="true"
                    ></div>
                </div>

            </form>

            <Script
                src="https://accounts.google.com/gsi/client"
                strategy="lazyOnload"
                onLoad={() => {
                    if (!window.google) return;

                    window.google.accounts.id.initialize({
                        client_id: GOOGLE_CLIENT_ID,
                        callback: handleGoogleLogin,
                    });

                    window.google.accounts.id.renderButton(
                    document.getElementById("googleBtn"),
                    {
                        type: "standard",
                        theme: "outline",
                        size: "large",
                        shape: "rectangular",
                        text: "continue_with",
                        logo_alignment: "left",
                        width: 400,
                    }
                    );
                }}
            />

            {errorMessage && (
                <Toast
                    message={errorMessage}
                    type="error"
                    onClose={() => setErrorMessage(null)}
                />
            )}

            {showSessionExpiredToast && !errorMessage && (
                <Toast
                    message="Sua sessão expirou. Por favor, faça login novamente."
                    type="error"
                    onClose={() => setShowSessionExpiredToast(false)}
                />
            )}

        </div>
    );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div className={styles.contentContainer}>Carregando...</div>}>
      <LoginContent />
    </Suspense>
  );
}
