<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import { get_token } from "src/user.js";
    import { ADMIN, NOTICE } from "src/url";
    import { get_html } from "src/markdown.js";
    import { to_string } from "src/time.js";

    /**
     * Auto-resizing textarea
     *
     * @param {HTMLElement} textarea textarea element
     */
    function autosize(textarea) {
        textarea.style.height = "1px";
        textarea.style.height = 12 + textarea.scrollHeight + "px";
    }

    const TOKEN = get_token();

    let is_loading = true;

    let is_admin = false;
    let open_new_todo = false;
    let new_notice_title = "";
    let new_notice_text = "";
    let new_notice_loading = false;
    let new_notice_submit = undefined;

    let notice_edit_id = 0;
    let notice_edit_mode = false;
    let notice_edit_title = "";
    let notice_edit_text = "";
    let notice_edit_loading = false;
    let notice_edit_submit = undefined;

    /**
     * @typedef {Object} Notice
     * @property {number} id
     * @property {string} title
     * @property {string} text
     * @property {number} created_at
     * @property {number|null} updated_at
     */

    /**
     * @type {Notice[]}
     */
    let notice_list = [];

    onMount(() => {
        fetch(NOTICE)
            .then((resp) => resp.json())
            .then((json) => {
                notice_list = json.notice_list;
                is_loading = false;
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
                push("/");
            });

        if (TOKEN != null) {
            fetch(ADMIN, {
                headers: {
                    "x-auth": TOKEN,
                },
            })
                .then((resp) => resp.json())
                .then((json) => {
                    if (json.admin === true) {
                        is_admin = true;
                    }
                });
        }
    });
</script>

