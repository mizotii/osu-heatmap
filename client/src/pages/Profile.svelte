<script>
    import { onMount } from "svelte";
    import Heatmap from "../components/Heatmap.svelte";
    import RulesetMenu from "../components/RulesetMenu.svelte";
    import Login from "../components/Login.svelte";

    const apiEndpoint = process.env.BACKEND_API;

    export let id;
    export let ruleset;

    let username;
    let userRuleset;
    let userHeatmapData;

    async function fetchProfile() {
        if (id) {
            let endpoint = `${apiEndpoint}/api/profile/${id}`;
            if (ruleset) {
                endpoint += `/${ruleset}`;
            } else {
                // TODO: get default playmode
                ruleset = 'osu';
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

<div class='login'>
    <Login />
</div>

<profile>
    <img src="https://a.ppy.sh/{id}" alt="{id}'s avatar"/>
    <div class='username'>{username}</div>
    <div class='rulesets'>
        <RulesetMenu id={id}/>
    </div>
    <div class='heatmap'>
        <Heatmap heatmapData={userHeatmapData} id={id} ruleset={ruleset}/>
    </div>
</profile>

<style>
    profile {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    img {
        height: 200px;
        border: solid 1px white;
    }

    .heatmap {
        width: 634px;
        margin: 12px;
    }

    .rulesets {
        margin: 12px;
    }

    .username {
        color: white;
        font-weight: 500;
        font-size: 48px;
    }
</style>