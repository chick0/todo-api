<script>
    import Router from "svelte-spa-router";
    import { onMount } from "svelte";
    import { routes } from "./router.js";

    let hash = GIT_HASH;
    let date = new Date(BUILD_DATE);

    function update_theme_color() {
        document
            .querySelector("meta[name=theme-color]")
            .setAttribute("content", getComputedStyle(document.documentElement).getPropertyValue("--background"));
    }

    onMount(() => {
        update_theme_color();
        window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => update_theme_color());
    });
</script>

<Router routes="{routes}" />

<div class="section container">
    <p class="build">{hash} / {date.toLocaleString()}</p>
</div>

<style>
    .build {
        font-weight: 200;
        font-size: 16px;
        color: #949494;
    }
</style>
