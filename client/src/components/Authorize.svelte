<script>
    import { onMount } from 'svelte';

    async function authRedirect() {
        const authURL = await fetch('/config/endpoints/AUTHORIZATION_URL');
        const clientID = await fetch('/config/client_credentials/CLIENT_ID');
        const redirectURI = await fetch('config/endpoints/REDIRECT_URI');

        const url = new URL(
            authURL
        );

        const params = {
            'client_id': clientID,
            'redirect_uri': redirectURI,
            'response_type': 'code',
            'scope': 'public_identify',
            'state': 'randomval',
        }
        Object.keys(params)
            .forEach(key => url.searchParams.append(key, params[key]));

        window.location.href = url;
    }
</script>

<authorize>
    <button on:click={authRedirect}>authorize</button>
</authorize>

<style>
</style>