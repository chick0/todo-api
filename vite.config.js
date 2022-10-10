import path from "path";
import { execSync } from "child_process";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
    define: {
        TAG: JSON.stringify(execSync("git describe --tags").toString().trim()),
        BUILD_DATE: JSON.stringify(Date.now()),
    },
    plugins: [svelte()],
    resolve: {
        alias: {
            src: path.resolve(__dirname) + "/src",
            routes: path.resolve(__dirname) + "/src/routes",
            styles: path.resolve(__dirname) + "/src/styles",
        },
    },
});
