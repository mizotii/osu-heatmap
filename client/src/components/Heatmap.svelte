<script>
    import { dataType } from "../stores/profile";
    import { onMount, afterUpdate } from "svelte";
    import { heatmapCells } from "../../config.json";
    import CalHeatmap from "cal-heatmap";
    import Scores from "./Scores.svelte";
    import Tooltip from "cal-heatmap/plugins/Tooltip";

    const apiEndpoint = process.env.BACKEND_API;

    export let heatmapData;
    export let heatmapMax;
    export let id;
    export let ruleset;

    let scores = [];
    
    const cal = new CalHeatmap();

    cal.on('click', (event, timestamp, value) => {
        fetchScores(id, ruleset, timestamp);
    });

    async function fetchScores(id, ruleset, timestamp) {
        const response = await fetch(`${apiEndpoint}/api/scores/${id}/${ruleset}/${timestamp}`, {
            credentials: 'include',
        });
        const data = await response.json();
        scores = data;
        console.log(scores);
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
                        range: ['#ffefef', '#ff547e'],
                        domain: [0, heatmapMax[$dataType]],
                    },
                },
                domain: {
                    type: 'year',
                    label: { position: 'bottom' },
                },
                subDomain: { 
                    type: 'day',
                    radius: 2,
                    width: 12,
                    height: 12,
                    gutter: 3,
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
                                let hours = Math.floor(value / 3600);
                                let minutes = Math.floor((value / 60) - (hours * 60));
                                return (
                                    Math.floor(hours).toString() +
                                    heatmapCells[$dataType]['hours'] +
                                    minutes.toString() +
                                    heatmapCells[$dataType]['minutes'] +
                                    dayjsDate.format('YYYY-MM-DD HH:mm:ss')
                                )
                            } else if ($dataType === 'total_hits') {
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
        )
    }

    onMount (async () => {
        await reloadHeatmap();
    })

    afterUpdate(reloadHeatmap);
</script>

<heatmap>
    <select class="select select-bordered select-primary w-32 max-w-xs" bind:value={$dataType} on:change={reloadHeatmap($dataType)}>
        <option value='total_hits'>total hits</option>
        <option value='play_count'>play count</option>
        <option value='play_time'>play time</option>
        <option value='ranked_score'>ranked score</option>
        <option value='total_score'>total score</option>
    </select>
    <div id='cal-nav'>
        <button class="btn btn-xs btn-outline btn-primary" on:click={e => {
            e.preventDefault();
            cal.previous();
        }}>◄</button>
        <button class="btn btn-xs btn-outline btn-primary" on:click={e => {
            e.preventDefault();
            cal.next();
        }}>►</button>
    </div>
    <div class='box-border container h-auto overflow-x-auto border-8 border-[#111111]' id="osu-heatmap">
    </div>
    <div class='container'>
        <Scores isHidden={false} scores={scores} ruleset={ruleset}/>
    </div>
</heatmap>

<style>
    #cal-nav {
        margin-bottom: 12px;
    }

    heatmap {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    select {
        margin-bottom: 12px;
    }
</style>