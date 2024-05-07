<script>
    import { onMount, onDestroy } from "svelte";
    import { dataType, isUserValid } from "../stores/profile";
    import Heatmap from "../components/Heatmap.svelte";
    import RulesetMenu from "../components/RulesetMenu.svelte";

    export let id;
    export let ruleset;

    let user;
    let username;
    let userRuleset;
    let userHeatmapData;

    async function fetchProfile() {
        if (id) {
            let endpoint = `/api/profile/${id}`;
            if (ruleset) {
                console.log(ruleset);
                endpoint += `/${ruleset}`;
            }
            const response = await fetch(endpoint);
            const data = await response.json();
            user = data.user;
            userRuleset = data.user_ruleset;
            userHeatmapData = data.user_heatmap_data;
        }
    }

    onMount (async () => {
        console.log(userRuleset);
        await fetchProfile();
        username = user.username;
    })

    onDestroy(() => {
        isUserValid.set(null);
    });
</script>

<profile>
    <img src="https://a.ppy.sh/{id}" alt="{id}'s avatar"/>
    <p>{username} {ruleset}</p>
    <RulesetMenu id={id}/>
    <Heatmap heatmapData={userHeatmapData}/>
</profile>

<style>
</style>