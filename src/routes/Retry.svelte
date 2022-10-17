<script>
    import { push } from "svelte-spa-router";
    import { HELP, RETRY } from "src/url.js";
    import { is_login } from "src/user.js";

    let is_loading = true;
    let help_email = "-";

    let email = "";
    let email_input = undefined;
    let submit = undefined;

    if (is_login()) {
        push("/todo");
    } else {
        is_loading = false;

        fetch(HELP)
            .then((resp) => resp.json())
            .then((json) => {
                help_email = json.email;
            });
    }
</script>

<div class="container">
    <h1>이메일 인증</h1>
    {#if is_loading}
        <div class="spinner"></div>
    {:else}
        <p>5분마다 한 번씩 시도할 수 있습니다.</p>
        <br />
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

                        if (json.status) {
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
