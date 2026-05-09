'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { BookMarked, ShieldCheck } from 'lucide-react';

import styles from './alterarSenha.module.css';
import Input from '@/app/components/Input/Input';
import Button from '@/app/components/Button/Button';
import Toast from '@/app/components/Toast/Toast';
import { criarSenha } from '@/app/services/service_auth';

interface RegrasSenha {
    minCaracteres: boolean;
    maiuscula: boolean;
    minuscula: boolean;
    numero: boolean;
    senhasIguais: boolean;
}

function validarSenha(senha: string, confirmacao: string): RegrasSenha {
    return {
        minCaracteres: senha.length >= 8,
        maiuscula: /[A-Z]/.test(senha),
        minuscula: /[a-z]/.test(senha),
        numero: /[0-9]/.test(senha),
        senhasIguais: senha.length > 0 && senha === confirmacao,
    };
}

function IndicadorRegra({ valida, texto }: { valida: boolean; texto: string }) {
    return (
        <span className={`${styles.regra} ${valida ? styles.regraValida : styles.regraInvalida}`}>
            <span className={styles.regraIcone}>{valida ? '✓' : '·'}</span>
            {texto}
        </span>
    );
}

function AlterarSenha() {
    const router = useRouter();
    const searchParams = useSearchParams();

    const [token, setToken] = useState<string>('');
    const [novaSenha, setNovaSenha] = useState<string>('');
    const [confirmacaoSenha, setConfirmacaoSenha] = useState<string>('');
    const [mostrarNovaSenha, setMostrarNovaSenha] = useState<boolean>(false);
    const [mostrarConfirmacao, setMostrarConfirmacao] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [tokenInvalido, setTokenInvalido] = useState<boolean>(false);

    const regras = validarSenha(novaSenha, confirmacaoSenha);
    const senhaValida = Object.values(regras).every(Boolean);

    useEffect(() => {
        const tokenParam = searchParams?.get('token');
        if (!tokenParam) {
            // Sem token na URL — redireciona para validação
            router.replace('/token-validate');
            return;
        }
        setToken(tokenParam);
    }, [searchParams, router]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);

        if (!senhaValida) {
            setErrorMessage('A senha não atende todos os requisitos.');
            return;
        }

        setLoading(true);

        try {
            const result = await criarSenha(token, novaSenha);

            if (!result.ok) {
                if (result.status === 410) {
                    setTokenInvalido(true);
                    setErrorMessage(
                        'Este link já foi utilizado ou é inválido. Utilize a opção "Esqueci minha senha" para redefinir seu acesso.'
                    );
                } else {
                    setErrorMessage('Erro ao criar a senha. Tente novamente em instantes.');
                }
                return;
            }

            router.push('/login?senhaCriada=1');
        } catch {
            setErrorMessage('Erro ao criar a senha. Tente novamente em instantes.');
        } finally {
            setLoading(false);
        }
    };

    const isDisabled = !senhaValida || loading;

    return (
        <div className={styles.contentContainer}>

            <div className={styles.brandHeader}>
                <div className={styles.asideLogo}>
                    <BookMarked size={22} strokeWidth={2.4} />
                </div>
                <span className={styles.asideBrandName}>Tutor</span>
            </div>

            <div className={styles.iconWrapper}>
                <ShieldCheck size={28} strokeWidth={2} className={styles.pageIcon} />
            </div>

            <h2 className={styles.welcomeTitle}>Criar sua senha</h2>
            <p className={styles.welcomeSubtitle}>
                Defina uma senha segura para acessar a plataforma.
            </p>

            <form className={styles.formContainer} onSubmit={handleSubmit}>

                <div className={styles.inputPasswordWrapper}>
                    <Input
                        id="novaSenha"
                        name="novaSenha"
                        label="Nova senha"
                        type={mostrarNovaSenha ? 'text' : 'password'}
                        required
                        value={novaSenha}
                        onChange={(e) => setNovaSenha(e.target.value)}
                        disabled={loading || tokenInvalido}
                        invalid={!!errorMessage && !senhaValida}
                    />
                    <button
                        type="button"
                        className={styles.toggleSenha}
                        onClick={() => setMostrarNovaSenha((v) => !v)}
                        aria-label={mostrarNovaSenha ? 'Ocultar senha' : 'Mostrar senha'}
                        tabIndex={-1}
                    >
                        {mostrarNovaSenha ? '🙈' : '👁️'}
                    </button>
                </div>

                <div className={styles.inputPasswordWrapper}>
                    <Input
                        id="confirmacaoSenha"
                        name="confirmacaoSenha"
                        label="Confirmar senha"
                        type={mostrarConfirmacao ? 'text' : 'password'}
                        required
                        value={confirmacaoSenha}
                        onChange={(e) => setConfirmacaoSenha(e.target.value)}
                        disabled={loading || tokenInvalido}
                        invalid={confirmacaoSenha.length > 0 && !regras.senhasIguais}
                    />
                    <button
                        type="button"
                        className={styles.toggleSenha}
                        onClick={() => setMostrarConfirmacao((v) => !v)}
                        aria-label={mostrarConfirmacao ? 'Ocultar senha' : 'Mostrar senha'}
                        tabIndex={-1}
                    >
                        {mostrarConfirmacao ? '🙈' : '👁️'}
                    </button>
                </div>

                {/* Indicadores de requisitos da senha */}
                {novaSenha.length > 0 && (
                    <div className={styles.regrasContainer}>
                        <IndicadorRegra valida={regras.minCaracteres} texto="Mínimo 8 caracteres" />
                        <IndicadorRegra valida={regras.maiuscula} texto="Uma letra maiúscula" />
                        <IndicadorRegra valida={regras.minuscula} texto="Uma letra minúscula" />
                        <IndicadorRegra valida={regras.numero} texto="Um número" />
                        {confirmacaoSenha.length > 0 && (
                            <IndicadorRegra valida={regras.senhasIguais} texto="Senhas idênticas" />
                        )}
                    </div>
                )}

                <Button
                    type="submit"
                    style="filled"
                    action="primary"
                    fullWidth
                    label={loading ? 'Criando senha...' : 'Criar senha'}
                    isDisabled={isDisabled || tokenInvalido}
                />

            </form>

            {tokenInvalido && (
                <p className={styles.helperText}>
                    <a className={styles.forgotPasswordLink} href="/esqueci-senha">
                        Ir para &quot;Esqueci minha senha&quot;
                    </a>
                </p>
            )}

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

export default function PrimeiroAcessoPage() {
    return (
        <Suspense fallback={<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>Carregando...</div>}>
            <AlterarSenha />
        </Suspense>
    );
}
