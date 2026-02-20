import axios from "axios";

let apiUrl = import.meta.env.VITE_SCANNER_API_URL;
if (apiUrl === undefined) {
    apiUrl = 'http://localhost:3000'
    console.error("No scanner url were found")
}
// const apiUrl = '/api'

export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getScanners = async () => {
    try {
        const response = await api.get(`${apiUrl}/scanners`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}

export const makeScan = async (mDocID, scanner, groupDocId) => {
    try {
        const response = await api.post(`${apiUrl}/scan?mdoc_id=${mDocID}&group_doc_id=${groupDocId}`, scanner);
        return response.status;
    } catch (error) {
        console.error("Error fetching profile:", error);
        return error.status
    }
}

export const getDocs = async (mDocID, groupDocId) => {
    try {
        const response = await api.get(`${apiUrl}/documents?mdoc_id=${mDocID}&group_doc_id=${groupDocId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching docs for doc:", error);
        return []
    }
}

export const deleteDocApi = async (mDocID, groupDocId, filename) => {
    try {
        const response = await api.delete(`${apiUrl}/documents?mdoc_id=${mDocID}&group_doc_id=${groupDocId}&filename=${filename}`);
        return response.status;
    } catch (error) {
        console.error("Error fetching docs for doc:", error);
        return error.status
    }
}

export const sendDocs = async (mDocID, groupDocId) => {
    try {
        const response = await api.post(`${apiUrl}/documents/send?mdoc_id=${mDocID}&group_doc_id=${groupDocId}`);
        return response.status;
    } catch (error) {
        console.error("Error fetching docs for doc:", error);
        return error.status
    }
}
