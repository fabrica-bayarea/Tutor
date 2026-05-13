export const Role = {
    ADMIN:     'ADMIN',
    PROFESSOR: 'PROFESSOR',
    ALUNO:     'ALUNO',
} as const;

export type RoleType = typeof Role[keyof typeof Role];

export const Status = {
    ATIVO:   'ATIVO',
    INATIVO: 'INATIVO',
} as const;

export type StatusType = typeof Status[keyof typeof Status];

export function homeForRole(role: string | null | undefined): string {
    if (role === Role.ADMIN)     return '/admin';
    if (role === Role.PROFESSOR) return '/professor';
    return '/chat';
}
