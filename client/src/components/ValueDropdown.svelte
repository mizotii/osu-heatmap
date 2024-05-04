<script>
    import { onMount } from "svelte"; 
    export let selectedValue;

    function logStuff() {
        console.log(selectedValue);
    }

    onMount (() => {
    })
</script>

<select class="select select-bordered w-full max-w-xs" bind:value={selectedValue} on:change={logStuff}>
    <option value='note_count'>note count</option>
    <option value='play_count'>play count</option>
    <option value='play_time'>play time</option>
    <option value='ranked_score'>ranked score</option>
    <option value='total_score'>total score</option>
  </select>

<style>
    
</style>