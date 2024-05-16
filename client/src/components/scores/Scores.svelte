<script>
    export let isHidden;
    export let scores;
    export let ruleset;
</script>

<scores>
    {#if !isHidden}
        {#each scores as score}
            <div class='score'>
                <img src='{score.beatmapset_data.slimcover_2x}' alt='score background'>
                <div class='top'>
                    <div class='title'>{score.beatmapset_data.title} [{score.beatmap_data.version}]</div>
                    <div class='total-score'>{score.score_data.score}</div>
                    <div class='notes'>{score.score_data.notes}</div>
                </div>
                <div class='bottom'>
                    <div class='artist'>{score.beatmapset_data.artist}</div>
                    <div class='timestamp'>{score.score_data.timestamp}</div>
                    <div class='mods'>{score.score_data.mods}</div>
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
                </div>
            </div>
        {/each}
    {/if}
</scores>

<style>
    .score {
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: flex-start;
        text-align: center;
        margin: 12px;
        height: 50px;
        width: 750px;
        overflow: hidden;
        border: solid 1px white;
        color: white;
        position: relative;
    }

    img {
        max-width: 100%;
        max-height: 100vh;
        filter: blur(4px) brightness(50%);
    }
    
    .top {
        height: 60%;
        width: 100%;
        display: flex;
        justify-content: space-between;
        font-weight: bold;
    }

    .bottom {
        height: 40%;
        width: 100%;
        display: flex;
        justify-content: flex-end space-between;
        font-size: 0.5em;
    }

    /*.title {
    }

    .total-score {
    }

    .notes {
    }*/
    
    .note-splits {
        color: white;
        font-size: 16px;
        text-align: right;
    }

    /*.mods {
    }*/

    .timestamp {
        margin-left: 6px;
        color: grey;
    }

    .artist {
        color: inherit;
    }

    @media only screen and (max-width: 600px) {
        .score {
            width: 90%;
            color: black;
        }
    }
</style>