'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { BookMarked, KeyRound } from 'lucide-react';

import styles from './tokenValidate.module.css';
import Input from '@/app/components/Input/Input';
import Button from '@/app/components/Button/Button';
import Toast from '@/app/components/Toast/Toast';
import { validarToken } from '@/app/services/service_auth';
import { div } from 'framer-motion/client';

function TokenValidate() {
    const router = useRouter();
    const searchParams = useSearchParams();

    const [token, setToken] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [autoValidating, setAutoValidating] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    useEffect(() => {
        const tokenParam = searchParams?.get('token');
        if (tokenParam) {
            setToken(tokenParam);
            handleAutoValidate(tokenParam);
        }
    }, []);

    const handleAutoValidate = async (tokenValue: string) => {
        setAutoValidating(true);
        setErrorMessage(null);

        try {
            const result = await validarToken(tokenValue);

            if (!result.ok) {
                setErrorMessage(
                    'Este link já foi utilizado ou é inválido. Utilize a opção "Esqueci minha senha" para redefinir seu acesso.'
                );
                return;
            }

            router.push(`/alterar-senha?token=${encodeURIComponent(tokenValue)}`);
        } catch {
            setErrorMessage('Erro ao validar o token. Tente novamente em instantes.');
        } finally {
            setAutoValidating(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        setLoading(true);

        try {
            const result = await validarToken(token.trim());

            if (!result.ok) {
                setErrorMessage(
                    'Este link já foi utilizado ou é inválido. Utilize a opção "Esqueci minha senha" para redefinir seu acesso.'
                );
                return;
            }

            router.push(`/alterar-senha?token=${encodeURIComponent(token.trim())}`);
        } catch {
            setErrorMessage('Erro ao validar o token. Tente novamente em instantes.');
        } finally {
            setLoading(false);
        }
    };

    const isDisabled = !token.trim() || loading || autoValidating;
    const isProcessing = loading || autoValidating;

    return (
        <div className={styles.contentContainer}>

            <div className={styles.brandHeader}>
                <div className={styles.asideLogo}>
                    <BookMarked size={22} strokeWidth={2.4} />
                </div>
                <span className={styles.asideBrandName}>Tutor</span>
            </div>

            <div className={styles.iconWrapper}>
                <KeyRound size={28} strokeWidth={2} className={styles.pageIcon} />
            </div>

            <h2 className={styles.welcomeTitle}>Validar token de acesso</h2>
            <p className={styles.welcomeSubtitle}>
                {autoValidating
                    ? 'Verificando seu token...'
                    : 'Insira o token recebido no seu e-mail para continuar.'}
            </p>

            <form className={styles.formContainer} onSubmit={handleSubmit}>

                <Input
                    id="token"
                    name="token"
                    label="Token de acesso"
                    type="text"
                    required
                    value={token}
                    onChange={(e) => setToken(e.target.value)}
                    disabled={isProcessing}
                    invalid={!!errorMessage}
                />

                <Button
                    type="submit"
                    style="filled"
                    action="primary"
                    fullWidth
                    label={isProcessing ? 'Validando...' : 'Validar token'}
                    isDisabled={isDisabled}
                />

            </form>

            <p className={styles.helperText}>
                Não recebeu o e-mail?{' '}
                <a className={styles.forgotPasswordLink} href="/tutor/esqueci-senha">
                    Esqueci minha senha
                </a>
            </p>

            {errorMessage && (
                <Toast
                    message={errorMessage}
                    type="error"
                    onClose={() => setErrorMessage(null)}
                />
            )}

        </div>
    );
}

export default function ValidateTokenPage() {
    return (
        <Suspense fallback={<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>Carregando...</div>}>
            <TokenValidate />
        </Suspense>
    );
}
