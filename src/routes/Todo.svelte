<script>
    import { push } from "svelte-spa-router";
    import { marked } from "marked";
    import DOMPurify from "dompurify";
    import { TODO, TODO_CHECK } from "../url.js";
    import { is_login, get_token } from "../user.js";
    import { to_datestring, to_timestring } from "../time.js";

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
                if (json.status === true) {
                    todos = json.todos.map((todo) => {
                        todo.reset = todo.text;
                        return todo;
                    });

                    is_loading = false;

                    if (todos.length == 0) {
                        newTodoOpen = true;
                        newTodo = "- 이 곳에 할 일을 적어주세요!\n- 마크다운 문법을 사용 할 수 있습니다.";
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
                push("/");
            });
    }

    /**
     * Timestamp to string
     *
     * @param {number} timestamp timestamp from python api
     * @returns {string} date or time string
     */
    function get_function(timestamp) {
        let now = Date.now() / 1000;
        if (now - timestamp > 3600) {
            return to_datestring(timestamp);
        } else {
            return to_timestring(timestamp);
        }
    }

    const TOKEN = get_token();

    let show_hidden_button = false;
    let todos = [];
    let newTodo = "";
    let newTodoOpen = false;
    let newTodoElement = undefined;
    let newTodoSave = undefined;

    let is_loading = true;

    if (!is_login()) {
        push("/login");
    } else {
        fetch_todos();
    }

    const renderer = new marked.Renderer();

    // @ts-ignore
    renderer.link = (href, title, text) => {
        return `<a target="_blank" rel="noreferrer" href="${href}">${text}</a>`;
    };

    marked.setOptions({
        renderer: renderer,
        headerIds: false,
    });
</script>

<div class="section container">
    <h1
        on:dblclick="{() => {
            show_hidden_button = !show_hidden_button;
        }}">
        To-Do
    </h1>
    <div class="buttons">
        <a class="button" href="#/user">계정 정보</a>
        <a class="button" href="#/logout">로그아웃</a>
        <button
            class="button"
            on:click="{() => {
                is_loading = true;
                todos = [];
                fetch_todos();
            }}">새로고침</button>
        {#if show_hidden_button}
            <a class="button" href="#/version">버전 정보</a>
            <a class="button" href="/cache.html">캐시 관리자</a>
        {/if}
    </div>

    <hr />
    {#if is_loading == true}
        <div class="spinner"></div>
    {:else}
        {#if newTodoOpen == false}
            <p
                class="clickable"
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
                    on:input="{() => {
                        newTodoElement.style.height = '1px';
                        newTodoElement.style.height = 12 + newTodoElement.scrollHeight + 'px';
                    }}"
                    on:keydown="{(e) => {
                        if (e.key == 'Escape') {
                            newTodoElement.blur();
                        } else if (e.ctrlKey == true && e.key == "Enter") {
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
                    class="button max"
                    bind:this="{newTodoSave}"
                    on:click="{() => {
                        newTodoSave.classList.add('spin');
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
                                if (json.status == true) {
                                    newTodo = '';

                                    json.todo.reset = json.todo.text;
                                    todos.unshift(json.todo);
                                    todos = todos;
                                } else {
                                    alert(json.message);
                                }

                                newTodoSave.classList.remove('spin');

                                if (json.logout_required == true) {
                                    push('/logout');
                                }
                            })
                            .catch(() => {
                                alert('알 수 없는 오류가 발생했습니다.');
                                newTodoSave.classList.remove('spin');
                            });
                    }}">새로운 할 일 저장</button>
            </div>
        {/if}

        <hr />

        {#if todos.length == 0}
            <p>저장된 할 일이 없습니다!</p>
        {/if}

        {#each todos as todo}
            <div class="todo {todo.checked == true ? 'checked' : ''}">
                <input
                    type="checkbox"
                    disabled="{todo.checked_pending == true}"
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
                                if (json.status == true) {
                                    todo.checked = json.checked;
                                    todo.checked_at = json.checked_at;
                                } else {
                                    alert(json.message);
                                }

                                if (json.logout_required == true) {
                                    push('/logout');
                                }
                            })
                            .catch(() => {
                                alert('알 수 없는 오류가 발생했습니다.');
                                todo.checked_pending = false;
                            });
                    }}" />

                {#if todo.editmode == true}
                    <textarea
                        maxlength="500"
                        readonly="{todo.button?.classList.contains('spin') === true}"
                        bind:this="{todo.textarea}"
                        bind:value="{todo.text}"
                        on:input="{() => {
                            todo.textarea.style.height = '1px';
                            todo.textarea.style.height = 12 + todo.textarea.scrollHeight + 'px';
                        }}"
                        on:focus="{() => {
                            todo.textarea.style.height = '1px';
                            todo.textarea.style.height = 12 + todo.textarea.scrollHeight + 'px';
                        }}"
                        on:keydown="{(e) => {
                            if (e.key == 'Escape') {
                                todo.textarea.blur();
                            } else if (e.ctrlKey == true && e.key == "Enter") {
                                if (todo.text.length != 0) {
                                    todo.textarea.blur();
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
                        class="button max"
                        bind:this="{todo.button}"
                        on:click="{() => {
                            todo.button.classList.add('spin');
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
                                    todo.button.classList.remove('spin');

                                    if (json.status == true) {
                                        todo.text = json.text;
                                        todo.reset = json.text;
                                        todo.editmode = false;
                                    } else {
                                        alert(json.message);

                                        if (json.text == null) {
                                            todos = todos.filter((x) => x.id != todo.id);
                                        }
                                    }

                                    if (json.logout_required == true) {
                                        push('/logout');
                                    }
                                })
                                .catch(() => {
                                    alert('알 수 없는 오류가 발생했습니다.');
                                    todo.button.classList.remove('spin');
                                });
                        }}">수정한 할 일 저장</button>
                {:else}
                    <div
                        class="todo-content"
                        on:dblclick="{() => {
                            if (todo.checked == false) {
                                todo.editmode = true;
                                setTimeout(() => {
                                    todo.textarea.focus();
                                }, 300);
                            }
                        }}">
                        {@html DOMPurify.sanitize(marked.parse(todo.text))}
                    </div>
                {/if}

                <p>
                    {#if todo.checked}
                        <span title="완료일">
                            {get_function(todo.checked_at)}
                        </span>
                    {:else}
                        <span title="생성일">
                            {get_function(todo.created_at)}
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

                                        if (json.logout_required == true) {
                                            push('/logout');
                                        }
                                    })
                                    .catch(() => {
                                        alert('알 수 없는 오류가 발생했습니다.');
                                    });
                            }
                        }}">삭제</b>
                </p>
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

    textarea {
        font-family: Pretendard, sans-serif;
        font-size: 20px;

        display: block;
        overflow: hidden;
        overflow-wrap: break-word;
        resize: none;

        width: 100%;
        min-height: 60px;

        padding: 10px;
        border: 1px solid var(--color);
        background-color: var(--background);
        color: var(--color);
    }

    /* Todo Element */
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

    .todo.checked > div {
        color: #a8a8a8;
    }

    /* Todo Checkbox */
    .todo > input[type="checkbox"] {
        width: 30px;
        height: 30px;
    }

    /* Todo content */
    .todo-content {
        min-height: 25px;
        overflow-x: scroll !important;
    }

    /* Todo Datetext */
    .todo > p {
        margin-top: 10px;
        font-size: 18px;
        font-weight: 400;
    }

    /* Delete button */
    .delete {
        cursor: pointer;
        font-weight: 600;
    }

    .delete:hover {
        color: crimson;
    }
</style>
