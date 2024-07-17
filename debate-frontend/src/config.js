import axios from 'axios';

const config = {
    backendUrl: process.env.REACT_APP_BACKEND_URL || 'https://127.0.0.1:5000',
};

let axiosInstance = axios.create({
        baseURL: config.backendUrl,
        withCredentials: true,
    });

export { config, axiosInstance };