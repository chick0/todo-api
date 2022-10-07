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
        <a class="button" href="/cache.html">캐시 관리자</a>
    </div>
    <br />
    <div class="table-wrapped">
        <table>
            <thead>
                <tr>
                    <th>클라이언트</th>
                    <th>서버</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{tag}</td>
                    <td>{server_id}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <br />
    <h3>빌드 날짜</h3>
    <p>- {build_date.toLocaleString()}</p>
    <br />
    <h3>서버 시작 날짜</h3>
    <p>- {to_string(started_at)}</p>
</div>

<style>
    table {
        table-layout: fixed;
    }
</style>
