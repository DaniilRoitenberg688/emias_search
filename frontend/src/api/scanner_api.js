import axios from "axios";

const apiUrl = 'http://localhost:8000'
// const apiUrl = '/api'

export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getScanners = async () => {
    try {
        const response = await api.get(`${apiUrl}/scan?host=${window.location.hostname}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}

export const makeScan = async (mDocID, scanner) => {
    try {
        const response = await api.post(`${apiUrl}/scan?mdoc_id=${mDocID}&host=${window.location.hostname}`, scanner);
        return [response.data, response.status];
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}