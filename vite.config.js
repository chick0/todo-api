import { execSync } from "child_process";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [svelte()],
    define: {
        TAG: JSON.stringify(execSync("git describe --tags").toString().trim()),
        BUILD_DATE: JSON.stringify(Date.now()),
    },
});
