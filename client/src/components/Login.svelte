<script>
    import { onMount } from "svelte";

    let isAuthenticated = false;
    let username;
    let avatar_url;

    async function fetchUser() {
        const response = await fetch(`api/get_user_data`);
        const data = await response.json();
        console.log(data);
        username = data['username'];
        avatar_url = data['avatar_url'];
    }

    async function authRedirect() {
        try {
            const response = await fetch(`/authorize`);
            const data = await response.json();
            window.location.href = data;
        } catch (error) {
            console.error('error:', error);
        }
    }

    onMount(() => {
        fetch(`/api/get_session`, {
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
            console.log(isAuthenticated);
        })
        .catch((err) => {
            console.log(err);
        });
    });


</script>

<login>
    <button class="btn btn-outline" on:click={authRedirect}>
        {#if isAuthenticated}
            <img class="default" src="{avatar_url}" alt="default avatar">
            {username}
        {:else}
            <img class="default" src="https://s.ppy.sh/a/-1" alt="default avatar">
            login with osu!
        {/if}
    </button>
</login>

<style>
    .default {
        position: relative;
        max-width: 15%;
    }
</style>