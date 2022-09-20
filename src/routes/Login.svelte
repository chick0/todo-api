<script>
    // TODO:if login goto todos

    let is_trying_auto_login = false;
    if (localStorage.getItem("to-do.token") != undefined) is_trying_auto_login = true;

    let email = undefined;
    let password = undefined;
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
            <a class="button" href="#/find">계정 찾기</a>
        </div>

        <div class="container">
            <div class="field">
                <label for="email">이메일</label>
                <input type="email" id="email" bind:this="{email}" placeholder="Email" required />
            </div>
    
            <div class="field">
                <label for="password">비밀번호</label>
                <input type="password" id="password" bind:this="{password}" placeholder="Password" required minlength="8" />
            </div>

            <button class="button max" type="submit" bind:this="{submit}" on:click="{() => {
                if(submit.classList.contains("spin")){
                    alert("이미 처리중입니다!");
                } else {
                    submit.classList.add("spin");

                    // TODO:fetch to api
                }
            }}">로그인</button>
        </div>
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
