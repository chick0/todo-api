<script>
    import { push } from "svelte-spa-router";
    import { SIGN_UP } from "src/url.js";
    import { is_login } from "src/user.js";

    let is_loading = true;

    let email = "";
    let password = "";
    let password_input = undefined;
    let submit = undefined;

    if (is_login()) {
        push("/todo");
    } else {
        is_loading = false;
    }
</script>

<div class="container">
    <h1>회원가입</h1>

    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        <div class="field">
            <label for="email">이메일</label>
            <input
                type="email"
                id="email"
                bind:value="{email}"
                placeholder="Email"
                required
                on:keydown="{(e) => {
                    if (e.key == 'Enter') {
                        password_input.focus();
                    }
                }}" />
        </div>

        <div class="field">
            <label for="password">비밀번호</label>
            <input
                type="password"
                id="password"
                placeholder="Password"
                required
                minlength="8"
                bind:this="{password_input}"
                bind:value="{password}"
                on:keydown="{(e) => {
                    if (e.key == 'Enter') {
                        password_input.blur();
                        submit.click();
                    }
                }}" />
        </div>

        <button
            class="button max"
            type="submit"
            bind:this="{submit}"
            on:click="{() => {
                is_loading = true;
                fetch(SIGN_UP, {
                    method: 'POST',
                    body: JSON.stringify({
                        email: email,
                        password: password,
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        alert(json.message);

                        if (json.status === true) {
                            push('/login');
                        } else {
                            is_loading = false;
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">회원가입</button>
    {/if}
</div>
