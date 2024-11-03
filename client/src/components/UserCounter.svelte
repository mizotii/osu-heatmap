<script>
    import { onMount } from "svelte";

    const apiEndpoint = process.env.BACKEND_API;

    let users;

    let loaded = false;

    async function getUserCount() {
        const response = await fetch(`${apiEndpoint}/api/get_user_count`, {
            credentials: 'include',
        });
        const data = await response.json();
        userCountString(data.count);
    }

    function userCountString(count, suffix = 's') {
        users = `${count} user${count !== 1 ? suffix : ''} and counting!`;
    }

    onMount(async () => {
        await getUserCount();
        loaded = true;
    })
</script>

<usercounter>
    {#if loaded}
        {users}
    {/if}
</usercounter>

<style>
    usercounter {
        font-size: 12px;
        font-style: italic;
        font-family: 'Courier New', Courier, monospace;
    }
</style>