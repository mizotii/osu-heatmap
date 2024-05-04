<script>
    import { onMount, onDestroy } from "svelte";
    import { isUserValid } from "../stores/profile";
    import CalHeatmap from "cal-heatmap";
    import Tooltip from "cal-heatmap/plugins/Tooltip";
    import ValueDropdown from "../components/ValueDropdown.svelte";

    export let id;

    const cal = new CalHeatmap();

    let user;
    let user_ruleset;
    let user_heatmap_data;

    let selectedValue;

    async function fetchProfile() {
        if (id) {
            console.log(id)
            const response = await fetch(`/api/profile/${id}`);
            const data = await response.json();
            user = data.user;
            user_ruleset = data.user_ruleset;
            user_heatmap_data = data.user_heatmap_data;
        }
    }

    onMount (async () => {
        await fetchProfile();
        console.log(selectedValue);
        console.log(user);
        console.log(user_ruleset);
        console.log(user_heatmap_data);
        cal.paint(
            {
                data: {
                    source: user_heatmap_data,
                    x: 'start_date',
                    y: `${selectedValue}`,
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
    <img src="https://a.ppy.sh/{id}" alt="{id}'s avatar"/>
    <p>{id}</p>
    <div id="osu-heatmap"></div>
    <ValueDropdown selectedValue={selectedValue} />
</profile>

<style>
</style>