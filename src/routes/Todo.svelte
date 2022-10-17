<script>
    import { push } from "svelte-spa-router";
    import { TODO, TODO_CHECK } from "src/url.js";
    import { is_login, get_token } from "src/user.js";
    import { has_label, parse_labels } from "src/label.js";
    import { to_string } from "src/time.js";
    import { get_html } from "src/markdown.js";

    /**
     * Fetch todo list from api server
     */
    function fetch_todos() {
        fetch(TODO, {
            headers: {
                "x-auth": TOKEN,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status) {
                    todos = json.todos.map((todo) => {
                        let labels = parse_labels(todo.text);

                        let high_level = labels[0]?.level;
                        if (high_level == undefined) {
                            high_level = 0;
                        }

                        todo.high_level = high_level;
                        todo.total_level = labels.map((label) => label.level).reduce((a, b) => a + b, 0);

                        todo.reset = todo.text;
                        todo.editmode = false;
                        return todo;
                    });

                    todos.sort((a, b) => {
                        if (a.checked || b.checked) {
                            return Number(a.checked) - Number(b.checked);
                        }

                        if (a.high_level == b.high_level) {
                            return b.total_level - a.total_level;
                        }

                        return b.high_level - a.high_level;
                    });

                    is_loading = false;
                } else {
                    alert(json.message);
                }

                if (json.logout_required) {
                    push("/logout");
                }
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
                push("/");
            });
    }

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

    /**
     * @typedef {Object} To_Do To-Do
     * @property {number} id
     * @property {boolean} checked
     * @property {string} text
     * @property {number} created_at
     * @property {number|null} checked_at
     * @property {boolean} checked_pending
     * @property {boolean} loading
     * @property {string} reset
     * @property {boolean} editmode
     * @property {HTMLElement} textarea
     * @property {HTMLElement} button
     * @property {number} high_level
     * @property {number} total_level
     */

    /**
     * @type {To_Do[]}
     */
    let todos = [];

    let newTodo = "";
    let newTodoOpen = false;
    let newTodoElement = undefined;
    let newTodoSave = undefined;
    let newTodoLoading = false;

    let is_loading = true;

    if (!is_login()) {
        push("/login");
    } else {
        fetch_todos();
    }
</script>

