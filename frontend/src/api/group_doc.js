import axios from "axios";


let apiUrl = import.meta.env.VITE_API_URL;
if (apiUrl === undefined) {
    apiUrl = 'http://localhost:8000/api'
}


export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});


export const getGroupDoc = async () => {
    try {
        const response = await api.get(`${apiUrl}/group_doc`);
        return response.data;
    } catch (error) {
        console.error("Error getting group doc", error);
        throw error;
    }
}