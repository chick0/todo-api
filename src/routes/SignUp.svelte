<script>
    import { push } from "svelte-spa-router";
    import { SIGN_UP } from "../url.js";

    // TODO:if login / go to todo page

    let email = "";
    let password = "";
    let submit = undefined;
</script>

<div class="section container">
    <h1>회원가입</h1>
    <div class="buttons">
        <a class="button" href="#/login">로그인</a>
        <a class="button" href="#/find">계정 찾기</a>
    </div>

    <div class="field">
        <label for="email">이메일</label>
        <input type="email" id="email" bind:value="{email}" placeholder="Email" required />
    </div>

    <div class="field">
        <label for="password">비밀번호</label>
        <input type="password" id="password" bind:value="{password}" placeholder="Password" required minlength="8" />
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
                    method: "POST",
                    body: JSON.stringify({
                        "email": email,
                        "password": password
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    },
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        if(json.status === true) {
                            alert(json.message);
                            push("/login");
                        } else if (json.status === false) {
                            alert(json.message);
                            submit.classList.remove('spin');
                        } else {
                            throw "req_fail";
                        }
                    })
                    .catch(() => {
                        alert("알 수 없는 오류가 발생했습니다.");
                        submit.classList.remove('spin');
                    });
            }
        }}">회원가입</button>
</div>

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
