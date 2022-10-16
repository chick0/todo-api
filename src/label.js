/**
 * Label Level Calculation
 *
 * @param {string} label Unparsed label
 * @returns {number} level
 */
function calc_level(label) {
    if (label.startsWith("@@@")) {
        return 3;
    } else if (label.startsWith("@@")) {
        return 2;
    } else {
        return 1;
    }
}

/**
 * Check 'text' has a label
 *
 * @param {string} text
 * @returns {boolean}
 */
export function has_label(text) {
    return text.startsWith("@");
}

/**
 * Simple label
 * @typedef {Object} Label
 * @property {number} level
 * @property {string} text
 */

/**
 * Parse labels from 'text'
 *
 * @param {string} text
 * @returns {Label[]} labels
 */
export function parse_labels(text) {
    let labels = [];

    if (text.startsWith("@")) {
        text.split("\n")[0]
            .split(",")
            .forEach((label) => {
                label = label.trim();

                let level = calc_level(label);
                let text = label.slice(level, label.length).trim();

                if (level > 3) {
                    level = 3;
                }

                if (level >= 1 && text.length != 0) {
                    labels.push({
                        level,
                        text,
                    });
                }
            });
    }

    labels.sort((a, b) => b.level - a.level);
    return labels;
}

/**
 * Remove label from text
 *
 * @param {string} text
 * @returns {string} text
 */
export function remove_label(text) {
    if (!has_label(text)) {
        return text;
    }

    return text.split("\n").slice(1).join("\n");
}
