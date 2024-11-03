<script>
    import Base from "./Base.svelte";

    export let id;
    export let selected;

    let ruleset = 'osu';
</script>

<Base ruleset={ruleset} id={id} selected={selected}/>

<style>

</style>