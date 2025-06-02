import axios from "axios";

export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getUsers = async (offset, limit) => {
    try {
        const response = await api.get(`${window._env_.VITE_APP_API_URL}/users?offset=${offset}&limit=${limit}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};