<div class="container">
    <h1>할 일</h1>
    <div class="buttons">
        <button
            class="button"
            on:click="{() => {
                if (is_loading == false) {
                    is_loading = true;
                    todos = [];
                    fetch_todos();
                }
            }}">새로고침</button>
        <a class="button" href="#/todo/clean-up">정리하기</a>
    </div>

    <br class="breakpoint" />

    {#if is_loading}
        <div class="spinner"></div>
    {:else}
        {#if newTodoOpen == false}
            <p
                class="clickable open"
                on:click="{() => {
                    newTodoOpen = true;
                }}">
                [<b>+</b>] 펼치기
            </p>
        {:else}
            <p
                class="clickable"
                on:click="{() => {
                    newTodoOpen = false;
                }}">
                [<b>-</b>] 접기
            </p>
            <div class="todo new">
                <textarea
                    maxlength="500"
                    bind:value="{newTodo}"
                    bind:this="{newTodoElement}"
                    on:input="{() => autosize(newTodoElement)}"
                    on:keydown="{(e) => {
                        if (e.key == 'Escape') {
                            newTodoElement.blur();
                        } else if (e.ctrlKey && e.key == 'Enter') {
                            if (newTodo.length != 0) {
                                newTodoElement.blur();
                                newTodoSave.click();
                            }
                        }
                    }}"
                    on:blur="{() => {
                        if (newTodo.length == 0) {
                            newTodoOpen = false;
                        }
                    }}"></textarea>
                <p>{newTodo.length}/500자</p>
                <br />
                <button
                    class="button max {newTodoLoading ? 'spin' : ''}"
                    bind:this="{newTodoSave}"
                    on:click="{() => {
                        if (newTodoLoading) {
                            return;
                        }

                        newTodoLoading = true;

                        fetch(TODO, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'x-auth': TOKEN,
                            },
                            body: JSON.stringify({
                                text: newTodo,
                            }),
                        })
                            .then((resp) => resp.json())
                            .then((json) => {
                                if (json.status) {
                                    newTodo = '';

                                    setTimeout(() => {
                                        if (newTodoOpen) {
                                            autosize(newTodoElement);
                                            newTodoElement?.focus();
                                        }
                                    }, 100);

                                    json.todo.reset = json.todo.text;
                                    json.todo.editmode = false;
                                    todos.unshift(json.todo);
                                    todos = todos;
                                } else {
                                    alert(json.message);
                                }

                                newTodoLoading = false;

                                if (json.logout_required) {
                                    push('/logout');
                                }
                            })
                            .catch(() => {
                                alert('알 수 없는 오류가 발생했습니다.');
                                newTodoLoading = false;
                            });
                    }}">새로운 할 일 저장</button>
            </div>
        {/if}

        <br class="breakpoint" />

        {#if todos.length == 0}
            <p>저장된 할 일이 없습니다!</p>
        {/if}

        {#each todos as todo}
            <div class="todo {todo.checked ? 'checked' : ''}">
                <input
                    type="checkbox"
                    disabled="{todo.checked_pending}"
                    bind:checked="{todo.checked}"
                    on:change="{() => {
                        todo.checked_at = Date.now() / 1000;
                        todo.checked_pending = true;

                        fetch(TODO_CHECK, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'x-auth': TOKEN,
                            },
                            body: JSON.stringify({
                                id: todo.id,
                                checked: todo.checked,
                            }),
                        })
                            .then((resp) => resp.json())
                            .then((json) => {
                                todo.checked_pending = false;
                                if (json.status) {
                                    todo.checked = json.checked;
                                    todo.checked_at = json.checked_at;
                                } else {
                                    alert(json.message);
                                }

                                if (json.logout_required) {
                                    push('/logout');
                                }
                            })
                            .catch(() => {
                                alert('알 수 없는 오류가 발생했습니다.');
                                todo.checked_pending = false;
                            });
                    }}" />

                {#if todo.editmode}
                    <textarea
                        maxlength="500"
                        readonly="{todo.loading}"
                        bind:this="{todo.textarea}"
                        bind:value="{todo.text}"
                        on:input="{() => autosize(todo.textarea)}"
                        on:focus="{() => autosize(todo.textarea)}"
                        on:blur="{() => {
                            todo.text = todo.text.trim();

                            if (todo.text == todo.reset) {
                                todo.editmode = false;
                            }
                        }}"
                        on:keydown="{(e) => {
                            if (e.key == 'Escape') {
                                todo.textarea.blur();
                            } else if (e.ctrlKey && e.key == 'Enter') {
                                todo.textarea.blur();

                                if (todo.editmode) {
                                    todo.button.click();
                                }
                            }
                        }}"></textarea>
                    <p>
                        {todo.text.length}/500자
                        <b
                            class="delete"
                            on:click="{() => {
                                if (confirm('취소하시겠습니까?')) {
                                    todo.editmode = false;
                                    todo.text = todo.reset;
                                }
                            }}">취소</b>
                    </p>
                    <br />
                    <button
                        class="button max {todo.loading ? 'spin' : ''}"
                        bind:this="{todo.button}"
                        on:click="{() => {
                            if (todo.loading) {
                                return;
                            }

                            todo.loading = true;

                            fetch(TODO, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'x-auth': TOKEN,
                                },
                                body: JSON.stringify({
                                    id: todo.id,
                                    text: todo.text,
                                }),
                            })
                                .then((resp) => resp.json())
                                .then((json) => {
                                    todo.loading = false;

                                    if (json.status) {
                                        todo.text = json.text;
                                        todo.reset = json.text;
                                        todo.editmode = false;
                                    } else {
                                        alert(json.message);

                                        if (json.text == null) {
                                            todos = todos.filter((x) => x.id != todo.id);
                                        }
                                    }

                                    if (json.logout_required) {
                                        push('/logout');
                                    }
                                })
                                .catch(() => {
                                    alert('알 수 없는 오류가 발생했습니다.');
                                    todo.loading = false;
                                });
                        }}">수정한 할 일 저장</button>
                {:else}
                    <div
                        on:dblclick="{() => {
                            if (todo.checked == false && todo.editmode == false) {
                                todo.editmode = true;
                                setTimeout(() => {
                                    todo.textarea?.focus();
                                }, 10);
                            }
                        }}">
                        {#if has_label(todo.text)}
                            <div class="labels">
                                {#each parse_labels(todo.text) as label}
                                    <span class="lv{label.level}">{label.text}</span>
                                {/each}
                            </div>
                        {/if}
                        <div class="todo-content">
                            {@html get_html(todo.text)}
                        </div>
                    </div>
                {/if}

                <p>
                    {#if todo.checked}
                        <span title="완료일">
                            {to_string(todo.checked_at)}
                        </span>
                    {:else}
                        <span title="생성일">
                            {to_string(todo.created_at)}
                        </span>
                    {/if}

                    <b
                        class="delete"
                        on:click="{() => {
                            if (confirm('삭제하시겠습니까?')) {
                                todos = todos.filter((x) => x.id != todo.id);

                                fetch(TODO, {
                                    method: 'DELETE',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'x-auth': TOKEN,
                                    },
                                    body: JSON.stringify({
                                        id: todo.id,
                                    }),
                                })
                                    .then((resp) => resp.json())
                                    .then((json) => {
                                        if (json.status == false) {
                                            alert(json.message);
                                        }

                                        if (json.logout_required) {
                                            push('/logout');
                                        }
                                    })
                                    .catch(() => {
                                        alert('알 수 없는 오류가 발생했습니다.');
                                    });
                            }
                        }}">삭제</b>
                    {#if todo.checked == false && todo.editmode == false}
                        <b
                            class="edit"
                            on:click="{() => {
                                todo.editmode = true;
                                setTimeout(() => {
                                    todo.textarea?.focus();
                                }, 10);
                            }}">수정</b>
                    {/if}
                </p>
            </div>
        {/each}
    {/if}
