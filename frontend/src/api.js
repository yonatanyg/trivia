/*import axios from "axios";

const API_URL = "http://localhost:8000"; // FastAPI backend

export const api = axios.create({
  baseURL: API_URL,
});
*/

import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL; // from .env

export const api = axios.create({
  baseURL: API_URL,
});
