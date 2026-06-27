export type TurnoDisplay = "Manhã" | "Tarde" | "Noite";
export type TurnoApi = "Matutino" | "Vespertino" | "Noturno";

const API_TO_DISPLAY: Record<TurnoApi, TurnoDisplay> = {
    Matutino: "Manhã",
    Vespertino: "Tarde",
    Noturno: "Noite",
};

const DISPLAY_TO_API: Record<TurnoDisplay, TurnoApi> = {
    Manhã: "Matutino",
    Tarde: "Vespertino",
    Noite: "Noturno",
};

export const TURNO_DISPLAY_OPTIONS: TurnoDisplay[] = ["Manhã", "Tarde", "Noite"];

export function turnoApiToDisplay(api: string): string {
    return API_TO_DISPLAY[api as TurnoApi] ?? api;
}

export function turnoDisplayToApi(display: string): string {
    return DISPLAY_TO_API[display as TurnoDisplay] ?? display;
}

export const SEMESTRE_REGEX = /^\d{4}\.[12]$/;
