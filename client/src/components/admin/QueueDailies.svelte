<script>
    const apiEndpoint = process.env.BACKEND_API;
    
    async function queueDailies() {
        try {
            await fetch(`${apiEndpoint}/queue_dailies`);
        } catch (error) {
            console.error('error: ', error);
        }
    }
</script>

<deleteexpiredtokens>
    <button on:click={queueDailies}>queue dailies</button>
</deleteexpiredtokens>

<style>

</style>