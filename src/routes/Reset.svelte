<script>
    import { push } from "svelte-spa-router";
    import { RESET_STEP_1, RESET_STEP_2 } from "src/url.js";
    import { is_login } from "src/user.js";

    let is_loading = true;
    let step = 1;

    // step1
    let email = "";
    let email_input = undefined;
    let submit1 = undefined;

    // step2
    let token = "";
    let password = "";
    let password_input = undefined;
    let submit2 = undefined;

    if (is_login()) {
        push("/todo");
    } else {
        if (location.hash.endsWith("?step2")) {
            token = sessionStorage.getItem("to-do:reset_verify_token");

            if (token == null) {
                alert("인증 토큰이 없습니다!");
                step = 1;
                is_loading = false;
            } else {
                step = 2;
                is_loading = false;
            }
        } else {
            step = 1;
            is_loading = false;
        }
    }
</script>

<div class="section container">
    <h1>비밀번호 재설정</h1>
    {#if is_loading == true}
        <div class="spinner"></div>
    {:else if step == 1}
        <p>5분마다 한 번씩 시도할 수 있습니다.</p>

        <div class="field">
            <label for="email-2">이메일</label>
            <input
                type="email"
                id="email-2"
                placeholder="Email"
                required
                bind:this="{email_input}"
                bind:value="{email}"
                on:keydown="{(e) => {
                    if (e.key == 'Enter') {
                        email_input.blur();
                        submit1.click();
                    }
                }}" />
        </div>

        <button
            class="button max"
            type="submit"
            bind:this="{submit1}"
            on:click="{() => {
                is_loading = true;
                fetch(RESET_STEP_1, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                    }),
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        alert(json.message);

                        if (json.status == true) {
                            push('/');
                        } else {
                            is_loading = false;
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">다음</button>
    {:else if step == 2}
        <p>새로운 비밀번호를 입력해주세요.</p>

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
                        submit2.click();
                    }
                }}" />
        </div>

        <button
            class="button max"
            type="submit"
            bind:this="{submit2}"
            on:click="{() => {
                is_loading = true;
                fetch(RESET_STEP_2, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-reset': token,
                    },
                    body: JSON.stringify({
                        password: password,
                    }),
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        alert(json.message);

                        if (json.status == true) {
                            push('/login');
                        } else {
                            is_loading = false;
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">다음</button>
    {/if}
</div>
