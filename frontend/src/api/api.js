import axios from "axios";

const apiUrl = 'http://localhost:8000/api'
// const apiUrl = '/api'

export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getUsers = async (offset, limit) => {
    try {
        const response = await api.get(`${apiUrl}/users?offset=${offset}&limit=${limit}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};

export const getSearchUsers = async (line, offset, limit) => {
    try {
        const response = await api.get(`${apiUrl}/users/search?offset=${offset}&limit=${limit}&search_line=${line}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}