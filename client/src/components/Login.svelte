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

<login>
    <button class="btn btn-outline" on:click={authRedirect}>
        <img class="default" src="https://s.ppy.sh/a/-1" alt="default avatar">
        login with osu!
    </button>
</login>

<style>
    .default {
        position: relative;
        max-width: 15%;
    }
</style>