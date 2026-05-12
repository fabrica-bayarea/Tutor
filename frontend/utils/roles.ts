export const Role = {
    ADMIN:     'ADMIN',
    PROFESSOR: 'PROFESSOR',
    ALUNO:     'ALUNO',
} as const;

export type RoleType = typeof Role[keyof typeof Role];

export function homeForRole(role: string | null | undefined): string {
    if (role === Role.ADMIN)     return '/admin';
    if (role === Role.PROFESSOR) return '/professor';
    return '/chat';
}
