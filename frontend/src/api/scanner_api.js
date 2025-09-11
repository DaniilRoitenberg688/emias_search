import axios from "axios";

const apiUrl = 'http://localhost:3000'
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