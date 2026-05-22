type Handler = (active: boolean) => void;

let handler: Handler | null = null;
let activeRequests = 0;

export const loadingEmitter = {
    register: (fn: Handler) => { handler = fn; },
    show: () => {
        activeRequests++;
        handler?.(true);
    },
    hide: () => {
        activeRequests = Math.max(0, activeRequests - 1);
        if (activeRequests === 0) handler?.(false);
    },
};
