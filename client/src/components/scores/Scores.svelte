<script>
    import { scoreNotes } from "../../../config.json";

    export let isHidden;
    export let scores;
    export let ruleset;
</script>

<scores>
    {#if !isHidden}
        {#each scores as score}
            <div class="container-lg flex-row container relative m-4 flex h-16 border border-white text-white" style={`background-image: url('${score.beatmapset_data.slimcover_2x}');`}>
                <div class='flex flex-col basis-4/5 backdrop-blur-sm backdrop-brightness-50'>
                    <div class='basis-3/5 font-bold text-lg'>
                        {score.beatmapset_data.title} [{score.beatmap_data.version}]
                    </div>
                    <div class='basis-2/5 text-[10px]'>
                        <span>{score.beatmapset_data.artist}</span>
                        <span class='text-gray-300'>
                            {score.score_data.timestamp}
                            {score.score_data.mods}
                        </span>
                    </div>
                </div>
                <div class='basis-1/5 backdrop-blur-sm backdrop-brightness-50 text-center'>
                    <div class='font-bold'>
                        score: +{score.score_data.score}
                    </div>
                    <div class='text-[16px] font-bold'>
                        {scoreNotes[ruleset]}: +{score.score_data.notes}
                    </div>
                    <div class='text-[8px]'>
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
        width: 900px;
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