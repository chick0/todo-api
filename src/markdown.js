import { marked } from "marked";
import DOMPurify from "dompurify";
import { remove_label } from "src/label.js";
import "src/markdown.css";

DOMPurify.addHook("afterSanitizeAttributes", function (node) {
    let tag = node.tagName.toLowerCase();

    if (tag == "a" && "target" in node) {
        // Set target to `_blank` when device type is desktop
        if (window.innerWidth > 700) {
            node.setAttribute("target", "_blank");
        }
    }
});

/**
 * marked.js markdown renderer
 *
 * @type {Object}
 */
const renderer = new marked.Renderer();

/**
 * @param {string} head
 * @param {string} body
 */
renderer.table = (head, body) => {
    return [
        '<div class="table-wrapped">',
        "<table>",
        "<thead>" + head + "</thead>",
        "<tbody>" + body + "</tbody>",
        "</table>",
        "</div>",
    ].join("");
};

/**
 * @param {string} text
 * @param {number} level
 */
renderer.heading = (text, level) => {
    return `<h${level} class="markdown">${text}</h${level}>`;
};

renderer.hr = () => {
    return "<hr class='markdown'>";
};

/**
 * @param {string} text
 * @param {boolean} task
 * @param {boolean} checked
 */
renderer.listitem = (text, task, checked) => {
    if (task == true) {
        text = text.replace(/<input [a-z=" ]*"> /g, "");
        text = `<i class="todo-task ${checked == true ? "checked" : "not-checked"}"></i> ${text}`;
    }

    return `<li>${text}</li>`;
};

/**
 * @param {string} href
 * @param {string|null} title
 * @param {string} text
 */
renderer.link = (href, title, text) => {
    /**
     * @returns {string} Get title attribute
     */
    function get_title() {
        return title == null ? "" : `title="${title}"`;
    }

    return `<a rel="noreferrer" href="${href}" ${get_title()}>${text}</a>`;
};

marked.setOptions({
    breaks: true,
    headerIds: false,
    renderer: renderer,
});

/**
 * Render markdown and purify
 *
 * @param {string} markdown MarkDown string
 * @returns {string} HTML String
 */
export function get_html(markdown) {
    let lable_removed = remove_label(markdown);
    return DOMPurify.sanitize(marked.parse(lable_removed), {});
}
