<script>
    async function deleteExpiredTokens() {
        try {
            await fetch('/delete_expired_tokens');
        } catch (error) {
            console.error('error: ', error);
        }
    }
</script>

<deleteexpiredtokens>
    <button on:click={deleteExpiredTokens}>delete expired tokens</button>
</deleteexpiredtokens>

<style>

</style>