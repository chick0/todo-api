<script>
    import Router from "svelte-spa-router";
    import { location, push } from "svelte-spa-router";
    import { onMount } from "svelte";
    import { titles } from "src/title.js";
    import { routes } from "src/router.js";
    import { is_login } from "src/user.js";
    import "src/navbar.css";
    import "src/D2Coding.css";

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

        window.addEventListener("keydown", (e) => {
            if (e.target == document.body && e.shiftKey && e.key != "Shift") {
                if (e.key == "@") {
                    if (is_login()) {
                        if (confirm("로그아웃 하시겠습니까?")) {
                            push("/logout");
                        }
                    } else {
                        push("/login");
                    }
                } else if (e.key == "#") {
                    if (where_am_i != "/todo") {
                        push("/todo");
                    } else {
                        /**
                         * @type {HTMLElement} New todo input area open button
                         */
                        let open = document.querySelector("p.clickable.open");
                        open?.click();

                        setTimeout(() => {
                            /**
                             * @type {HTMLElement} New todo input textarea
                             */
                            let textarea = document.querySelector("div.todo.new > textarea");

                            if (textarea != undefined) {
                                window.scrollTo(0, textarea.offsetTop - 20);
                                textarea.focus();
                            }
                        }, 150);
                    }
                }
            }
        });
    });

    let login_status = is_login();

    /**
     * Warning! For mobile device
     */
    let vertical_open = false;

    /**
     * SPA Router path
     */
    let where_am_i = "";

    location.subscribe((path) => {
        where_am_i = path;
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
            <li
                class="head"
                on:click="{() => push('/')}"
                on:dblclick="{() => {
                    window.getSelection()?.removeAllRanges();
                    push('/version');
                }}">
                <b>To-Do</b>
            </li>
            <li class="head trigger" on:click="{() => (vertical_open = !vertical_open)}">
                <span></span>
                <span></span>
                <span></span>
            </li>
            {#if login_status == false}
                <li on:click="{() => push('/login')}">로그인</li>
                <li on:click="{() => push('/sign-up')}">회원가입</li>
            {:else}
                <li on:click="{() => push('/todo')}">할 일</li>
                <li on:click="{() => push('/user')}">계정 정보</li>
                <li on:click="{() => {
                    if (confirm("로그아웃 하시겠습니까?")) {
                        push("/logout");
                    }
                }}">로그아웃</li>
            {/if}
        </ul>
    </div>
</nav>

<Router routes="{routes}" />
