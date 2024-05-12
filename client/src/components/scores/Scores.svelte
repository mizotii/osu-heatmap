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
                <div class='accuracy'>{score.score_data.accuracy}</div>
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
                <div class='notes'>{score.score_data.notes}</div>
                <div class='max_combo'>{score.score_data.max_combo}</div>
                <div class='mods'>{score.score_data.mods}</div>
                <div class='rank'>{score.score_data.rank}</div>
                <div class='total_score'>{score.score_data.score}</div>
                <div class='version'>{score.beatmap_data.version}</div>
                <div class='artist'>{score.beatmapset_data.artist}</div>
                <div class='creator'>{score.beatmapset_data.creator}</div>
                <div class='title'>{score.beatmapset_data.title}</div>
            </div>
        {/each}
    {/if}
</scores>

<style>
    .score {
        position: relative;
        text-align: center;
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
        position: absolute;
    }

    .total_score {
        position: absolute;
    }

    .version {
        position: absolute;
    }

    .artist {
        position: absolute;
    }

    .creator {
        position: absolute;
    }

    .title {
        position: absolute;
        top: 8px;
        left: 8px;
    }
</style>