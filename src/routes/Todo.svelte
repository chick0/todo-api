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
                if (json.result === true) {
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
        <a class="button" href="#/logout">로그아웃</a>
        <a class="button" href="#/quit">서비스 탈퇴</a>
    </div>

    <hr />
    {#if isLoading == true}
        <div class="spinner"></div>
    {:else}
        <div class="todo new">
            <div
                contenteditable="true"
                bind:textContent="{newTodo}"
                bind:this="{newTodoElement}"
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
                                if (json.result == true) {
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
                }}">
            </div>

            <p>{newTodo.length}/500자</p>
        </div>

        {#each todos as todo}
            <div class="todo {todo.checked == true ? 'ok' : 'no'}" bind:this="{todo.this}">
                <input
                    type="checkbox"
                    bind:checked="{todo.checked}"
                    readonly="{todo.checked_pending != true}"
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
                                if (json.result == true) {
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

                <div
                    class="content"
                    contenteditable="true"
                    bind:textContent="{todo.text}"
                    on:blur="{() => {
                        todo.text = todo.text.trim().slice(0, 500);

                        if (confirm('저장하시겠습니까?')) {
                            todo.this.setAttribute('contenteditable', 'false');
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
                                    if (json.result == true) {
                                        todo.text = json.text;
                                        todo.this.setAttribute('contenteditable', 'true');
                                    } else {
                                        alert(json.message);
                                        todo.this.setAttribute('contenteditable', 'true');
                                    }

                                    if (json.logout_required == true) {
                                        push('/logout');
                                    }
                                })
                                .catch(() => {
                                    alert('알 수 없는 오류가 발생했습니다.');
                                    todo.this.setAttribute('contenteditable', 'true');
                                });
                        }
                    }}">
                </div>

                <p contenteditable="false">
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
    .todo {
        padding: 15px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px var(--todo-shadow);
    }

    .todo.ok {
        --todo-shadow: lime;
    }

    .todo.no {
        --todo-shadow: crimson;
    }

    .todo.new {
        --todo-shadow: aqua;
    }

    .todo > input {
        width: 30px;
        height: 30px;
    }

    .todo > div {
        display: block;
        overflow-wrap: break-word;
    }

    .todo > div.content {
        margin-top: -35px;
        margin-left: 45px;
        min-height: 45px;
    }

    .todo > p {
        margin-top: 10px;
        font-size: 18px;
        font-weight: 200;
    }

    .delete {
        cursor: pointer;
        font-weight: 600;
    }
    .delete:hover {
        color: crimson;
    }
</style>
