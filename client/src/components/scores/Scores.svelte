<script>
    export let isHidden;
    export let scores;
    export let ruleset;
</script>

<scores>
    {#if !isHidden}
        {#each scores as score}
            <div class='score'>
                <div class='background'>
                    <img src='{score.beatmapset_data.slimcover_2x}' alt='score background'>
                </div>
                <div class='accuracy'>{score.score_data.accuracy}</div>
                <div class='note-splits'>
                    {score.score_data.count_300} / 
                    {#if ruleset == 'mania'}
                        {score.score_data.count_geki} / 
                    {/if}
                    {score.score_data.count_100} / 
                    {#if ruleset == 'mania'}
                        {score.score_data.count_katu} / 
                    {/if}
                    {#if ruleset != 'taiko'}
                        {score.score_data.count_50} / 
                    {/if}
                    {score.score_data.count_miss}
                </div>
                <div class='notes'>{score.score_data.notes}</div>
                <div class='max_combo'>{score.score_data.max_combo}</div>
                <div class='mods'>{score.score_data.mods}</div>
                <div class='total-score'>{score.score_data.score}</div>
                <div class='song-info'>
                    <div class='title'>{score.beatmapset_data.title} [{score.beatmap_data.version}]</div>
                    <div class='artist'>{score.beatmapset_data.artist}</div>
                </div>
                <div class='creator'>{score.beatmapset_data.creator}</div>
            </div>
        {/each}
    {/if}
</scores>

<style>
    .score {
        position: relative;
        text-align: center;
        margin: 12px;
        height: 50px;
        width: 750px;
        overflow: hidden;
        border: solid 1px white;
        color: white;
    }

    .background {
        filter: blur(4px) brightness(50%);
    }

    /*.accuracy {
        position: absolute;
    }*/
    
    .note-splits {
        position: absolute;
        width: 215px;
        right: 10px;
        color: white;
        font-size: 16px;
        font-weight: bold;
        top: 12.5px;
        text-align: right;
    }

    /*.notes {
        position: absolute;
    }

    .max_combo {
        position: absolute;
    }

    .mods {
        position: absolute;
    }

    .total-score {
        position: absolute;
    }*/

    .song-info {
        position: absolute;
        text-align: left;
        width: 515px;
        height: 25px;
        top: 6.5px;
        left: 10px;
        font-size: 16px;
    }

    .artist {
        font-size: 0.5em;
    }

    .creator {
        position: absolute;
    }

    .title {
        font-weight: bold;
    }

    @media only screen and (max-width: 600px) {
        .score {
            width: 90%;
            color: black;
        }
    }
</style>