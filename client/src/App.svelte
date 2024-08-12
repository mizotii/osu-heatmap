<script>
	import { Route, Router, Link } from 'svelte-routing';
	import { onMount } from 'svelte';

	// pages
  	import Home from './pages/Home.svelte';
	import Profile from './pages/Profile.svelte';

	// components
	import Login from './components/Login.svelte';
	import UserCounter from './components/UserCounter.svelte';

	export let url = '';

	onMount(() => {
	})
</script>

<Router {url}>
	<nav>
		<Link to='/'>
			<img src='/static/logo.png' alt='osu-heatmap logo' width='64' height='64'>
		</Link>
	</nav>
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
	<div class='usercounter'>
		<UserCounter />
	</div>

	<div class='login'>
		<Login />
	</div>
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

	.usercounter {
        position: absolute;
        bottom: 2.5%;
        right: 2.5%;
	}

	.login {
		position: absolute;
		top: 2.5%;
		right: 2.5%;
	}
</style>