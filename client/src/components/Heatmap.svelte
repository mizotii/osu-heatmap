<script>
    import { dataType } from "../stores/profile";
    import { onMount, afterUpdate } from "svelte";
    import { heatmapCells } from "../../config.json";
    import CalHeatmap from "cal-heatmap";
    import Tooltip from "cal-heatmap/plugins/Tooltip";

    export let heatmapData;
    export let ruleset;
    
    const cal = new CalHeatmap();

    async function reloadHeatmap() {
        cal.paint(
            {
                data: {
                    source: heatmapData,
                    x: 'start_date',
                    y: $dataType,
                },
                date: {
                    start: new Date('2024-01-01')
                },
                range: 1,
                scale: {
                    color: {
                        type: 'linear',
                        scheme: 'PRGn',
                        domain: [0, 40]
                    }
                },
                domain: {
                    type: 'year',
                    label: { text: null },
                },
                subDomain: { 
                    type: 'day',
                    radius: 2
                },
                itemSelector: '#osu-heatmap',
            },
            [
                [
                    Tooltip,
                    {
                        // terrible, will refactor
                        text: function (date, value, dayjsDate) {
                            if ($dataType === 'play_time') {
                                return (
                                    Math.floor((value / 3600)).toString() +
                                    heatmapCells[$dataType]['hours'] +
                                    Math.floor((value / 60)).toString() +
                                    heatmapCells[$dataType]['minutes'] +
                                    dayjsDate.format('YYYY-MM-DD HH:mm:ss')
                                )
                            } else if ($dataType === 'note_count') {
                                console.log(ruleset)
                                return (
                                    (value ? value : 'No') +
                                    heatmapCells[$dataType][ruleset] +
                                    dayjsDate.format('YYYY-MM-DD HH:mm:ss')
                                );
                            } else {
                                return (
                                    (value ? value : 'No') +
                                    heatmapCells[$dataType] +
                                    dayjsDate.format('YYYY-MM-DD HH:mm:ss')
                                );
                            }
                        }
                    },
                ],
            ]
        );
    }

    onMount (async () => {
        await reloadHeatmap();
    })
    afterUpdate(reloadHeatmap);
</script>

<heatmap>
    <div id="osu-heatmap"></div>
    <select class="select select-bordered w-full max-w-xs" bind:value={$dataType} on:change={reloadHeatmap($dataType)}>
        <option value='note_count'>note count</option>
        <option value='play_count'>play count</option>
        <option value='play_time'>play time</option>
        <option value='ranked_score'>ranked score</option>
        <option value='total_score'>total score</option>
    </select>
</heatmap>

<style>
    
</style>