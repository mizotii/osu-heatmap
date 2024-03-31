<script>
    import { onMount } from 'svelte';

    async function authRedirect() {
        try {
            const configData = await fetch('/config')
                .then(response => response.json());

            // debug
            console.log(configData.endpoints.AUTHORIZATION_URL);

            const url = new URL(
                configData.endpoints.AUTHORIZATION_URL
            );

            const params = {
                'client_id': configData.client_credentials.CLIENT_ID,
                'redirect_uri': configData.client_credentials.REDIRECT_URI,
                'response_type': 'code',
                'scope': 'public identify',
                'state': 'randomval',
            }
            Object.keys(params)
                .forEach(key => url.searchParams.append(key, params[key]));

            window.location.href = url;
        } catch (error) {
            console.error('Error:', error);
        }
    }
</script>

<authorize>
    <button on:click={authRedirect}>authorize</button>
</authorize>

<style>
</style>