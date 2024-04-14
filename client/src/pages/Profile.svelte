<script>
    import { onMount } from "svelte";

    let userId;
    let user;

    async function getUserId() {
        userId = window.location.pathname.split('/').pop()
    }

    onMount (async () => {
        getUserId();
        fetchProfile();
    })
</script>

<profile>
    <img src="https://a.ppy.sh/{userId}" alt="{user}'s avatar"/>
</profile>

<style>
</style>