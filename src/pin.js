const TOKEN_KEY = "to-do:pin:token";

/**
 * Set PIN token in localStorage
 *
 * @param {string} token pin token
 */
export function set_pin_token(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Get PIN token in localStorage
 *
 * @returns {string|null} token pin token
 */
export function get_pin_token(token) {
    return localStorage.getItem(TOKEN_KEY);
}

/**
 * Clear PIN token in localStorage
 */
export function clear_pin_token() {
    localStorage.removeItem(TOKEN_KEY);
}
