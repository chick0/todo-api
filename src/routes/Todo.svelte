<script>
    import { push } from "svelte-spa-router";
    import { TODO, TODO_CHECK } from "../url.js";
    import { is_login, get_token } from "../user.js";
    import { to_datestring } from "../time.js";

    const TOKEN = get_token();

    let todos = [];
    let newTodo = "새로운 To-Do를 여기에 입력해주세요!";
    let newTodoElement = undefined;

    let isLoading = true;

    if (!is_login()) {
        push("/login");
    } else {
        fetch(TODO, {
            headers: {
                "x-auth": TOKEN,
            },
        })
            .then((resp) => resp.json())
            .then((json) => {
                if (json.status === true) {
                    todos = json.todos;
                    isLoading = false;
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
</script>

<div class="section container">
    <h1>To-Do</h1>
    <div class="buttons">
        <a class="button" href="#/user">계정 정보</a>
        <a class="button" href="#/logout">로그아웃</a>
    </div>

    <hr />
    {#if isLoading == true}
        <div class="spinner"></div>
    {:else}
        <div class="todo new">
            <textarea
                maxlength="500"
                bind:value="{newTodo}"
                bind:this="{newTodoElement}"
                on:input="{() => {
                    newTodoElement.style.height = '1px';
                    newTodoElement.style.height = 12 + newTodoElement.scrollHeight + 'px';
                }}"
                on:blur="{() => {
                    newTodo = newTodo.trim().slice(0, 500);

                    if (confirm('저장하시겠습니까?')) {
                        newTodoElement.setAttribute('contenteditable', 'false');
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
                                    newTodoElement.setAttribute('contenteditable', 'true');

                                    todos.unshift(json.todo);
                                    todos = todos;
                                } else {
                                    alert(json.message);
                                    newTodoElement.setAttribute('contenteditable', 'true');
                                }

                                if (json.logout_required == true) {
                                    push('/logout');
                                }
                            })
                            .catch(() => {
                                alert('알 수 없는 오류가 발생했습니다.');
                                newTodoElement.setAttribute('contenteditable', 'true');
                            });
                    }
                }}"></textarea>
            <p>{newTodo.length}/500자</p>
        </div>

        {#each todos as todo}
            <div class="todo {todo.checked == true ? 'ok' : 'no'}">
                <input
                    type="checkbox"
                    readonly="{todo.checked_pending != true}"
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

                <textarea
                    maxlength="500"
                    readonly="{todo.pending_text == true}"
                    bind:this="{todo.textarea}"
                    bind:value="{todo.text}"
                    on:mousemove="{() => {
                        if (todo.onetime != true) {
                            todo.textarea.style.height = '1px';
                            todo.textarea.style.height = 12 + todo.textarea.scrollHeight + 'px';
                            todo.onetime = true;
                        }
                    }}"
                    on:input="{() => {
                        todo.textarea.style.height = '1px';
                        todo.textarea.style.height = 12 + todo.textarea.scrollHeight + 'px';
                    }}"
                    on:blur="{() => {
                        todo.text = todo.text.trim().slice(0, 500);

                        if (todo.save_last_ask == undefined) {
                            todo.save_last_ask = Date.now() - 10000;
                        } else if (Date.now() - todo.save_last_ask < 2000) {
                            console.warn('2초이내 수정시도 무시됨.', Date.now() - todo.save_last_ask + '초');
                            return;
                        }

                        todo.save_last_ask = Date.now();

                        if (confirm('저장하시겠습니까?')) {
                            todo.pending_text = true;
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
                                    if (json.status == true) {
                                        todo.text = json.text;
                                    } else {
                                        alert(json.message);
                                    }

                                    todo.pending_text = false;

                                    if (json.logout_required == true) {
                                        push('/logout');
                                    }
                                })
                                .catch(() => {
                                    alert('알 수 없는 오류가 발생했습니다.');
                                    todo.pending_text = false;
                                });
                        }
                    }}"></textarea>

                <p>
                    {#if todo.checked}
                        {to_datestring(todo.created_at)} ~ {to_datestring(todo.checked_at)}
                    {:else}
                        {to_datestring(todo.created_at)}
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
    textarea {
        font-family: "Pretendard", "Noto Sans KR", "Malgun Gothic", sans-serif;
        font-size: 20px;

        display: block;
        overflow: hidden;
        overflow-wrap: break-word;
        resize: none;

        width: 100%;
        min-height: 60px;

        border: none;
        background-color: var(--background);
        color: var(--color);
    }

    .todo:not(.new) > textarea {
        margin-top: -35px;
        margin-left: 45px;
        width: calc(100% - 45px);
    }

    /* Todo Element */
    .todo {
        padding: 15px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px var(--todo-shadow);
    }

    .todo.ok {
        --todo-shadow: green;
    }

    .todo.no {
        --todo-shadow: red;
    }

    .todo.new {
        --todo-shadow: blue;
    }

    /* Todo Checkbox */
    .todo > input[type="checkbox"] {
        width: 30px;
        height: 30px;
    }

    /* Todo Datetext */
    .todo > p {
        margin-top: 10px;
        font-size: 18px;
        font-weight: 200;
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
