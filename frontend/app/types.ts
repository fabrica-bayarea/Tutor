export interface InterfaceAluno {
    id: string;
    matricula: string;
    nome: string;
    email: string;
    cpf: string;
    data_nascimento?: Date;
}

export interface InterfaceProfessor {
    id: string;
    matricula: string;
    nome: string;
    email: string;
    cpf: string;
    data_nascimento?: Date;
}

export interface InterfaceArquivo {
    id: string;
    professor_id: string;
    titulo: string;
    data_upload: Date | string;
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
