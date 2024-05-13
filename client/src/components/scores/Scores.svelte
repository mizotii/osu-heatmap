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
                <div class='note_splits'>
                    <div class='count_300'>{score.score_data.count_300}</div>
                    <div class='count_100'>{score.score_data.count_100}</div>
                    <div class='count_miss'>{score.score_data.count_miss}</div>
                    {#if ruleset != 'taiko'}
                        <div class='count_50'>{score.score_data.count_50}</div>
                    {/if}
                    {#if ruleset == 'mania'}
                        <div class='count_geki'>{score.score_data.count_geki}</div>
                        <div class='count_katu'>{score.score_data.count_katu}</div>
                    {/if}
                </div>
                <div class='notes'>{score.score_data.notes}</div>
                <div class='max_combo'>{score.score_data.max_combo}</div>
                <div class='mods'>{score.score_data.mods}</div>
                <div class='rank'>{score.score_data.rank}</div>
                <div class='total_score'>{score.score_data.score}</div>
                <div class='version'>{score.beatmap_data.version}</div>
                <div class='song_info'>
                    <div class='title'>{score.beatmapset_data.title}</div>
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
        width: 750px;
        border: solid 1px white;
        color: white;
    }

    .background {
        filter: blur(4px) brightness(50%);
    }

    .accuracy {
        position: absolute;
    }

    .count_300 {
        position: absolute;
    }

    .count_100 {
        position: absolute;
    }

    .count_50 {
        position: absolute;
    }

    .count_geki {
        position: absolute;
    }

    .count_katu {
        position: absolute;
    }

    .count_miss {
        position: absolute;
    }

    .notes {
        position: absolute;
    }

    .max_combo {
        position: absolute;
    }

    .mods {
        position: absolute;
    }

    .rank {
        font-size: 100px;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        position: absolute;
    }

    .total_score {
        position: absolute;
    }

    .version {
        position: absolute;
    }

    .song_info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        position: absolute;
        text-align: left;
        width: 50%;
        top: 8px;
        left: 8px;
        font-size: 24px;
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