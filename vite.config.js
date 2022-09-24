import { execSync } from "child_process";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [svelte()],
    define: {
        BUILD_DATE: JSON.stringify(Date.now()),
        COMMIT_HASH: JSON.stringify(execSync("git rev-parse --short HEAD").toString().trim()),
    },
});
