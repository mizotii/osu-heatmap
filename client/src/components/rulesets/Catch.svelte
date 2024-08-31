<script>
    import Base from "./Base.svelte";

    export let id;
    export let selected;

    let ruleset = 'catch';
</script>

<Base ruleset={ruleset} id={id} selected={selected}/>

<style>

</style>