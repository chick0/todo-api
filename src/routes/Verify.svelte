<script>
    import { push } from "svelte-spa-router";
    import { VERIFY, VERIFY_SESSION } from "src/url.js";
    import { to_string } from "src/time.js";

    const verify_token = sessionStorage.getItem("to-do:verify_token");

    let is_loaded = false;
    let date;

    if (verify_token == null) {
        alert("이메일 인증 요청이 올바르지 않습니다.");
        push("/");
    } else {
        fetch(VERIFY_SESSION, {
            headers: {
                "x-auth": verify_token,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status) {
                    date = to_string(json.exp);
                    is_loaded = true;
                } else {
                    alert(json.message);
                }
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
                location.reload();
            });
    }

    /**
     * Send verify answer to server
     *
     * @param {boolean} answer true is pass, false to not pass
     */
    function send(answer) {
        is_loaded = true;
        fetch(VERIFY, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-auth": verify_token,
            },
            body: JSON.stringify({
                answer: answer,
            }),
        })
            .then((resp) => resp.json())
            .then((json) => {
                alert(json.message);

                if (json.status == true) {
                    sessionStorage.removeItem("to-do:verify_token");
                }

                push("/");
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
            });
    }
</script>

<div class="container">
    <h1>이메일 인증</h1>
    {#if is_loaded != true}
        <div class="spinner"></div>
    {:else}
        <br />
        <p>이 이메일 인증 요청은 <b>{date}</b>에 만료됩니다.</p>
        <br />
        <p>만약, 본인의 인증 시도가 아니라면 '<b>❌ 인증 취소</b>'를 선택하거나, 무시하면 됩니다.</p>
        <hr />
        <div class="buttons">
            <button
                class="button"
                on:click="{() => {
                    if (confirm('해당 요청을 취소하시겠습니까?')) {
                        send(false);
                    }
                }}">❌ 인증 취소</button>
            <button
                class="button"
                on:click="{() => {
                    if (confirm('해당 요청을 승인하시겠습니까?')) {
                        send(true);
                    }
                }}">✔️ 인증 승인</button>
        </div>
    {/if}
</div>

<style>
    .button {
        width: calc(50% - 3px);
    }
</style>
