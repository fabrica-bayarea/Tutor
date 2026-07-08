/**
 * Prefixo de path para uso em window.location (onde o Next.js não
 * adiciona o basePath automaticamente).
 *
 * Para router.push / <Link href> NÃO use este prefixo — o Next.js já
 * trata o basePath nesses casos.
 */
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || '/tutor';

/**
 * Redireciona via window.location respeitando o basePath.
 */
export function hardRedirect(path: string) {
  window.location.href = `${BASE_PATH}${path}`;
}

/**
 * Substitui a URL atual (sem adicionar ao histórico) respeitando o basePath.
 */
export function hardReplace(path: string) {
  window.location.replace(`${BASE_PATH}${path}`);
}
