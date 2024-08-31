<script>
    export let id;
    export let ruleset;
    export let selected;
</script>

<a class='button' href='/profile/{id}/{ruleset}'>
    {#if selected}
        <img src='../../static/selected-mode-{ruleset}.png' alt={ruleset} width='32' height='32'>
    {:else}
        <img src='../../static/mode-{ruleset}.png' alt={ruleset} width='32' height='32'>
    {/if}
</a>

<style>

</style>