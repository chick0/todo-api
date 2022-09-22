<script>
    import { push } from "svelte-spa-router";
    import { LOGIN } from "../url.js";
    import { is_login, set_token } from "../user.js";

    if (is_login()) {
        push("/todo");
    }

    // TODO:auto login
    let is_trying_auto_login = false;

    let email = "";
    let password = "";
    let submit = undefined;
</script>

{#if is_trying_auto_login}
    <div class="section container">
        <h2>잠시만요...</h2>
        <p>자동 로그인 확인중입니다...</p>
    </div>
{:else}
    <div class="section container">
        <h1>로그인</h1>
        <div class="buttons">
            <a class="button" href="#/sign-up">회원가입</a>
            <a class="button" href="#/reset">비밀번호 재설정</a>
        </div>

        <div class="field">
            <label for="email">이메일</label>
            <input type="email" id="email" bind:value="{email}" placeholder="Email" required />
        </div>

        <div class="field">
            <label for="password">비밀번호</label>
            <input
                type="password"
                id="password"
                bind:value="{password}"
                placeholder="Password"
                required
                minlength="8" />
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
                                push('/todo');
                            } else if (json.status === false) {
                                alert(json.message);
                                submit.classList.remove('spin');
                            } else {
                                throw 'req_fail:login';
                            }
                        })
                        .catch(() => {
                            alert('알 수 없는 오류가 발생했습니다.');
                            submit.classList.remove('spin');
                        });
                }
            }}">로그인</button>
    </div>
{/if}

<style>
    .field {
        display: block;
        margin-top: 30px;
        margin-bottom: 30px;
    }

    label {
        display: block;
        font-size: 40px;
        font-weight: 500;
    }
</style>
