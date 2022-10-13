<script>
    import { push } from "svelte-spa-router";
    import { LOGIN } from "src/url.js";
    import { is_login, set_token } from "src/user.js";
    import { get_pin_token } from "src/pin.js";

    let is_loading = true;

    let email = "";
    let password = "";
    let password_input = undefined;
    let submit = undefined;

    if (is_login()) {
        push("/todo");
    } else {
        if (get_pin_token() == null) {
            is_loading = false;
        } else {
            if (!location.hash.endsWith("?force")) {
                push("/pin");
            } else {
                is_loading = false;
            }
        }
    }
</script>

<div class="container">
    <h1>로그인</h1>

    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        <div class="buttons">
            <a class="button" href="#/reset">비밀번호 재설정</a>
        </div>

        <div class="field">
            <label for="email">이메일</label>
            <input
                type="email"
                id="email"
                placeholder="Email"
                required
                bind:value="{email}"
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

                fetch(LOGIN, {
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
                        if (json.status === true) {
                            set_token(json.token);

                            let push_to = '/todo';

                            if (window.innerWidth <= 700) {
                                if (confirm('PIN 로그인을 설정하시겠습니까?')) {
                                    push_to = '/pin/create';
                                }
                            }

                            push(push_to);
                        } else {
                            alert(json.message);
                            is_loading = false;
                            password = '';

                            if (json.email_verify_required) {
                                if (confirm('이메일 인증을 다시 시도하시겠습니까?')) {
                                    push('/retry');
                                }
                            }
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">로그인</button>
    {/if}
</div>
