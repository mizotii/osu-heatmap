<script>
    import Osu from "./rulesets/Osu.svelte";
    import Taiko from "./rulesets/Taiko.svelte";
    import Catch from "./rulesets/Catch.svelte";
    import Mania from "./rulesets/Mania.svelte";

    export let id;
</script>

<Osu id={id}/>
<Taiko id={id}/>
<Catch id={id}/>
<Mania id={id}/>

<style>
    
</style>