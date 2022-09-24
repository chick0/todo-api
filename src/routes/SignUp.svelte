<script>
    import { push } from "svelte-spa-router";
    import { SIGN_UP } from "../url.js";
    import { is_login } from "../user.js";

    if (is_login()) {
        push("/todo");
    }

    let email = "";
    let password = "";
    let password_input = undefined;
    let submit = undefined;
</script>

<div class="section container">
    <h1>회원가입</h1>
    <div class="buttons">
        <a class="button" href="#/login">로그인</a>
        <a class="button" href="#/reset">비밀번호 재설정</a>
    </div>

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
            if (submit.classList.contains('spin')) {
                alert('이미 처리중입니다!');
            } else {
                submit.classList.add('spin');
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
                            submit.classList.remove('spin');
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        submit.classList.remove('spin');
                    });
            }
        }}">회원가입</button>
</div>
