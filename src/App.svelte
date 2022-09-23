<script>
    import Router from "svelte-spa-router";
    import { routes } from "./router.js";

    let hash = GIT_HASH;
    let date = new Date(BUILD_DATE);
</script>

<Router routes="{routes}" />

<div class="section container">
    <p class="build">{hash} {date.toLocaleString()}</p>
</div>

<style>
    .build {
        font-size: 12px;
        color: #949494;
    }
</style>
