<script>
    import { rank } from "../../config.json";

    export let grade;
</script>

<div>
    <p class={rank[grade]}>
        {#if grade == 'SH'}
            S
        {/if}
        {#if grade == 'SSH'}
            SS
        {/if}
        {grade}
    </p>
</div>

<style>
</style>