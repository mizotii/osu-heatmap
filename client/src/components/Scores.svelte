<script>
    import { scoreNotes } from "../../config.json";

    import SampleScore from "./SampleScore.svelte";

    export let isHidden;
    export let scores;
    export let ruleset;
</script>

<scores>
    {#if !isHidden}
        {#each scores as score}
            <div class='score'>
                <div class='img'>
                    <img src='{score.beatmapset_data.slimcover_2x}' alt='score background'>
                </div>
                <div class='top'>
                    <div class='title'>{score.beatmapset_data.title} [{score.beatmap_data.version}]</div>
                    <div class='total-score'>score: +{score.score_data.score}</div>
                </div>
                <div class='bottom'>
                    <div class='left'>
                        <div class='artist'>{score.beatmapset_data.artist}</div>
                        <div class='timestamp'>{score.score_data.timestamp}</div>
                        <div class='mods'>{score.score_data.mods}</div>
                    </div>
                </div>
                <div class='notes'>
                    <div class='total-notes'>
                        {scoreNotes[ruleset]}: +{score.score_data.notes}
                    </div>
                    <div class='note-splits'>
                        {#if ruleset == 'mania'}
                            {score.score_data.count_geki} / 
                        {/if}
                        {score.score_data.count_300} / 
                        {#if ruleset == 'mania'}
                            {score.score_data.count_katu} / 
                        {/if}
                        {score.score_data.count_100} / 
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
        position: relative;
        text-align: center;
        margin: 12px;
        height: 50px;
        width: 90%;
        overflow: hidden;
        border: solid 1px white;
        color: white;
    }

    .img {
        filter: blur(4px) brightness(33%);
    }

    .top {
        position: absolute;
        padding-top: 4px;
        left: 0%;
        top: 0%;
        height: 60%;
        width: 85%;
        font-size: 16px;
        font-weight: bold;
    }

    .top > .title {
        text-align: left;
        padding-left: 6px;
        float: left;
        left: 0%;
    }

    .top > .total-score {
        text-align: right;
        float: right;
        left: 75%;
    }

    .bottom {
        position: absolute;
        padding-bottom: 4px;
        top: 60%;
        left: 0%;
        height: 40%;
        width: 85%;
        font-size: 10px;
    }

    .bottom > .left {
        display: inline-flex;
        text-align: left;
        padding-left: 6px;
        float: left;
        left: 0%;
        width: 80%;
        gap: 6px;
    }

    .notes {
        position: absolute;
        padding-top: 4px;
        padding-bottom: 4px;
        top: 0%;
        right: 0%;
        height: 100%;
        width: 15%;
        font-size: 16px;
        text-align: center;
        font-weight: bold;
    }

    .notes > .note-splits {
        font-size: 10px;
    }

    .timestamp {
        color: grey;
    }

    @media only screen and (max-width: 600px) {
        .score {
            width: 90%;
        }
    }
</style>