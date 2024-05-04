<script>
    export let selectedValue = 'note_count';

    function selectValue(value) {
        selectedValue = value;
        console.log(selectedValue)
    }
</script>

<details class="dropdown">
    <summary class="m-1 btn">display...</summary>
    <ul class="p-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-52">
      <li><btn on:click={() => selectValue('note_count')}>note count</btn></li>
      <li><btn on:click={() => selectValue('play_count')}>play count</btn></li>
      <li><btn on:click={() => selectValue('play_time')}>play time</btn></li>
      <li><btn on:click={() => selectValue('ranked_score')}>ranked score</btn></li>
      <li><btn on:click={() => selectValue('total_score')}>total score</btn></li>
    </ul>
</details>

<style>
    
</style>