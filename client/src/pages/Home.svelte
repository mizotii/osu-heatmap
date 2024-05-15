<script>
    import Authorize from "../components/Authorize.svelte";
    import Search from "../components/Search.svelte";
    import DeleteExpiredTokens from "../components/admin/DeleteExpiredTokens.svelte";
    import QueueDailies from "../components/admin/QueueDailies.svelte";
</script>

<Authorize />
<Search />
<DeleteExpiredTokens />
<QueueDailies />

<style>

</style>