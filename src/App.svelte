<script>
    import Router from "svelte-spa-router";
    import { location, push } from "svelte-spa-router";
    import { onMount } from "svelte";
    import { titles } from "./title.js";
    import { routes } from "./router.js";
    import { is_login } from "./user.js";
    import "./navbar.css";

    /**
     * Update theme-color meta data
     */
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
            window.location.reload();
        };
    });

    let login_status = is_login();

    /**
     * Warning! For mobile device
     */
    let vertical_open = false;

    location.subscribe((path) => {
        let title = titles[path];

        if (title == null) {
            console.warn(`'${path}'에 제목이 설정되지 않았습니다.`);
            title = "To-Do";
        }

        document.title = title;
        login_status = is_login();
        vertical_open = false;
    });
</script>

<nav class="container">
    <div class="navbar">
        <ul class="{vertical_open == true ? 'nav-opened' : 'nav-closed'}">
            <li on:click="{() => push('/')}"><b>To-Do</b></li>
            <li
                class="trigger"
                on:click="{() => {
                    vertical_open = !vertical_open;
                }}">
                {vertical_open == true ? "-" : "+"}
            </li>
            {#if login_status == false}
                <li on:click="{() => push('/login')}">로그인</li>
                <li on:click="{() => push('/sign-up')}">회원가입</li>
            {:else}
                <li on:click="{() => push('/todo')}">할 일</li>
                <li on:click="{() => push('/user')}">계정 정보</li>
                <li on:click="{() => push('/logout')}">로그아웃</li>
            {/if}
        </ul>
    </div>
</nav>

<Router routes="{routes}" />
