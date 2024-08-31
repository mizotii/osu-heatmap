<script>
    import Content from "../components/Content.svelte";
    import { onMount } from "svelte";

    let loaded = false;

    onMount(() => {
        loaded = true;
    })
</script>

<Content>
    <article class="prose max-w-none">
        <h2 class='text-center'>osu-heatmap! - A personal statistic tracker for osu!</h2>
        <h3>What is this?</h3>
        <p>osu-heatmap! is nothing more than a calendar heatmap which allows you to visualize the efforts you put into the game. It does so in a manner that we hope you find motivating or more meaningful than a simple playcount graph!</p>
        <h3>What does it look like?</h3>
        <p>As of now, it looks something like this.</p>
        <img src='/static/demo.png' alt='osu-heatmap demo' width='600'>
        <p>We also plan on adding customizable themes and BBCode signatures that you can add to your osu! profiles in the future!</p>
        <h3>OK, cool. Sign me up!</h3>
        <p>All you have to do is authorize yourself by clicking the avatar in the top left corner, and we take care of the rest. Users are queued frequently enough that you should be able to see your gameplay logged in close to real time.</p>
    </article>
</Content>

<style>
    
</style>