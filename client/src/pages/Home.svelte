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
        <h1 class='text-center'>NOTE: THIS IS STILL IN DEVELOPMENT AND I RESET DATA PRETTY REGULARLY -- PLEASE KEEP THAT IN MIND IF YOU DO DECIDE TO PLAY AROUND ON THE SITE!</h1>
        <h2 class='text-center'>osu-heatmap! - A personal statistic tracker for osu!</h2>
        <h3>What is this?</h3>
        <p>osu-heatmap! is a calendar heatmap which allows you to visualize all the efforts you've put into the game! It does so in a manner that we hope you find motivating or more meaningful than a simple playcount graph.</p>
        <h3>What does it look like?</h3>
        <a href='https://osu-heatm.app/profile/8816844'>
            <img src='/static/demo.png' alt='osu-heatmap demo' width='600'>
        </a>
        <p>We also plan on adding customizable themes and BBCode signatures that you can add to your osu! profiles in the future!</p>
        <h3>OK, cool. Sign me up!</h3>
        <p>All you have to do is authorize yourself by clicking the avatar in the top left corner, and we take care of the rest. Users are queued frequently enough that you should be able to see your gameplay logged in close to real time.</p>
    </article>
</Content>

<style>
    
</style>