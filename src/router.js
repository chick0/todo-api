// import { wrap } from "svelte-spa-router/wrap";

import About from "./routes/About.svelte";
import Login from "./routes/Login.svelte";
import SignUp from "./routes/SignUp.svelte";
import Todo from "./routes/Todo.svelte";

import NotFound from "./NotFound.svelte";

export const routes = {
    "/": About,

    "/login": Login,
    "/sign-up": SignUp,

    "/todo": Todo,

    "*": NotFound,
};
