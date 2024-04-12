<script>
    import { onMount } from "svelte";

    let userId;
    let user;

    async function getUserId() {
        userId = window.location.pathname.split('/').pop()
    }

    async function fetchProfile() {
        try {
            const response = await fetch(`/profile/${userId}`);
            const data = await response.json();
            user = data.name;
        } catch (error) {
            console.log("Error:", error)
        }
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