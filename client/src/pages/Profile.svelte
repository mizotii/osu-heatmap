<script>
    import { onMount, onDestroy } from "svelte";
    import { isUserValid } from "../stores/profile";
    import Heatmap from "../components/Heatmap.svelte";

    export let id;

    let username;
    let rank;
    let scores = {};

    async function fetchProfile() {
        if (id) {
            const response = await fetch(`/api/profile/${id}`);
            const data = await response.json();
            username = data.USERNAME;
            rank = data.GLOBAL_RANK;
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
    <img src="https://a.ppy.sh/{id}" alt="{username}'s avatar"/>
    <p>#{rank}</p>
    <p>{username}</p>
    <Heatmap />
</profile>

<style>
</style>