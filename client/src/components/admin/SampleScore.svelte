<script>
    const apiEndpoint = process.env.BACKEND_API;

    import Scores from "../scores/Scores.svelte";
    import { onMount } from "svelte";

    let scores = [];

    async function getSample() {
        const response = await fetch(`${apiEndpoint}/api/scores/8816844/taiko/1715731200000`);
        const data = await response.json();
        console.log(data);
        scores = data;
    }

    onMount(async () => {
        getSample();
    })
</script>

<Scores isHidden={false} scores={scores} ruleset={'taiko'}/>

<style>

</style>