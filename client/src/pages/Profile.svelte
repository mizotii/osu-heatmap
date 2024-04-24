<script>
    import { onMount, onDestroy } from "svelte";
    import { isUserValid } from "../stores/profile";
    import SvelteHeatmap from 'svelte-heatmap';
    import moment from 'moment';

    export let id;

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

    function getHeatmapData() {
        return heatmap_data;
    }

    onMount (async () => {
        await fetchProfile();
        console.log(heatmap_data);
    })

    onDestroy(() => {
        isUserValid.set(null);
    });
</script>

<profile>
    <img src="https://a.ppy.sh/{id}" alt="{username}'s avatar"/>
    <p>#{rank}</p>
    <p>{username}</p>
    <div class="container">
        <SvelteHeatmap
            allowOverflow={true}
            cellGap={5}
            cellRadius={1}
            colors={['#a1dab4', '#42b6c4', '#2c7fb9', '#263494']}
            data={heatmap_data}
            dayLabelWidth={20}
            dayLabels={[]}
            emptyColor={'#808080'}
            endDate={moment().toDate()}
            fontSize={8}
            monthGap={20}
            monthLabelHeight={20}
            startDate={moment().subtract(5, 'months').toDate()}
            view={'monthly'}
         />
    </div>
</profile>

<style>
</style>