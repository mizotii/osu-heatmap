<script>
	import { Route, Router, Link, navigate } from 'svelte-routing';
	// components
	import Authorize from './components/Authorize.svelte';
	import Search from './components/Search.svelte';

	// admin
	import DeleteExpiredTokens from './components/admin/DeleteExpiredTokens.svelte';
	import QueueDailies from './components/admin/QueueDailies.svelte';
	import SampleScore from './components/admin/SampleScore.svelte';

	//pages
	import Error from './pages/Error.svelte';
  	import Home from './pages/Home.svelte';
	import Profile from './pages/Profile.svelte';

	export let url = '';
</script>

<Router {url}>
	<nav>
		<Link to='/'>Home</Link>
		<Link to='/sampleScore'>sampleScores</Link>
	</nav>
	<div>
		<Route path='/home' component={Home}></Route>
		<Route path='/profile/:id/' component={Profile} let:params let:active>
			<Profile id='{params.id}' active={active}/>
		</Route>
		<Route path='/profile/:id/:ruleset' component={Profile} let:params let:active>
			<Profile id='{params.id}' ruleset='{params.ruleset}' active={active}/>
		</Route>
		<Route path='/error' component={Error}/>
		<Route path='/sampleScore' component={SampleScore}/>
	</div>
</Router>

<main>
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