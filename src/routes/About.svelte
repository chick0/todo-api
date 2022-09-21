<script>
    import { is_login } from "../user.js";
</script>

<div class="section container">
    <h1>To-Do</h1>
    <div class="buttons">
        {#if !is_login()}
            <a class="button" href="#/login">로그인</a>
            <a class="button" href="#/sign-up">회원가입</a>
        {:else}
            <a class="button" href="#/todo">할 일</a>
            <a class="button" href="#/logout">로그아웃</a>
            <a class="button" href="#/quit">서비스 탈퇴</a>
        {/if}
    </div>

    <hr />

    <p><b>To-Do</b>는 웹에서 사용하는 간단한 투두 리스트 어플리케이션입니다.</p>
</div>
