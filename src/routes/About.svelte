<script>
    import { parse_labels } from "src/label.js";
    import "src/label.css";

    let raw_labels = "@1단계, @@2단계, @@@3단계\n\n@이렇게 첫 줄에 적히지 않은 라벨은 무시됩니다";
</script>

<div class="container">
    <h1>To-Do</h1>
    <br />
    <p><b>To-Do</b>는 간단한 할 일 목록 웹 애플리케이션입니다.</p>
</div>

<div class="container">
    <h2>할 일</h2>
    <br />
    <p>
        <b>To-Do</b>는 할 일을
        <a href="https://ko.wikipedia.org/wiki/%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4" target="_blank">마크다운</a>을
        이용해 작성할 수 있습니다.
    </p>
    <br />
    <p>#을 이용해서 제목을 표현할 수 있습니다.</p>
    <p>제목은 1단계부터 6단계까지 있으며, 단계가 높을수록 하위 제목입니다.</p>
    <br />
    <p>**로 감싸면 <b>이렇게</b> 굵은 글씨를 사용할 수 있습니다.</p>
    <p>*로 감싸면 <i>이렇게</i>&nbsp; 기울여진 글씨를 사용할 수 있습니다.</p>
    <p>~~로 감싸면 <del>이렇게</del> 취소 선을 사용할 수 있습니다.</p>
    <blockquote>
        <p>&gt; 를 이용하면 이렇게 별도의 박스가 생깁니다.</p>
    </blockquote>
    <br />
    <p>링크는 <a href="/#/sign-up">[이렇게](/#/sign-up)</a> 작성할 수 있습니다.</p>
    <br />
    <p>또 아래의 <b>라벨</b>을 이용해 할 일을 강조할 수 있습니다.</p>
</div>

<div class="container">
    <h2>라벨</h2>
    <br />
    <p><b>라벨</b>은 작성한 할 일을 쉽게 <u>강조</u>할 수 있는 기능입니다.</p>
    <br />
    <p>
        라벨은 <b>@</b>의 개수로 중요도를 설정할 수 있습니다. 중요도는 1단계부터 3단계까지 총 3가지로 나누어져 있습니다.
        라벨은 중요도 순서로 정렬됩니다. 할 일 역시 라벨을 이용해 정렬됩니다.
    </p>
    <br />
    <p>
        <b>주의!</b> 첫 줄에 적히지 않은 라벨은 무시됩니다!
    </p>
    <p><b>라벨</b>을 직접 사용해보세요!</p>
    <ul class="label-test">
        <li>
            <textarea rows="5" maxlength="500" bind:value="{raw_labels}"></textarea>
            <p>{raw_labels.length}/500자</p>
        </li>
        <li>
            <div class="labels">
                {#each parse_labels(raw_labels) as label}
                    <span class="lv{label.level}">{label.text}</span>
                {/each}
            </div>
        </li>
    </ul>
</div>

<div style="margin-bottom: 30vh;"></div>

<div class="container">
    <h2>단축키</h2>
    <br />
    <p>편의성을 위해 <b>To-Do</b>는 몇 가지 단축키를 제공합니다.</p>
    <div class="table-wrapped">
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">키</th>
                    <th>설명</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Shift + 2</td>
                    <td>로그인 화면으로 이동하거나 로그아웃합니다.</td>
                </tr>
                <tr>
                    <td>Shift + 3</td>
                    <td>할 일 목록 화면으로 이동합니다. 또는 새로운 할 일 메뉴를 펼칩니다.</td>
                </tr>
                <tr>
                    <td>Ctrl + Enter</td>
                    <td>작성 중인 할 일을 저장합니다.</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<div style="margin-bottom: 30vh;"></div>

<style>
    div.container {
        margin-bottom: 15vh;
    }

    p {
        font-size: 25px;
        padding-bottom: 10px;
    }

    blockquote p {
        padding: 5px;
    }

    .label-test > li {
        float: left;
        width: calc(50% - 20px);
    }

    .label-test > li:first-child {
        margin-right: 20px;
    }

    .label-test > li::before {
        content: none;
    }

    .label-test > li > p {
        font-size: 18px;
    }

    td:last-child {
        text-align: left;
        padding-left: 20px;
    }
</style>
