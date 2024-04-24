<script>
    import { onMount, onDestroy } from "svelte";
    import { isUserValid } from "../stores/profile";
    import CalHeatmap from "cal-heatmap";
    import Tooltip from "cal-heatmap/plugins/Tooltip";

    export let id;

    const cal = new CalHeatmap();

    let username;
    let rank;
    let scores = [];
    let heatmap_data = [];

    async function fetchProfile() {
        if (id) {
            const response = await fetch(`/api/profile/${id}`);
            const data = await response.json();
            for (const point of data.HEATMAP_DATA) {
                point.date = (new Date(point.date));
            }
            username = data.USERNAME;
            rank = data.GLOBAL_RANK;
            scores = data.SCORES;
            heatmap_data = data.HEATMAP_DATA;
        }
    }

    onMount (async () => {
        await fetchProfile();
        console.log(heatmap_data);
        cal.paint(
            {
                data: {
                    source: heatmap_data,
                    x: 'date',
                    y: 'value',
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
                        text: function (date, value, dayjsDate) {
                            return (
                                (value ? value : 'No') +
                                ' circles clicked on ' +
                                dayjsDate.format('YYYY-MM-DD HH:mm:ss')
                            );
                        }
                    },
                ],
            ]
        );
    })

    onDestroy(() => {
        isUserValid.set(null);
    });
</script>

<profile>
    <img src="https://a.ppy.sh/{id}" alt="{username}'s avatar"/>
    <p>#{rank}</p>
    <p>{username}</p>
    <div id="osu-heatmap"></div>
</profile>

<style>
</style>