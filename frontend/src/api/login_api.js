import {Buffer} from "buffer";
import axios from "axios";


let apiUrl = import.meta.env.VITE_LOGIN_API_URL;
if (apiUrl === undefined) {
    console.error("No login url were found")
}

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
