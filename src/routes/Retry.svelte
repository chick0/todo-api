<script>
    import { push } from "svelte-spa-router";
    import { RETRY } from "../url.js";
    import { is_login } from "../user.js";

    let is_loading = true;
    let help_email = "-";

    let email = "";
    let email_input = undefined;
    let submit = undefined;

    if (is_login()) {
        push("/todo");
    } else {
        is_loading = false;
        fetch(RETRY)
            .then((resp) => resp.json())
            .then((json) => {
                if (json.help != null) {
                    help_email = json.help;
                } else {
                    help_email = "오류";
                }
            });
    }
</script>

<div class="section container">
    <h1>이메일 인증</h1>
    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        <div class="buttons">
            <a class="button" href="#/login">로그인</a>
            <a class="button" href="#/sign-up">회원가입</a>
            <a class="button" href="#/reset">비밀번호 재설정</a>
        </div>
        <hr />
        <p>5분마다 한 번씩 시도할 수 있습니다.</p>
        <p>반복해서 오류가 발생하는 경우에는 <b>{help_email}</b>로 메일을 보내주세요.</p>
        <div class="field">
            <label for="email-1">이메일</label>
            <input
                type="email"
                id="email-1"
                placeholder="Email"
                required
                bind:this="{email_input}"
                bind:value="{email}"
                on:keydown="{(e) => {
                    if (e.key == 'Enter') {
                        email_input.blur();
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
                fetch(RETRY, {
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
                        email = '';
                        is_loading = false;
                        alert(json.message);

                        if (json.status === true) {
                            push('/login');
                        }
                    })
                    .catch(() => {
                        is_loading = false;
                        alert('알 수 없는 오류가 발생했습니다.');
                    });
            }}">전송</button>
    {/if}
</div>
