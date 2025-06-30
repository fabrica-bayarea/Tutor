import api from "./api";

const arquivos_url = "arquivos";

async function postUpload(files: File[], matricula_professor: string, vinculos: any[]) {
    try {
        const formData = new FormData();
        
        files.forEach((file, index) => {
            formData.append('arquivos', file);
        });

        formData.append('matricula_professor', matricula_professor);

        formData.append('vinculos', JSON.stringify(vinculos));

        const response = await api.post(`/${arquivos_url}/upload`, formData, {
            headers: {"Content-Type": "multipart/form-data"}
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao processar o arquivo:", error);
        throw error;
    }
}

async function getArquivos(id_professor){
    pass
}



export {postUpload, getArquivos};