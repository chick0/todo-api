const BASE_URL = import.meta.env.PROD === true ? "/api" : "http://localhost:18282/api";

export const LOGIN = BASE_URL + "/login";
export const SIGN_UP = BASE_URL + "/sign-up";
