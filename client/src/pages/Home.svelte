<script>
    import Authorize from "../components/Authorize.svelte";
    import QueueDailies from "../components/QueueDailies.svelte";
    import Search from "../components/Search.svelte";
</script>

<div class='login'>
    <Authorize />
</div>
<Search />
<QueueDailies />

<style>
    .login {
        top: 2.5%;
        right: 2.5%;
    }
</style>