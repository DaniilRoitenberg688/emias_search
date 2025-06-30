import {Buffer} from "buffer";
import axios from "axios";

const apiUrl = 'http://j-auth-tpak.m15.dzm/api/v2/login'

export const api = axios.create({

});



export const loginRequest = async (token) => {
    try {
        // const response = await fetch(apiUrl, {
        //     method: 'POST',
        //     headers: {'Authorization': `Basic ${line}`},
        // });
        const response = await axios.post(`${apiUrl}`, {},
            {headers: {'Authorization': `Basic ${token}`}})
        return [response.status, response.data];
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};
