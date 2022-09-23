<script>
    import { push } from "svelte-spa-router";
    import { Renderer, setOptions, parse } from "marked";
    import { TODO, TODO_CHECK } from "../url.js";
    import { is_login, get_token } from "../user.js";
    import { to_datestring } from "../time.js";

    const TOKEN = get_token();

    let todos = [];
    let newTodo = "";
    let newTodoElement = undefined;
    let newTodoSave = undefined;

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

                    if (todos.length == 0) {
                        newTodo = "새로운 To-Do를 여기에 입력해주세요!\n\n마크다운 문법을 사용 할 수 있습니다 :)";
                        setTimeout(() => {
                            newTodoElement.style.height = "100px";
                        }, 100);
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

    const renderer = new Renderer();

    // @ts-ignore
    renderer.link = (href, title, text) => {
        return `<a target="_blank" rel="noreferrer" href="${href}">${text}</a>`;
    };

    setOptions({
        gfm: true,
        renderer: renderer,
    });
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

        <hr />

        {#if todos.length == 0}
            <p>저장된 할 일이 없습니다!</p>
        {/if}

        {#each todos as todo}
            <div class="todo {todo.checked == true ? 'checked' : ''}">
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
                        }}"></textarea>
                    <p>{todo.text.length}/500자</p>
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
                        on:dblclick="{() => {
                            if (todo.checked == false) {
                                todo.editmode = true;
                                setTimeout(() => {
                                    todo.textarea.focus();
                                }, 300);
                            }
                        }}">
                        {@html parse(todo.text)}
                    </div>
                {/if}

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
        font-family: "Malgun Gothic", sans-serif;
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
