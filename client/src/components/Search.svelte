<script>
    import { navigate } from "svelte-routing";
    import { isUserValid } from "../stores/profile";
    import Search from "svelte-search";

    let value = "";

    async function handleSearch(username) {
        const response = await fetch(`/api/search/${username}`);
        const data = await response.json();
        isUserValid.set(data.USER_FOUND);
        if (!data.USER_FOUND) {
            navigate(`/profile/${username}`);
        } else {
            navigate(`/profile/${data.USER_ID}`);
        }
    }
</script>

<Search label="field" hideLabel bind:value on:submit={handleSearch(value)} placeholder="player" />

<style>
</style>