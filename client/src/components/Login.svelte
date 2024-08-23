<script>
    import { onMount } from "svelte";
  import { construct_svelte_component } from "svelte/internal";

    const apiEndpoint = process.env.BACKEND_API;

    $: isAuthenticated = false;
    let id;
    let username;
    let avatar_url;

    let loaded;

    async function fetchUser() {
        const response = await fetch(`${apiEndpoint}/api/get_user_data`, {
            credentials: 'include',
        });
        const data = await response.json();
        id = data['id'];
        username = data['username'];
        avatar_url = data['avatar_url'];
    }

    async function authRedirect() {
        try {
            const response = await fetch(`${apiEndpoint}/authorize`, {
                credentials: 'include',
            });
            const data = await response.json();
            window.location.href = data;
        } catch (error) {
            console.error('error:', error);
        }
    }

    async function profileRedirect() {
        window.location.href = `/profile/${id}`;
    }

    const logout = () => {
        fetch(`${apiEndpoint}/api/logout`, {
            credentials: 'include',
        })
        .then(() => {
            isAuthenticated = false;
        })
        .catch((err) => {
            console.log(err);
        });
    };

    onMount(() => {
        fetch(`${apiEndpoint}/api/get_session`, {
            credentials: 'include',
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if (data.login == true) {
                isAuthenticated = true;
                fetchUser();
            } else {
                isAuthenticated = false;
            }
        })
        .catch((err) => {
            console.log(err);
        });
        setTimeout(() => {
            loaded = true;
        }, 1000);
    });


</script>

{#if loaded}
    <login>
        {#if isAuthenticated}
            <div class="dropdown">
                <div tabindex="0" role="button" class="btn m-1 btn-outline btn-primary min-w-16 w-64">
                    <div class="avatar">
                        <div class="w-8 ring-primary ring-offset-2 ring-offset-base-100 rounded-full">
                            <img src="{avatar_url}" alt="{username}'s avatar" />
                        </div>
                    </div>
                    {username}
                </div>
                <ul tabindex="0" class="menu dropdown-content bg-base-300 rounded-box z-[1] w-52 p-2 shadow">
                    <li>
                        <button class="btn btn-outline" on:click={profileRedirect}>profile</button>
                    </li>
                    <li>
                        <button class="btn btn-outline" on:click={logout}>log out</button>
                    </li>
                </ul>
            </div>
        {:else}
            <button class="btn m-1 btn-outline btn-primary min-w-16 w-64" on:click={authRedirect}>
                <div class="avatar">
                    <div class="w-8 ring-white ring-offset-2 ring-offset-base-100 rounded-full">
                        <img src="https://s.ppy.sh/a/-1" alt="default avatar" />
                    </div>
                </div>
                log in with osu!
            </button>
        {/if}
    </login>
{/if}

<style>
</style>