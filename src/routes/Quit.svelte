<script>
    import { push } from "svelte-spa-router";
    import { QUIT } from "src/url.js";
    import { is_login, get_token } from "src/user.js";

    const TOKEN = get_token();

    if (!is_login()) {
        push("/login");
    }

    let step = 1;
    let is_loading = false;

    // step 1
    let password = "";
    let submit = undefined;

    // step 2
    let quit_token = "";
</script>

<div class="container">
    <h1>회원 탈퇴</h1>
    <br />
    {#if is_loading == true}
        <div class="spinner"></div>
    {:else if step == 1}
        <p>회원 탈퇴를 계속하려면, 비밀번호를 다시 입력해주세요.</p>

        <div class="field">
            <label for="password">비밀번호</label>
            <input
                type="password"
                id="password"
                placeholder="Password"
                required
                minlength="8"
                bind:value="{password}"
                on:keydown="{(e) => {
                    if (e.key == 'Enter') {
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
                fetch(QUIT, {
                    method: 'POST',
                    headers: {
                        'x-auth': TOKEN,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        password: password,
                    }),
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        if (json.status === true) {
                            quit_token = json.token;
                            step = 2;
                        }

                        alert(json.message);
                        is_loading = false;
                        password = '';

                        if (json.logout_required == true) {
                            push('/logout');
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">다음</button>
    {:else if step == 2}
        <div class="field">
            <p>'다음' 버튼을 누르면 회원 탈퇴가 완료됩니다.</p>
            <br />
            <p>삭제된 정보는 복구 할 수 없으며, 탈퇴 이후 다시 가입 할 수 있습니다.</p>
        </div>

        <button
            class="button max"
            type="submit"
            on:click="{() => {
                is_loading = true;
                fetch(QUIT, {
                    method: 'DELETE',
                    headers: {
                        'x-auth': TOKEN,
                        'x-quit': quit_token,
                    },
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        if (json.status === true) {
                            json.logout_required = true;
                        }

                        alert(json.message);
                        is_loading = false;

                        if (json.logout_required == true) {
                            push('/logout');
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">다음</button>
    {/if}
</div>
