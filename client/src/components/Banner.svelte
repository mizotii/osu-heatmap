<script>
	import { Route, Router, Link } from 'svelte-routing';
    import Search from './Search.svelte';
    import Login from "./Login.svelte";
</script>

<banner>
    <div class="navbar bg-base-300">
        <div class="flex-1">
            <Link to='/'>
                <img src='../public/static/logo.png' alt='osu-heatmap logo' width='64' height='64'>
            </Link>
        </div>
        <div class="flex-none gap-2">
            <Search />
            <Login />
        </div>
    </div>
</banner>

<style>

</style>