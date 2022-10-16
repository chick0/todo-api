import { wrap } from "svelte-spa-router/wrap";

export const routes = {
    "/": wrap({ asyncComponent: () => import("routes/About.svelte") }),
    "/login": wrap({ asyncComponent: () => import("routes/Login.svelte") }),
    "/logout": wrap({ asyncComponent: () => import("routes/Logout.svelte") }),

    "/notice": wrap({ asyncComponent: () => import("routes/Notice.svelte") }),

    "/sign-up": wrap({ asyncComponent: () => import("routes/SignUp.svelte") }),
    "/verify": wrap({ asyncComponent: () => import("routes/Verify.svelte") }),

    "/retry": wrap({ asyncComponent: () => import("routes/Retry.svelte") }),
    "/reset": wrap({ asyncComponent: () => import("routes/Reset.svelte") }),

    "/todo": wrap({ asyncComponent: () => import("routes/Todo.svelte") }),
    "/todo/clean-up": wrap({ asyncComponent: () => import("routes/CleanUp.svelte") }),

    "/user": wrap({ asyncComponent: () => import("routes/User.svelte") }),
    "/user/quit": wrap({ asyncComponent: () => import("routes/Quit.svelte") }),

    "/pin": wrap({ asyncComponent: () => import("routes/Pin.svelte") }),
    "/pin/create": wrap({ asyncComponent: () => import("routes/PinCreate.svelte") }),

    "/version": wrap({ asyncComponent: () => import("routes/Version.svelte") }),
    "*": wrap({ asyncComponent: () => import("src/NotFound.svelte") }),
};
