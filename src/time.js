/**
 * Convert timestamp to locale datesting
 *
 * @param {number|null} timestamp not milliseconds timestamp
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
 * @returns {string} locale time
 */
export function to_timestring(timestamp) {
    if (timestamp == null) {
        return "?";
    }
    return new Date(timestamp * 1000).toLocaleTimeString();
}

/**
 * Convert timestamp to string
 *
 * @param {number} timestamp timestamp from python api
 * @returns {string} `date` or `time` string
 */
export function to_string(timestamp) {
    let now = Date.now() / 1000;
    if (now - timestamp > 3600) {
        return to_datestring(timestamp);
    } else {
        return to_timestring(timestamp);
    }
}
