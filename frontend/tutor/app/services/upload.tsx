import axios from "axios";

const uploadAPI = axios.create({baseURL: 'http://127.0.0.1:5000/arquivos'});

async function postUpload(files: File[], matricula_professor: string, vinculos: any[]) {
    try {
        const formData = new FormData();
        
        files.forEach((file, index) => {
            formData.append('arquivos', file);
        });

        formData.append('matricula_professor', matricula_professor);

        formData.append('vinculos', JSON.stringify(vinculos));

        const response = await uploadAPI.post('/upload', formData, {
            headers: {"Content-Type": "multipart/form-data"}
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao processar o arquivo:", error);
        throw error;
    }
}

export {postUpload};