<script>
  import { navigate } from "svelte-routing";

    export let id;
    export let ruleset;

    function navigateToRuleset(ruleset) {
        navigate(`/profile/${id}/${ruleset}`)
    }
</script>

<button class='button' on:click={navigateToRuleset(ruleset)}>
    <img src='static/mode-{ruleset}.png' alt={ruleset} width='32' height='32'>
</button>

<style>

</style>