<script>
    const apiEndpoint = process.env.BACKEND_API;

    async function authRedirect() {
        try {
            const response = await fetch(`${apiEndpoint}/authorize`);
            const data = await response.json();
            console.log(data);
            window.location.href = data;
        } catch (error) {
            console.error('error:', error);
        }
    }
</script>

<authorize>
    <button on:click={authRedirect}>authorize</button>
</authorize>

<style>
</style>