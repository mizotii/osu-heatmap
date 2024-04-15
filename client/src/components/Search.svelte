<script>
    import { onDestroy } from "svelte";
    import { setContext } from "svelte";
    import { navigate } from "svelte-routing";
    import Search from "svelte-search";
    import { userContext } from "../contexts/UserContext.svelte";

    let value = "";
    let isUserValid;

    async function handleSearch(username) {
        const response = await fetch(`/api/search/${username}`);
        const data = await response.json();
        isUserValid = data.USER_FOUND;
        if (!isUserValid) {
            navigate(`/profile/${username}`);
        } else {
            navigate(`/profile/${data.USER_ID}`);
        }
    }

    onDestroy(() => {

    });
</script>

<Search label="field" hideLabel bind:value on:submit={handleSearch(value)} placeholder="player" />

<style>
</style>