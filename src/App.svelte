<script>
    import Router from "svelte-spa-router";
    import { onMount } from "svelte";
    import { routes } from "./router.js";

    function update_theme_color() {
        document
            .querySelector("meta[name=theme-color]")
            .setAttribute(
                "content",
                getComputedStyle(document.documentElement).getPropertyValue("--background").trim()
            );
    }

    onMount(() => {
        update_theme_color();
        window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => update_theme_color());
        window.onunhandledrejection = () => {
            alert("치명적인 오류가 발생해 재시작합니다.");
            location.reload();
        };
    });
</script>

<Router routes="{routes}" />
