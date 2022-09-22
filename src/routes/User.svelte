<script>
    import { push } from "svelte-spa-router";
    import { USER, SESSION_DELETE } from "../url.js";
    import { is_login, get_token, get_payload } from "../user.js";
    import { to_datestring, to_timestring } from "../time.js";

    const TOKEN = get_token();
    const payload = get_payload();

    let is_loading = true;
    let history_list = [];
    let session_list = [];
    let count = "-";

    let colored_history = undefined;
    let email = "?";

    if (!is_login()) {
        push("/todo");
    } else {
        fetch(USER, {
            headers: {
                "x-auth": TOKEN,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status === true) {
                    history_list = json.history_list;
                    session_list = json.session_list;
                    count = json.count;
                    is_loading = false;

                    colored_history = session_list.filter((x) => x.id == payload.sid)[0].history_id;
                    email = payload.email;
                } else {
                    alert(json.message);
                }

                if (json.logout_required == true) {
                    push("/logout");
                }
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
            });
    }
</script>

<div class="section container">
    <h1>계정 정보</h1>
    <div class="buttons">
        <a class="button" href="#/todo">할 일</a>
        <a class="button" href="#/logout">로그아웃</a>
        <a class="button" href="#/user/quit">회원 탈퇴</a>
    </div>

    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        <hr />

        <p class="lead">이 계정의 이메일 주소는 <u>{email}</u>이며, 등록된 할 일은 총 <u>{count}개</u>가 있습니다.</p>

        <hr />

        <h2>로그인 세션</h2>
        <div class="buttons">
            <button
                class="button"
                on:click="{() => {
                    if (confirm("전체 세션을 삭제하시겠습니까?\n(삭제와 동시에 '모든' 기기에서 로그아웃이 됩니다.)")) {
                        is_loading = true;
                        fetch(SESSION_DELETE('all'), {
                            method: 'DELETE',
                            headers: {
                                'x-auth': TOKEN,
                            },
                        })
                            .then((resp) => resp.json())
                            .then((json) => {
                                if (json.status === true) {
                                    alert('전체 세션 삭제에 성공했습니다.');
                                    push('/logout');
                                } else {
                                    alert(json.message);
                                    is_loading = false;
                                }

                                if (json.logout_required == true) {
                                    push('/logout');
                                }
                            })
                            .catch(() => {
                                alert('알 수 없는 오류가 발생했습니다.');
                                is_loading = false;
                            });
                    }
                }}">전체 세션 삭제</button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>세션 ID</th>
                    <th>기록 ID</th>
                    <th>만료 날짜</th>
                    <th>만료 시간</th>
                    <th>마지막 사용시간</th>
                </tr>
            </thead>
            <tbody>
                {#each session_list as session}
                    <tr class="{session.history_id == colored_history ? 'colored' : ''}">
                        <td
                            class="clickable"
                            on:click="{() => {
                                if (
                                    confirm(
                                        "해당 세션을 삭제하시겠습니까?\n(삭제와 동시에 '해당' 기기에서 로그아웃이 됩니다)"
                                    )
                                ) {
                                    fetch(SESSION_DELETE(session.id), {
                                        method: 'DELETE',
                                        headers: {
                                            'x-auth': TOKEN,
                                        },
                                    })
                                        .then((resp) => resp.json())
                                        .then((json) => {
                                            if (json.status) {
                                                alert('해당 세션이 삭제되었습니다.');
                                                session_list = session_list.filter((x) => x.id != session.id);
                                            } else {
                                                alert(json.message);
                                            }

                                            if (json.logout_required == true) {
                                                push('/logout');
                                            }
                                        })
                                        .catch(() => {
                                            alert('알 수 없는 오류가 발생했습니다.');
                                        });
                                }
                            }}">{session.id}</td>
                        <td
                            class="clickable"
                            on:click="{() => {
                                colored_history = session.history_id;
                            }}">{session.history_id}</td>
                        <td>{to_datestring(session.dropped_at)}</td>
                        <td>{to_timestring(session.dropped_at)}</td>
                        <td>{to_timestring(session.last_access)}</td>
                    </tr>
                {/each}
            </tbody>
        </table>

        <hr />

        <h2>로그인 기록</h2>
        <table>
            <thead>
                <tr>
                    <th>기록 ID</th>
                    <th>로그인 날짜</th>
                    <th>로그인 시간</th>
                    <th>기기 IP</th>
                    <th>기기 정보</th>
                </tr>
            </thead>
            <tbody>
                {#each history_list as history}
                    <tr
                        class="clickable {history.id == colored_history ? 'colored' : ''}"
                        on:click="{() => {
                            colored_history = history.id;
                        }}">
                        <td>{history.id}</td>
                        <td>{to_datestring(history.created_at)}</td>
                        <td>{to_timestring(history.created_at)}</td>
                        <td>{history.ip}</td>
                        <td>{history.device}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {/if}
</div>

<style>
    .lead {
        font-size: 28px;
        font-weight: 300;
    }

    table {
        width: 100%;
        text-align: center;
        margin-top: 10px;
    }

    thead {
        border-bottom: 1px solid var(--color);
    }

    th {
        font-size: 25px;
        font-weight: 600;
    }

    th,
    td {
        padding: 10px;
    }

    th:not(:last-child),
    td:not(:last-child) {
        border-right: 1px solid var(--color);
    }

    tbody > tr:hover {
        box-shadow: 0 0 1px var(--color);
    }

    .colored {
        background-color: var(--color);
        color: var(--background);
    }

    .clickable {
        cursor: pointer;
    }
</style>
