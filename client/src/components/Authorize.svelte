<script>
    import { onMount } from 'svelte';

    let configData = {};

    async function fetchConfig() {
        try {
            const response = await fetch('/config');
            configData = await response.json();
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function authRedirect() {
        const url = new URL(
            configData.endpoints.AUTHORIZATION_URL
        );

        const params = {
            'client_id': configData.client_credentials.CLIENT_ID,
            'redirect_uri': configData.endpoints.REDIRECT_URI,
            'response_type': 'code',
            'scope': 'public identify',
            'state': 'randomval',
        }
        Object.keys(params)
            .forEach(key => url.searchParams.append(key, params[key]));

        //
        console.log(url);
        //

        window.location.href = url;
    }

    onMount(fetchConfig);
</script>

<authorize>
    <button on:click={authRedirect}>authorize</button>
</authorize>

<style>
</style>