import { Buffer } from "buffer/";

const TOKEN_KEY = "to-do:token";

/**
 * Get Auth token from sessionStorage
 *
 * @returns {string|null} auth token
 */
export function get_token() {
    return sessionStorage.getItem(TOKEN_KEY);
}

/**
 * Set Auth token in sessionStorage
 *
 * @param {string} token auth token
 */
export function set_token(token) {
    sessionStorage.setItem(TOKEN_KEY, token);
}

/**
 * Get payload from auth token
 *
 * @returns {Object} token payload
 */
export function get_payload() {
    const token = get_token();
    if (token == null) {
        return null;
    }

    const [head, payload, sign] = token.split(".");

    if (payload == null) {
        return null;
    }

    return JSON.parse(Buffer.from(payload, "base64").toString());
}

/**
 * Check user is logined
 */
export function is_login() {
    const payload = get_payload();

    return payload != null;
}
