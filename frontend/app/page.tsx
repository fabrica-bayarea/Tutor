/**
 * Página raiz — o middleware redireciona para /login ou home do role.
 * Forçada como dinâmica para garantir que o middleware execute server-side.
 */
export const dynamic = 'force-dynamic';

export default function RootPage() {
  return null;
}
