import axios from "axios";


let apiUrl = window.VITE_API_URL;
if (apiUrl === undefined) {
    apiUrl = 'http://triage-tpak.m15.dzm/api'
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