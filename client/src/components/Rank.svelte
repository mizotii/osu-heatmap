<script>
    import { rank } from "../../config.json";

    export let grade;
</script>

<div>
    <p class={rank[grade]}>
        {#if grade == 'SH'}
            S
        {:else if grade == 'SSH'}
            SS
        {:else}
            {grade}
        {/if}
    </p>
</div>

<style>
</style>