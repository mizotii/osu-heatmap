<script>
    import { onMount } from "svelte";

    const apiEndpoint = process.env.BACKEND_API;

    $: isAuthenticated = false;
    let username;
    let avatar_url;

    async function fetchUser() {
        const response = await fetch(`${apiEndpoint}/api/get_user_data`);
        const data = await response.json();
        username = data['username'];
        avatar_url = data['avatar_url'];
    }

    async function authRedirect() {
        try {
            const response = await fetch(`${apiEndpoint}/authorize`);
            const data = await response.json();
            window.location.href = data;
        } catch (error) {
            console.error('error:', error);
        }
    }

    async function logout() {
        try {
            const response = await fetch(`${apiEndpoint}/logout`);
            // don't think i need this?
            const data = await response.json();
        } catch (error) {
            console.error('error:', error);
        }
        isAuthenticated = false;
    }

    onMount(() => {
        fetch(`${apiEndpoint}/api/get_session`, {
        })
        .then((response) => response.json())
        .then((data) => {
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
    });


</script>

<login>
    {#if isAuthenticated}
        <details class="dropdown">
            <summary class="btn btn-outline">
                <img class="default" src="{avatar_url}" alt="default avatar">
                {username}
            </summary>
            <ul class="menu dropdown-content bg-base-100 rounded-box z-[1] w-52 p-2 shadow">
                <button class="btn btn-outline" on:click={logout}>log out</button>
            </ul>
        </details>
    {:else}
        <button class="btn btn-outline" on:click={authRedirect}>
            <img class="default" src="https://s.ppy.sh/a/-1" alt="default avatar">
            log in with osu!
        </button>
    {/if}
</login>

<style>
    .default {
        position: relative;
        max-width: 15%;
    }
</style>