</div>

<style>
    /* New To-Do UI Open/Close button */
    p.clickable > b {
        display: inline-block;
        width: 15px;
        text-align: center;
    }

    /* To-Do Content area */
    div.todo-content {
        min-height: 25px;
        overflow-x: auto;
    }

    /* To-Do Element */
    .todo {
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px var(--todo-shadow);
    }

    .todo:not(.new) > textarea,
    .todo:not(.todo.new) > div {
        margin-top: -35px;
        margin-left: 45px;
        width: calc(100% - 45px);
    }

    .todo:not(.new):not(:last-child) {
        padding-bottom: 20px;
        border-bottom: 1px solid var(--color);
    }

    /* Change checked To-Do color */
    .todo.checked > div {
        color: var(--gray);
    }

    /* To-Do checkbox */
    .todo > input[type="checkbox"] {
        width: 30px;
        height: 30px;
    }

    /* To-Do date/time text */
    .todo > p {
        margin-top: 10px;
        font-size: 18px;
        font-weight: 400;
    }

    /* To-Do delete button */
    .delete {
        font-weight: 600;
        color: var(--red);
    }

    .delete:hover {
        cursor: pointer;
        text-shadow: 0 0 var(--text-shadow) var(--red);
    }

    /* To-Do edit button */
    .edit {
        font-weight: 600;
        color: var(--green);
    }

    .edit:hover {
        cursor: pointer;
        text-shadow: 0 0 var(--text-shadow) var(--green);
    }
</style>
