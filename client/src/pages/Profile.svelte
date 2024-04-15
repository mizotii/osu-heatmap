<script>
    import { onMount, setContext } from "svelte";
    import { userContext } from "../contexts/UserContext.svelte";
    import { useContext } from "svelte";

    const { isUserValid } = useContext(userContext);

    let userId;
    let username;
    let rank;
    let scores = {};

    async function fetchProfile() {
        if (isUserValid) {
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
        setContext(userContext);
    });
</script>

<profile>
    <img src="https://a.ppy.sh/{userId}" alt="{username}'s avatar"/>
    <p>#{rank}</p>
</profile>

<style>
</style>