<script>
    import { push } from "svelte-spa-router";
    import { get_token, is_login } from "src/user";
    import { CLEAN_UP } from "src/url";

    /**
     * Fetch todo usage status
     */
    function fetch_status() {
        fetch(CLEAN_UP, {
            headers: {
                "x-auth": TOKEN,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status) {
                    max = json.max;
                    total = json.total;
                    checked = json.checked;

                    is_loading = false;

                    if (total == 0) {
                        alert("등록한 할 일이 없습니다!");
                        push("/todo");
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
                push("/todo");
            });
    }

    /**
     * Calculate percent
     *
     * @param {number} a b / a
     * @param {number} b b / a
     * @returns {number} n
     */
    function cacl_percent(a, b) {
        let percent = Math.round((b / a) * 100);

        if (isNaN(percent)) {
            return 0;
        }

        return percent;
    }

    let is_loading = true;
    const TOKEN = get_token();

    let max = 0;
    let total = 0;
    let checked = 0;

    if (!is_login()) {
        push("/login");
    } else {
        fetch_status();
    }
</script>

<div class="container">
    <h1>할 일 정리</h1>

    {#if is_loading}
        <div class="spinner"></div>
    {:else}
        <div class="field">
            <h3>사용량</h3>
            <p>{cacl_percent(max, total)}%</p>
            <progress class="{cacl_percent(max, total) >= 80 ? 'red' : ''}" max="{max}" value="{total}">
                {cacl_percent(max, total)}%
            </progress>
        </div>

        <div class="field">
            <h3>완료비율</h3>
            <p>{cacl_percent(total, checked)}%</p>
            <progress class="{cacl_percent(total, checked) >= 70 ? 'red' : ''}" max="{total}" value="{checked}">
                {cacl_percent(total, checked)}%
            </progress>
            {#if checked != 0}
                <button
                    class="button max"
                    on:click="{() => {
                        is_loading = true;
                        fetch(CLEAN_UP, {
                            method: 'DELETE',
                            headers: {
                                'x-auth': TOKEN,
                            },
                        })
                            .then((resp) => resp.json())
                            .then((json) => {
                                if (json.status) {
                                    fetch_status();
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
                                push('/todo');
                            });
                    }}">완료한 할 일 삭제</button>
            {/if}
        </div>
    {/if}
</div>

<style>
    progress {
        --progress-color: var(--blue);
        -webkit-appearance: none;
        width: 100%;
        border: none;
        margin-bottom: 10px;
    }

    progress.red {
        --progress-color: var(--red);
    }

    ::-moz-progress-bar {
        background: var(--progress-color);
    }

    ::-webkit-progress-value {
        background: var(--progress-color);
    }

    ::-webkit-progress-bar {
        background: #e6e6e6;
    }
</style>
