import axios from "axios";


let apiUrl = import.meta.env.VITE_API_URL;
if (apiUrl === undefined) {
    apiUrl = 'http://scan-doc-back:8083/'
    console.error("Cannot access group_doc, because url was not provided")
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