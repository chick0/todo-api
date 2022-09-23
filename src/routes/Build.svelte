<script>
    let hash = GIT_HASH;
    let date = new Date(BUILD_DATE);
</script>

<div class="section container">
    <h1>빌드 정보</h1>
    <hr>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>빌드 날짜</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{hash}</td>
                <td>{date.toLocaleString()}</td>
            </tr>
        </tbody>
    </table>
</div>
