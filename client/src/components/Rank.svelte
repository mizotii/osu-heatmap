<script>
    import { rank } from "../../config.json";

    export let grade;
</script>

<div>
    <p class={rank[grade]}>
        {grade}
    </p>
</div>

<style>
</style>