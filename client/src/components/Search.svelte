<script>
    import Search from "svelte-search";

    let value = "";

    async function handleSearch(username) {
        const response = await fetch(`/handle_search/${username}`);
        const data = await response.json();
        if (!data.userExists) {
            
        }
    }
</script>

<Search label="field" hideLabel bind:value on:submit={handleSearch(value)} placeholder="player" />

<style>
</style>