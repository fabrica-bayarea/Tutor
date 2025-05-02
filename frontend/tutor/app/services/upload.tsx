import axios from "axios";

const uploadAPI = axios.create({baseURL: 'http://127.0.0.1:5000/arquivos'});

async function postUpload(files: File[]) {
    try {
        const response = await uploadAPI.post('/upload', files, {headers: {"Content-Type": "multipart/form-data"}});
        return response.data;
    } catch (error) {
        console.error("Erro ao processar o arquivo:", error);
        throw error;
    }
}

export {postUpload};  