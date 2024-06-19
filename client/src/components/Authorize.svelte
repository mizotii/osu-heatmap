<script>
    async function authRedirect() {
        try {
            const response = await fetch(`/authorize`);
            const data = await response.json();
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