import type { ToastType } from '@/contexts/ToastContext';

type Handler = (message: string, type: ToastType) => void;

let handler: Handler | null = null;

export const toastEmitter = {
    register: (fn: Handler) => { handler = fn; },
    emit: (message: string, type: ToastType) => { handler?.(message, type); },
};
