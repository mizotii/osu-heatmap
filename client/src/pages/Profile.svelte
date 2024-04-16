<script>
    import { onMount, onDestroy } from "svelte";
    import { isUserValid } from "../stores/profile";

    let userId;
    let username;
    let rank;
    let scores = {};

    async function fetchProfile() {
        if (true) {
            userId = window.location.pathname.split('/').pop();
            const response = await fetch(`/api/profile/${userId}`);
            const data = response.json();
            username = data.USERNAME;
            rank = data.RANK;
            scores = data.SCORES;
        }
    }

    onMount (async () => {
        fetchProfile();
    })

    onDestroy(() => {
        isUserValid.set(null);
    });
</script>

<profile>
    <img src="https://a.ppy.sh/{userId}" alt="{username}'s avatar"/>
    <p>#{rank}</p>
</profile>

<style>
</style>