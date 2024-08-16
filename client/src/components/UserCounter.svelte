<script>
    import { onMount } from "svelte";

    const apiEndpoint = process.env.BACKEND_API;

    let users;

    async function getUserCount() {
        const response = await fetch(`${apiEndpoint}/api/get_user_count`, {
            credentials: 'same-origin',
        });
        const data = await response.json();
        userCountString(data.count);
    }

    function userCountString(count, suffix = 's') {
        users = `${count} user${count !== 1 ? suffix : ''} and counting!`;
    }

    onMount(async () => {
        await getUserCount();
    })
</script>

<usercounter>
    {users}
</usercounter>

<style>
    usercounter {
        font-size: 12px;
        font-style: italic;
        font-family: 'Courier New', Courier, monospace;
    }
</style>