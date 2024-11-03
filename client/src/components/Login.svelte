<script>
    import { onMount } from "svelte";

    const apiEndpoint = process.env.BACKEND_API;

    $: isAuthenticated = false;
    let id;
    let username;
    let avatar_url;

    let loaded = false;

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

<login>
    {#if loaded}
        {#if isAuthenticated}
            <div class="dropdown dropdown-end">
                <div tabindex="0" role="button" class="btn btn-lg btn-circle m-1 btn-outline btn-primary h-8">
                    <div class="avatar">
                        <div class="w-12 ring-primary ring-offset-2 ring-offset-base-100 rounded-full">
                            <img src="{avatar_url}" alt="{username}'s avatar" />
                        </div>
                    </div>
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
            <button class="btn btn-lg m-1 btn-circle btn-outline outline-4 btn-primary" on:click={authRedirect}>
                <div class="avatar">
                    <div class="w-12 ring-white ring-offset-2 ring-offset-base-100 rounded-full">
                        <img src="https://s.ppy.sh/a/-1" alt="default avatar" />
                    </div>
                </div>
            </button>
        {/if}
    {:else}
        <button class="btn btn-lg m-1 btn-circle btn-outline outline-4 btn-primary" disabled='disabled'>
            <div class="avatar">
                <div class="w-12 ring-white ring-offset-2 ring-offset-base-100 rounded-full">
                    <span class="loading loading-spinner loading-lg"></span>
                </div>
            </div>
        </button>
    {/if}
</login>

<style>
</style>