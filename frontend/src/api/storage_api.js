import axios from "axios";

let apiUrl = import.meta.env.VITE_API_URL;
if (apiUrl === undefined) {
    apiUrl = 'http://scan-doc-back:8083/'
}


export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getToken = async () => {
    try {
        const response = await api.get(`${apiUrl}/storage?id=${localStorage.getItem('id')}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}
export const setToken = async (token) => {
    try {
        const response = await api.post(`${apiUrl}/storage?token=${token}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}


export const deleteToken = async () => {
    try {
        const response = await api.delete(`${apiUrl}/storage?id=${localStorage.getItem('id')}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}

