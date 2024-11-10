<script>
    import Overall from "./rulesets/Overall.svelte";
    import Osu from "./rulesets/Osu.svelte";
    import Taiko from "./rulesets/Taiko.svelte";
    import Catch from "./rulesets/Catch.svelte";
    import Mania from "./rulesets/Mania.svelte";

    export let id;
    export let ruleset;
</script>

<rulesets>
    {#if ruleset == 'overall'}
        <Overall id={id} selected={true}/>
    {:else}
        <Overall id={id} selected={false}/>
    {/if}
    {#if ruleset == 'osu'}
        <Osu id={id} selected={true}/>
    {:else}
        <Osu id={id} selected={false}/>
    {/if}
    {#if ruleset == 'taiko'}
        <Taiko id={id} selected={true}/>
    {:else}
        <Taiko id={id} selected={false}/>
    {/if}
    {#if ruleset == 'catch'}
        <Catch id={id} selected={true}/>
    {:else}
        <Catch id={id} selected={false}/>
    {/if}
    {#if ruleset == 'mania'}
        <Mania id={id} selected={true}/>
    {:else}
        <Mania id={id} selected={false}/>
    {/if}
</rulesets>

<style>
    rulesets {
        display: flex;
        flex-direction: row;
    }
    
</style>