import axios from "axios";


let apiUrl = window.VITE_API_URL;
if (apiUrl === undefined) {
    apiUrl = 'http://triage-tpak.m15.dzm/api'
    console.error("Cannot access main api, because url was not provided")
}


export const api = axios.create({
    headers: {
        "Content-Type": "application/json",
    },
});

export const getUsers = async (offset, limit, usersType) => {
    try {
        const response = await api.get(`${apiUrl}/users?offset=${offset}&limit=${limit}&type_of_users=${usersType}&dept_id=${localStorage.getItem('deptId')}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};

export const getSearchUsers = async (line, offset, limit, usersType) => {
    try {
        const response = await api.get(`${apiUrl}/users/search?offset=${offset}&limit=${limit}&search_line=${line}&type_of_users=${usersType}&dept_id=${localStorage.getItem('deptId')}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
}