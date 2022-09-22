import { wrap } from "svelte-spa-router/wrap";

import About from "./routes/About.svelte";
import Login from "./routes/Login.svelte";
import Logout from "./routes/Logout.svelte";
import NotFound from "./NotFound.svelte";

export const routes = {
    "/": About,
    "/login": Login,
    "/logout": Logout,
    "/sign-up": wrap({ asyncComponent: () => import("./routes/SignUp.svelte") }),
    "/verify": wrap({ asyncComponent: () => import("./routes/Verify.svelte") }),
    "/retry": wrap({ asyncComponent: () => import("./routes/Retry.svelte") }),

    "/todo": wrap({ asyncComponent: () => import("./routes/Todo.svelte") }),

    "/user": wrap({ asyncComponent: () => import("./routes/User.svelte") }),
    "/user/quit": wrap({ asyncComponent: () => import("./routes/Quit.svelte") }),

    "/pin": wrap({ asyncComponent: () => import("./routes/Pin.svelte") }),
    "/pin/create": wrap({ asyncComponent: () => import("./routes/PinCreate.svelte") }),

    "*": NotFound,
};
