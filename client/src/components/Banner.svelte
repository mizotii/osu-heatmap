<script>
	import { Route, Router, Link } from 'svelte-routing';
    import Search from './Search.svelte';
    import Login from "./Login.svelte";
</script>

<banner>
    <div class="navbar shadow-lg bg-base-300">
        <div class="flex-1">
            <Link to='/'>
                <picture>
                    <source media="(max-width: 640px)" srcset="/static/logo.png" width="64" height="64" />
                    <img src='/static/logo-desktop.png' alt='osu-heatmap logo' width='296.5' height='64' />
                </picture>
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