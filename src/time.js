/**
 * Convert timestamp to locale datesting
 *
 * @param {number|null} timestamp not milliseconds timestamp
 *
 * @returns {string} locale date
 */
export function to_datestring(timestamp) {
    if (timestamp == null) {
        return "?";
    }
    return new Date(timestamp * 1000).toLocaleDateString();
}

/**
 * Convert timestamp to locale timestring
 *
 * @param {number|null} timestamp not milliseconds timestamp
 *
 * @returns {string} locale time
 */
export function to_timestring(timestamp) {
    if (timestamp == null) {
        return "?";
    }
    return new Date(timestamp * 1000).toLocaleTimeString();
}
