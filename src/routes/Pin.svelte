<script>
    import { push } from "svelte-spa-router";
    import { PIN_LOGIN } from "src/url.js";
    import { is_login, set_token } from "src/user.js";
    import { get_pin_token, clear_pin_token } from "src/pin.js";

    let is_loading = true;
    const pin_token = get_pin_token();

    let pin = "";
    let pin_input = undefined;
    let pin_button = undefined;

    if (is_login()) {
        push("/todo");
    } else {
        if (pin_token == null) {
            // push("/login");
            is_loading = false;
        } else {
            is_loading = false;
        }
    }
</script>

<div class="container">
    <h1>PIN</h1>
    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        <div class="buttons">
            <a class="button" href="#/login?force">또는 이메일 로그인</a>
        </div>

        <div class="field">
            <input
                id="pin"
                type="password"
                inputmode="numeric"
                minlength="6"
                placeholder="PIN을 입력해주세요."
                bind:this="{pin_input}"
                bind:value="{pin}"
                on:keydown="{(e) => {
                    if (e.key == 'Enter') {
                        pin_input.blur();
                        pin_button.click();
                    }
                }}" />
        </div>

        <button
            class="button max"
            type="submit"
            bind:this="{pin_button}"
            on:click="{() => {
                is_loading = true;
                fetch(PIN_LOGIN, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-pin': pin_token,
                    },
                    body: JSON.stringify({
                        code: pin.toString(),
                    }),
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        if (json.status == true) {
                            set_token(json.token);
                            push('/todo');
                        } else {
                            alert(json.message);
                            is_loading = false;
                            pin = '';

                            if (json.logout_required == true) {
                                clear_pin_token();
                                push('/login');
                            }
                        }
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        is_loading = false;
                    });
            }}">다음</button>
    {/if}
</div>
