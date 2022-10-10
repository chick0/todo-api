import "styles/app.css";
import "styles/navbar.css";
import "styles/scrollbar.css";
import "styles/button.css";
import "styles/list.css";
import "styles/table.css";
import "styles/label.css";
import "styles/input.css";

import App from "src/App.svelte";

const app = new App({
    target: document.getElementById("app"),
});

export default app;
