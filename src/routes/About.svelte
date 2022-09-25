<script>
    import { is_login } from "../user.js";
    let show_hidden_button = false;
</script>

<div class="section container">
    <h1
        on:dblclick="{() => {
            show_hidden_button = !show_hidden_button;
        }}">
        To-Do
    </h1>
    <div class="buttons">
        {#if !is_login()}
            <a class="button" href="#/login">로그인</a>
            <a class="button" href="#/sign-up">회원가입</a>
        {:else}
            <a class="button" href="#/todo">할 일</a>
            <a class="button" href="#/user">계정 정보</a>
            <a class="button" href="#/logout">로그아웃</a>
        {/if}
        {#if show_hidden_button}
            <a class="button" href="#/version">버전 정보</a>
            <a class="button" href="/cache.html">캐시 관리자</a>
        {/if}
    </div>

    <hr />

    <p><b>To-Do</b>는 간단한 할 일 목록 웹 애플리케이션입니다.</p>
</div>
