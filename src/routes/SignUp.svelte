<script>
    // TODO:if login goto todos

    let email = undefined;
    let password = undefined;
    let submit = undefined;
</script>

<div class="section container">
    <h1>회원가입</h1>
    <div class="buttons">
        <a class="button" href="#/login">로그인</a>
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
        }}">회원가입</button>
    </div>
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
