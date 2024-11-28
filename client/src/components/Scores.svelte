<script>
    import { scoreNotes } from "../../config.json";

    export let isHidden;
    export let scores;
    export let ruleset;
</script>

<scores>
    {#if !isHidden}
        {#each scores as score}
            <div class="container-lg flex-row container relative my-4 flex h-20 border border-white text-white" style={`background-image: url('${score.beatmapset_data.slimcover_2x}');`}>
                <div class='flex flex-col basis-[7%] backdrop-blur-sm backdrop-brightness-50 text-center px-2'>
                    <div class='basis-[75%] text-4xl font-bold'>
                        {score.score_data.rank}
                    </div>
                    <div class='font-bold text-xs'>
                        {score.score_data.accuracy}%
                    </div>
                    <div class='font-bold text-sm'>
                        {score.score_data.max_combo}x
                    </div>
                </div>
                <div class='flex flex-col basis-[65%] backdrop-blur-sm backdrop-brightness-50 p-2'>
                    <div class='flex flex-row basis-2/5 font-bold text-lg'>
                        {score.beatmapset_data.title} [{score.beatmap_data.version}]
                    </div>
                    <div class='flex flex-row basis-3/5 text-sm'>
                        <span>{score.beatmapset_data.artist}</span>
                        <span class='text-gray-300'>
                            {score.score_data.timestamp}
                            {score.score_data.mods}
                        </span>
                    </div>
                </div>
                <div class='basis-[28%] backdrop-blur-sm backdrop-brightness-50 text-center flex-col p-2'>
                    <div class='flex flex-row basis-3/5'>
                        <div class='text-sm font-bold px-1'>
                            score: +{score.score_data.score}
                        </div>
                        <div class='text-sm font-bold px-1'>
                            {scoreNotes[ruleset]}: +{score.score_data.notes}
                        </div>
                    </div>
                    <div class='text-[8px] mt-2'>
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
</style>