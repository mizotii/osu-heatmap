<script>
    import { onMount, onDestroy, afterUpdate } from "svelte";
    import { dataType, isUserValid } from "../stores/profile";
    import { navigate } from "svelte-routing";
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

    onMount(async () => {
        await fetchProfile();
        username = user.username;
    })
</script>

<profile>
    <img src="https://a.ppy.sh/{id}" alt="{id}'s avatar"/>
    <p>{username}</p>
    <RulesetMenu id={id}/>
    <Heatmap heatmapData={userHeatmapData}/>
</profile>

<style>
</style>