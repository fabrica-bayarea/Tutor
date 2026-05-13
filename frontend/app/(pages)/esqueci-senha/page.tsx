'use client';

import { useState } from 'react';
import Link from 'next/link';
import { CheckCircle } from 'lucide-react';
import TutorLogoIcon from '@/app/components/TutorLogoIcon';
import Input from '@/app/components/Input/Input';
import Button from '@/app/components/Button/Button';
import { solicitarRecuperacaoSenha } from '@/app/services/service_auth';
import styles from '../alterar-senha/alterarSenha.module.css';
import localStyles from './page.module.css';

export default function EsqueciSenhaPage() {
    const [email, setEmail] = useState('');
    const [enviado, setEnviado] = useState(false);
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!email.trim() || loading) return;
        setLoading(true);
        await solicitarRecuperacaoSenha(email.trim());
        setEnviado(true);
        setLoading(false);
    }

    if (enviado) {
        return (
            <div className={styles.contentContainer}>
                <div className={styles.brandHeader}>
                    <TutorLogoIcon size={28} color="#f97316" />
                    <span className={styles.brandName}>Tutor</span>
                </div>

                <div className={localStyles.checkIcon}>
                    <CheckCircle size={48} color="#0d9488" strokeWidth={1.5} />
                </div>

                <h2 className={styles.welcomeTitle}>E-mail enviado!</h2>
                <p className={styles.welcomeSubtitle}>
                    Se o e-mail informado estiver cadastrado, você receberá um link em instantes.
                    Verifique também a caixa de spam.
                </p>

                <Link href="/login" className={localStyles.backLink}>
                    ← Voltar para o login
                </Link>
            </div>
        );
    }

    return (
        <div className={styles.contentContainer}>
            <div className={styles.brandHeader}>
                <TutorLogoIcon size={28} color="#f97316" />
                <span className={styles.brandName}>Tutor</span>
            </div>

            <h2 className={styles.welcomeTitle}>Recuperar senha</h2>
            <p className={styles.welcomeSubtitle}>
                Informe seu e-mail cadastrado. Você receberá um link para redefinir sua senha.
            </p>

            <form className={styles.formContainer} onSubmit={handleSubmit}>
                <Input
                    id="email"
                    name="email"
                    label="E-mail institucional"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={loading}
                />

                <Button
                    type="submit"
                    style="filled"
                    action="primary"
                    fullWidth
                    label={loading ? 'Enviando...' : 'Enviar link de recuperação'}
                    isDisabled={!email.trim() || loading}
                />
            </form>

            <Link href="/login" className={localStyles.backLink}>
                ← Voltar para o login
            </Link>
        </div>
    );
}
