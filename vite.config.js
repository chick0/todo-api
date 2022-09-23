import { execSync } from "child_process";
import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        svelte(),
        VitePWA({
            injectRegister: "inline",
            manifestFilename: "manifest.json",
            manifest: {
                name: "To-Do",
                short_name: "To-Do",
                description: "간단한 할 일 목록 웹 애플리케이션",
                lang: "ko",
                icons: [
                    {
                        src: "/icons/192.png",
                        sizes: "192x192",
                        type: "image/png",
                    },
                    {
                        src: "/icons/256.png",
                        sizes: "256x256",
                        type: "image/png",
                    },
                    {
                        src: "/icons/512.png",
                        sizes: "512x512",
                        type: "image/png",
                    },
                    {
                        src: "/icons/752.png",
                        sizes: "752x752",
                        type: "image/png",
                        purpose: "any maskable",
                    },
                ],
                start_url: "/#/pin",
                display: "standalone",
                background_color: "#141414",
                theme_color: "#FFCC4D",
            },
            includeAssets: [
                "Pretendard/*.woff2"
            ]
        }),
    ],
    define: {
        BUILD_DATE: JSON.stringify(Date.now()),
        GIT_HASH: JSON.stringify(execSync("git rev-parse --short HEAD").toString().trim()),
    },
});
