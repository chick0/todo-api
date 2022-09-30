<script>
    import { onMount } from "svelte";
    import { VERSION } from "../url.js";
    import { to_string } from "../time.js";

    let tag = TAG;
    let build_date = new Date(BUILD_DATE);

    let server_id = "-";
    let started_at = null;

    onMount(() => {
        fetch(VERSION)
            .then((resp) => resp.json())
            .then((json) => {
                server_id = json.id;
                started_at = json.started_at;
            })
            .catch(() => {
                alert("서버 정보를 가져오는데 실패했습니다.");
            });
    });
</script>

<div class="section container">
    <h1>버전 정보</h1>
    <div class="buttons">
        <a class="button" href="/#/">메인 화면으로 이동</a>
    </div>
    <br />
    <div class="table-wrapped">
        <table>
            <thead>
                <tr>
                    <th style="width: 50%;">클라이언트 버전</th>
                    <th>빌드 날짜</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{tag}</td>
                    <td>{build_date.toLocaleString()}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <br />
    <ul>
        <li>서버 버전: {server_id}</li>
        <li>서버 시작 날짜: {to_string(started_at)}</li>
    </ul>
</div>
