<script>
	import { Route, Router } from 'svelte-routing';
	import { onMount } from 'svelte';

	// pages
	import Home from './pages/Home.svelte';
	import Profile from './pages/Profile.svelte';

	// components
	import Banner from './components/Banner.svelte';
	import Footer from './components/Footer.svelte';

	export let url = '';

	onMount(() => {
	})
</script>

<Router {url}>
	<div class='banner'>
		<Banner />
	</div>	
	<div>
		<Route path='/' component={Home}></Route>
		<Route path='/profile/:id/' component={Profile} let:params let:active>
			<Profile id='{params.id}' active={active}/>
		</Route>
		<Route path='/profile/:id/:ruleset' component={Profile} let:params let:active>
			<Profile id='{params.id}' ruleset='{params.ruleset}' active={active}/>
		</Route>
		<Route path='/error' component={Error}/>
	</div>
</Router>

<main>
	<Footer />
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>