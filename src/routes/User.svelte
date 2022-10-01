<script>
    import { push } from "svelte-spa-router";
    import { USER, SESSION_DELETE, PIN, MORE_HISTORY } from "../url.js";
    import { is_login, get_token, get_payload } from "../user.js";
    import { get_pin_token } from "../pin.js";
    import { to_datestring, to_timestring } from "../time.js";

    const TOKEN = get_token();
    const payload = get_payload();

    let is_loading = true;
    let has_pin_token = get_pin_token() != null;

    let count = "-";
    let email = payload?.email;
    let pin_list = [];
    let history_list = [];
    let session_list = [];

    let more_history_button = undefined;
    let history_cursor = null;
    $: history_cursor = history_list[history_list.length - 1]?.id;

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
                    count = json.count;
                    pin_list = json.pin_list;
                    session_list = json.session_list;
                    history_list = json.history_list;

                    is_loading = false;
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

        <p class="summary">
            이 계정의 이메일 주소는 <u>{email}</u>이며, 등록된 할 일은 총 <u>{count}개</u>가 있습니다.
        </p>

        <hr />

        <h2>PIN</h2>
        {#if has_pin_token == false || pin_list.length == 0}
            <div class="buttons">
                <a class="button" href="#/pin/create">PIN 생성하기</a>
            </div>
        {/if}

        {#if pin_list.length == 0}
            <p>등록된 PIN이 없습니다.</p>
        {:else}
            <div class="table-wrapped">
                <table>
                    <thead>
                        <tr>
                            <th class="w-70"></th>
                            <th colspan="2">생성 날짜</th>
                            <th>실패 횟수</th>
                            <th>설정된 기기</th>
                            <th colspan="2">마지막 사용 날짜</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each pin_list as pin}
                            <tr>
                                <td
                                    class="clickable"
                                    on:click="{() => {
                                        if (confirm('해당 PIN을 삭제하시겠습니까?')) {
                                            fetch(PIN, {
                                                method: 'DELETE',
                                                headers: {
                                                    'Content-Type': 'application/json',
                                                    'x-auth': TOKEN,
                                                },
                                                body: JSON.stringify({
                                                    id: pin.id,
                                                }),
                                            })
                                                .then((resp) => resp.json())
                                                .then((json) => {
                                                    alert(json.message);

                                                    if (json.status) {
                                                        pin_list = pin_list.filter((x) => x.id != pin.id);
                                                    }

                                                    if (json.logout_required == true) {
                                                        push('/logout');
                                                    }
                                                })
                                                .catch(() => {
                                                    alert('알 수 없는 오류가 발생했습니다.');
                                                });
                                        }
                                    }}">삭제</td>
                                <td>{to_datestring(pin.created_at)}</td>
                                <td>{to_timestring(pin.created_at)}</td>
                                <td class="{pin.fail_count == 0 ? 'green' : pin.fail_count > 5 ? 'red' : ''}">
                                    {pin.fail_count}회
                                </td>
                                <td>{pin.device}</td>
                                {#if pin.last_access == null}
                                    <td colspan="2">기록 없음</td>
                                {:else}
                                    <td>{to_datestring(pin.last_access)}</td>
                                    <td>{to_timestring(pin.last_access)}</td>
                                {/if}
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}

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
        <div class="table-wrapped">
            <table>
                <thead>
                    <tr>
                        <th class="w-70"></th>
                        <th>로그인 시간</th>
                        <th>세션 만료 시간</th>
                        <th>마지막 사용시간</th>
                        <th>기기 정보</th>
                    </tr>
                </thead>
                <tbody>
                    {#each session_list as session}
                        <tr>
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

                                                    if (session_list.length == 0) {
                                                        json.logout_required = true;
                                                    }
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
                                }}"
                                >삭제
                            </td>
                            <td>{to_timestring(session.created_at)}</td>
                            <td>{to_timestring(session.dropped_at)}</td>
                            {#if session.last_access == null}
                                <td colspan="2">기록 없음</td>
                            {:else}
                                <td>{to_timestring(session.last_access)}</td>
                            {/if}
                            <td>{session.device}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <hr />

        <h2>로그인 기록</h2>
        <div class="buttons">
            <a class="button" href="#/security/country">로그인 허용 국가 설정</a>
        </div>
        <div class="table-wrapped">
            <table>
                <thead>
                    <tr>
                        <th colspan="2">로그인 날짜</th>
                        <th>기기 IP</th>
                        <th>기기 정보</th>
                    </tr>
                </thead>
                <tbody>
                    {#each history_list as history}
                        <tr>
                            <td>{to_datestring(history.created_at)}</td>
                            <td>{to_timestring(history.created_at)}</td>
                            <td>{history.ip}</td>
                            <td>{history.device}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
        <br />
        <button
            class="button max"
            bind:this="{more_history_button}"
            on:click="{() => {
                if (more_history_button.classList.contains('spin')) {
                    alert('이전 기록들을 가져오고 있습니다. 잠시만 기다려주세요.');
                    return;
                }

                more_history_button.classList.add('spin');
                fetch(MORE_HISTORY(history_cursor), {
                    headers: {
                        'x-auth': TOKEN,
                    },
                })
                    .then((resp) => resp.json())
                    .then((json) => {
                        if (json.status) {
                            json.history_list.forEach((history) => {
                                history_list.push(history);
                            });

                            history_list = history_list;
                        } else {
                            alert(json.message);
                        }

                        if (json.logout_required == true) {
                            push('/logout');
                        }

                        more_history_button.classList.remove('spin');
                    })
                    .catch(() => {
                        alert('알 수 없는 오류가 발생했습니다.');
                        more_history_button.classList.remove('spin');
                    });
            }}">기록 더 불러오기</button>
    {/if}
</div>

<style>
    .w-70 {
        width: 70px;
    }

    p.summary {
        font-size: 28px;
        font-weight: 400;
    }

    .clickable {
        color: var(--red);
    }

    .clickable:hover {
        text-shadow: 0 0 3px var(--red);
    }

    .red {
        color: var(--red);
    }

    .green {
        color: var(--green);
    }
</style>
