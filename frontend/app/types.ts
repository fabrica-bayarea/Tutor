export interface InterfaceUsuario {
    id: string;
    matricula: string;
    nome: string;
    email: string;
    role: string;
    token?: string;
}

export interface InterfaceArquivo {
    id: string;
    professor_id: string;
    titulo: string;
    data_upload: Date | string;
}

export interface GooglePayload {
  email: string;
  name: string;
  sub: string; 
}

export interface InterfaceChat {
    id: string;
    aluno_id: string;
    nome: string;
    data_ultima_interacao?: Date;
}

export interface InterfaceMensagem {
    id: string;
    chat_id: string;
    sessao_id?: string;
    sender_id: string;
    conteudo: string;
    data_envio: Date;
}

export interface InterfaceTurma {
    id: string;
    codigo: string;
    semestre: string;
    turno: string;
}

export interface InterfaceMateria {
    id: string;
    codigo: string;
    nome: string;
}

export interface InterfaceAlunoTurma {
    aluno_id: string;
    turma_id: string;
}

export interface InterfaceTurmaMateria {
    turma_id: string;
    materia_id: string;
}

export interface InterfaceProfessorTurmaMateria {
    professor_id: string;
    turma_id: string;
    materia_id: string;
}

export interface InterfaceArquivoTurmaMateria {
    arquivo_id: string;
    turma_id: string;
    materia_id: string;
}

export interface Sessao {
    id: string;
    dono_id: string;
    inicio: Date;
    fim: Date;
}