<script>
    import { push } from "svelte-spa-router";
    import { get_token, is_login } from "../../user.js";
    import { COUNTRY, COUNTRY_CODES } from "../../url.js";
    import { to_datestring, to_timestring } from "../../time.js";

    /**
     * Get now country and selected countrys
     */
    function fetch_country_status() {
        is_loading = true;
        fetch(COUNTRY, {
            headers: {
                "x-auth": TOKEN,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status == true) {
                    is_loading = false;
                    code = json.code;
                    name = json.name;
                    countrys = json.countrys;

                    fetch_select_able();
                } else {
                    alert(json.message);
                }

                if (json.logout_required == true) {
                    push("/logout");
                }
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
                push("/user");
            });
    }

    /**
     * Get select able country
     */
    function fetch_select_able() {
        fetch(COUNTRY_CODES, {
            headers: {
                "x-auth": TOKEN,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status == true) {
                    select_able = json.codes;

                    if (select_able.filter((x) => x.code == "KR").length == 1) {
                        selected = code;
                    } else {
                        selected = "";
                    }
                } else {
                    alert(json.message);
                }

                if (json.logout_required == true) {
                    push("/logout");
                }
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
                push("/user");
            });
    }

    const TOKEN = get_token();
    let is_loading = true;

    let code = null;
    let name = null;
    let countrys = [];

    let selected = "";
    let select_able = [];
    let select_submit = undefined;

    if (!is_login()) {
        push("/login");
    } else {
        fetch_country_status();
    }
</script>

<div class="section container">
    <h1>로그인 허용 국가</h1>
    <div class="buttons">
        <a class="button" href="#/user">계정 정보</a>
    </div>
    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        <br />
        <p class="summary">현재 접속중인 국가는 <u>{name}</u>입니다.</p>
        <br />
        {#if countrys.length == 0}
            <p class="summary">허용 국가가 설정되지 않았습니다!</p>
            <p class="summary"><u>모든 국가</u>에서 로그인 할 수 있습니다.</p>
        {:else}
            <p class="summary">허용 국가가 설정되었습니다.</p>
            <p class="summary"><u>설정된 국가에서만</u> 로그인 할 수 있습니다.</p>
            <br />
            <div class="table-wrapped">
                <table>
                    <thead>
                        <tr>
                            <th class="w-70"></th>
                            <th>허용된 국가</th>
                            <th colspan="2">허용 날짜</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each countrys as country}
                            <tr>
                                <td
                                    class="clickable"
                                    on:click="{() => {
                                        is_loading = true;
                                        fetch(COUNTRY, {
                                            method: 'DELETE',
                                            headers: {
                                                'Content-Type': 'application/json',
                                                'x-auth': TOKEN,
                                            },
                                            body: JSON.stringify({
                                                id: country.id,
                                            }),
                                        })
                                            .then((resp) => resp.json())
                                            .then((json) => {
                                                if (json.status == true) {
                                                    fetch_country_status();
                                                    return;
                                                } else {
                                                    alert(json.message);
                                                }

                                                if (json.logout_required == true) {
                                                    push('/logout');
                                                }

                                                is_loading = false;
                                            })
                                            .catch(() => {
                                                alert('알 수 없는 오류가 발생했습니다.');
                                                is_loading = false;
                                            });
                                    }}">삭제</td>
                                <td>{country.name}</td>
                                <td>{to_datestring(country.created_at)}</td>
                                <td>{to_timestring(country.created_at)}</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}
        <hr />
        <div>
            <h2>허용 국가 설정</h2>

            <div class="field">
                <select bind:value="{selected}">
                    {#each select_able as country}
                        <option value="{country.code}">{country.name}</option>
                    {/each}
                </select>
            </div>

            <button
                class="button max"
                bind:this="{select_submit}"
                on:click="{() => {
                    if (select_submit.classList.contains('spin')) {
                        alert('저장하고있습니다. 잠시만 기다려주세요.');
                        return;
                    }

                    select_submit.classList.add('spin');
                    fetch(COUNTRY, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'x-auth': TOKEN,
                        },
                        body: JSON.stringify({
                            code: selected,
                        }),
                    })
                        .then((resp) => resp.json())
                        .then((json) => {
                            if (json.status == true) {
                                fetch_country_status();
                                return;
                            } else {
                                alert(json.message);
                            }

                            if (json.logout_required == true) {
                                push('/logout');
                            }

                            select_submit.classList.remove('spin');
                        })
                        .catch(() => {
                            alert('알 수 없는 오류가 발생했습니다.');
                            select_submit.classList.remove('spin');
                        });
                }}">추가하기</button>
        </div>
    {/if}
</div>

<style>
    p.summary {
        font-size: 28px;
        font-weight: 400;
    }

    .w-70 {
        width: 70px;
    }

    .clickable {
        color: var(--red);
    }

    .clickable:hover {
        text-shadow: 0 0 3px var(--red);
    }
</style>
