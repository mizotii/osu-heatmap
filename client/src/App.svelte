<script>
	import { Route, Router, Link, navigate } from 'svelte-routing';
	// components
	import Authorize from './components/Authorize.svelte';
	import Search from './components/Search.svelte';

	// admin
	import DeleteExpiredTokens from './components/admin/DeleteExpiredTokens.svelte';

	//pages
	import Error from './pages/Error.svelte';
	import Profile from './pages/Profile.svelte';

	export let url = '';
</script>

<Router {url}>
	<nav>
		<Link to='/'>Home</Link>
	</nav>
	<div>
		<Route path='/profile/:id' component={Profile} let:params>
			<Profile id='{params.id}' />
		</Route>
		<Route path='/error' component={Error}/>
	</div>
</Router>

<main>
	<Authorize />
	<Search />
	<DeleteExpiredTokens />
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