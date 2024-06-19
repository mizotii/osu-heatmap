<script>
    import { dataType } from "../stores/profile";
    import { onMount, afterUpdate } from "svelte";
    import { heatmapCells } from "../../config.json";
    import CalHeatmap from "cal-heatmap";
    import Scores from "./scores/Scores.svelte";
    import Tooltip from "cal-heatmap/plugins/Tooltip";

    export let heatmapData;
    export let id;
    export let ruleset;

    let scores = [];
    
    const cal = new CalHeatmap();

    cal.on('click', (event, timestamp, value) => {
        fetchScores(id, ruleset, timestamp);
    });

    async function fetchScores(id, ruleset, timestamp) {
        const response = await fetch(`/api/scores/${id}/${ruleset}/${timestamp}`);
        const data = await response.json();
        scores = data;
    }

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
        console.log(heatmapData);
        await reloadHeatmap();
    })

    afterUpdate(reloadHeatmap);
</script>

<heatmap>
    <select class="select select-bordered w-full max-w-xs" bind:value={$dataType} on:change={reloadHeatmap($dataType)}>
        <option value='note_count'>note count</option>
        <option value='play_count'>play count</option>
        <option value='play_time'>play time</option>
        <option value='ranked_score'>ranked score</option>
        <option value='total_score'>total score</option>
    </select>
    <div id="osu-heatmap"></div>
    <div class='scores'>
        <Scores isHidden={false} scores={scores} ruleset={ruleset}/>
    </div>
</heatmap>

<style>
    #osu-heatmap {
        border: solid 10px white;
    }

    heatmap {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    select {
        margin: 12px;
    }
</style>