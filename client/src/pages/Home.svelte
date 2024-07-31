<script>
    import Login from "../components/Login.svelte";
    import QueueDailies from "../components/QueueDailies.svelte";
    import Search from "../components/Search.svelte";
</script>

<div class='login'>
    <Login />
</div>
<div class='search'>
    <Search />
</div>

<style>
    .login {
        position: absolute;
        top: 2.5%;
        right: 2.5%;
    }

    .search {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateY(-50%);
        transform: translateX(-50%);
    }
</style>