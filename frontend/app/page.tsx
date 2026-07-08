import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';

/**
 * Página raiz — redireciona para /login (ou para a home do role se autenticado).
 */
export const dynamic = 'force-dynamic';

export default async function RootPage() {
  const cookieStore = await cookies();
  const token = cookieStore.get('token')?.value;

  if (!token) {
    redirect('/login');
  }

  // Se tem token, redireciona pra login mesmo (o middleware cuida do role)
  redirect('/login');
}