<div class="container">
    <h1>공지사항</h1>
    {#if is_loading}
        <div class="spinner"></div>
    {:else}
        {#if notice_list.length == 0}
            <br />
            <p>등록된 공지가 없습니다!</p>
        {/if}

        {#if is_admin}
            <br />
            {#if open_new_todo == false}
                <p
                    class="clickable"
                    on:click="{() => {
                        if (notice_edit_mode) {
                            notice_edit_mode = false;
                        }

                        open_new_todo = true;

                        setTimeout(() => {
                            if (open_new_todo) {
                                document.getElementById('title').focus();
                            }
                        }, 100);
                    }}">
                    [<b>+</b>] 펼치기
                </p>
            {:else}
                <p
                    class="clickable"
                    on:click="{() => {
                        open_new_todo = false;
                    }}">
                    [<b>-</b>] 접기
                </p>

                <div>
                    <div class="field">
                        <label for="title">제목</label>
                        <input
                            id="title"
                            type="text"
                            maxlength="80"
                            on:keydown="{(event) => {
                                if (event.key == 'Escape') {
                                    event.currentTarget.blur();
                                } else if (event.key == 'Enter') {
                                    event.currentTarget.blur();
                                    event.preventDefault();
                                    document.getElementById('text').focus();
                                }
                            }}"
                            bind:value="{new_notice_title}" />
                    </div>

                    <div class="field">
                        <label for="text">본문</label>
                        <textarea
                            id="text"
                            on:input="{(event) => autosize(event.currentTarget)}"
                            on:keydown="{(event) => {
                                if (event.key == 'Escape') {
                                    event.currentTarget.blur();
                                } else if (event.ctrlKey && event.key == 'Enter') {
                                    event.currentTarget.blur();
                                    new_notice_submit.click();
                                }
                            }}"
                            bind:value="{new_notice_text}"></textarea>
                    </div>

                    <button
                        class="button max {new_notice_loading ? 'spin' : ''}"
                        bind:this="{new_notice_submit}"
                        on:click="{() => {
                            if (new_notice_loading) {
                                return;
                            }

                            new_notice_loading = true;

                            fetch(NOTICE, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'x-auth': TOKEN,
                                },
                                body: JSON.stringify({
                                    title: new_notice_title,
                                    text: new_notice_text,
                                }),
                            })
                                .then((resp) => resp.json())
                                .then((json) => {
                                    if (json.status) {
                                        notice_list.unshift(json.notice);
                                        notice_list = notice_list;
                                        open_new_todo = false;

                                        new_notice_title = '';
                                        new_notice_text = '';
                                    }

                                    alert(json.message);
                                    new_notice_loading = false;

                                    if (json.logout_required) {
                                        push('/logout');
                                    }
                                })
                                .catch(() => {
                                    alert('알 수 없는 오류가 발생했습니다.');
                                    new_notice_loading = false;
                                });
                        }}">공지사항 등록</button>
                </div>
            {/if}
        {/if}

        {#each notice_list as notice}
            <br />
            <div class="notice">
                <h2>{notice.title}</h2>

                {#if notice_edit_mode && notice_edit_id == notice.id}
                    <div class="field">
                        <div class="field">
                            <label for="edit-title">제목</label>
                            <input
                                id="edit-title"
                                type="text"
                                maxlength="80"
                                on:keydown="{(event) => {
                                    if (event.key == 'Escape') {
                                        event.currentTarget.blur();
                                    } else if (event.key == 'Enter') {
                                        event.currentTarget.blur();
                                        event.preventDefault();
                                        document.getElementById('edit-text').focus();
                                    }
                                }}"
                                bind:value="{notice_edit_title}" />
                        </div>

                        <div class="field">
                            <label for="edit-text">본문</label>
                            <textarea
                                id="edit-text"
                                on:focus="{(event) => autosize(event.currentTarget)}"
                                on:input="{(event) => autosize(event.currentTarget)}"
                                on:keydown="{(event) => {
                                    if (event.key == 'Escape') {
                                        event.currentTarget.blur();
                                    } else if (event.ctrlKey && event.key == 'Enter') {
                                        event.currentTarget.blur();
                                        notice_edit_submit.click();
                                    }
                                }}"
                                bind:value="{notice_edit_text}"></textarea>
                        </div>

                        <button
                            class="button max {notice_edit_loading ? 'spin' : ''}"
                            bind:this="{notice_edit_submit}"
                            on:click="{() => {
                                if (notice_edit_loading) {
                                    return;
                                }

                                notice_edit_loading = true;

                                let title_edited = notice.title != notice_edit_title;
                                let text_edited = notice.text != notice_edit_text;

                                if (title_edited == false && text_edited == false) {
                                    notice_edit_loading = false;
                                    notice_edit_mode = false;
                                    return;
                                }

                                fetch(NOTICE, {
                                    method: 'PATCH',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'x-auth': TOKEN,
                                    },
                                    body: JSON.stringify({
                                        id: notice.id,
                                        title: title_edited ? notice_edit_title : null,
                                        text: text_edited ? notice_edit_text : null,
                                    }),
                                })
                                    .then((resp) => resp.json())
                                    .then((json) => {
                                        if (json.status) {
                                            notice.title = json.notice.title;
                                            notice.text = json.notice.text;
                                            notice.updated_at = json.notice.updated_at;

                                            notice_edit_mode = false;
                                        }

                                        alert(json.message);
                                        notice_edit_loading = false;

                                        if (json.logout_required) {
                                            push('/logout');
                                        }
                                    })
                                    .catch(() => {
                                        alert('알 수 없는 오류가 발생했습니다.');
                                        notice_edit_loading = false;
                                    });
                            }}">변경사항 저장</button>
                    </div>
                {:else}
                    <div class="notice content">{@html get_html(notice.text)}</div>
                {/if}

                <ul class="dateinfo">
                    <li>작성시간 : {to_string(notice.created_at)}</li>
                    {#if notice.updated_at != null}
                        <li>수정시간 : {to_string(notice.updated_at)}</li>
                    {/if}
                </ul>

                {#if is_admin}
                    <div class="admin">
                        <b
                            class="clickable edit"
                            on:click="{() => {
                                if (notice_edit_mode) {
                                    if (notice_edit_id == notice.id) {
                                        notice_edit_mode = false;
                                        return;
                                    }
                                }

                                if (open_new_todo) {
                                    open_new_todo = false;
                                }

                                notice_edit_id = notice.id;
                                notice_edit_title = notice.title;
                                notice_edit_text = notice.text;

                                notice_edit_mode = true;

                                setTimeout(() => {
                                    if (notice_edit_mode) {
                                        let target = document.getElementById('edit-title');
                                        window.scrollTo(0, target.offsetTop - 60);
                                        target.focus();
                                    }
                                }, 100);
                            }}">수정</b>
                        <b
                            class="clickable delete"
                            on:click="{() => {
                                if (is_loading) {
                                    return;
                                }

                                is_loading = true;

                                fetch(NOTICE, {
                                    method: 'DELETE',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'x-auth': TOKEN,
                                    },
                                    body: JSON.stringify({
                                        id: notice.id,
                                    }),
                                })
                                    .then((resp) => resp.json())
                                    .then((json) => {
                                        if (json.status) {
                                            notice_list = notice_list.filter((x) => x.id != notice.id);
                                            notice_edit_mode = false;
                                        }

                                        alert(json.message);
                                        is_loading = false;

                                        if (json.logout_required) {
                                            push('/logout');
                                        }
                                    })
                                    .catch(() => {
                                        alert('알 수 없는 오류가 발생했습니다.');
                                        is_loading = false;
                                    });
                            }}">삭제</b>
                    </div>
                {/if}
            </div>
        {/each}
    {/if}
</div>

<style>
    p.clickable > b {
        display: inline-block;
        width: 15px;
        text-align: center;
    }

    div.notice {
        margin-top: 20px;
        margin-bottom: 20px;
    }

    div.content {
        font-size: 30px;
    }

    /* Set color */
    .admin b.edit {
        --local-color: var(--green);
    }

    .admin b.delete {
        --local-color: var(--red);
    }

    /* Apply style */
    .admin {
        margin-top: 10px;
    }

    .admin b {
        color: var(--local-color);
    }

    .admin b:hover {
        text-shadow: 0 0 var(--text-shadow) var(--local-color);
    }
</style>
