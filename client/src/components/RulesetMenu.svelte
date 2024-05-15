<script>
    import Osu from "./rulesets/Osu.svelte";
    import Taiko from "./rulesets/Taiko.svelte";
    import Catch from "./rulesets/Catch.svelte";
    import Mania from "./rulesets/Mania.svelte";

    export let id;
</script>

<rulesets>
    <Osu id={id}/>
    <Taiko id={id}/>
    <Catch id={id}/>
    <Mania id={id}/>
</rulesets>

<style>
    rulesets {
        display: flex;
        flex-direction: row;
    }
    
</style>