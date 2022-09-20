import { wrap } from "svelte-spa-router/wrap";

import About from "./routes/About.svelte";
import NotFound from "./NotFound.svelte";

export const routes = {
    "/": About,

    "/login": wrap({
        asyncComponent: () => import("./routes/Login.svelte"),
    }),
    "/sign-up": wrap({
        asyncComponent: () => import("./routes/SignUp.svelte"),
    }),

    "*": NotFound
};
