<script>
    async function authRedirect() {
        try {
            const response = await fetch(`/queue_dailies`);
            const data = await response.json();
            window.location.href = data;
        } catch (error) {
            console.error('error:', error);
        }
    }
</script>

<authorize>
    <button on:click={authRedirect}>queue</button>
</authorize>

<style>
</style>