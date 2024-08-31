<script>
    import { onMount } from "svelte";
    import Heatmap from "../components/Heatmap.svelte";
    import RulesetMenu from "../components/RulesetMenu.svelte";
    import Content from "../components/Content.svelte";

    export let id;
    export let ruleset;

    let user;
    let username;
    let userRuleset;
    let userHeatmapData;
    let userHeatmapMax;

    let loaded = false;

    let isDefault = false;

    async function fetchProfile() {
        if (id) {
            let endpoint = `/api/profile/${id}`;
            if (ruleset) {
                endpoint += `/${ruleset}`;
            } else {
                isDefault = true;
            }
            const response = await fetch(endpoint);
            const data = await response.json();
            user = data.user;
            userRuleset = data.user_ruleset;
            userHeatmapData = data.user_heatmap_data;
            userHeatmapMax = data.user_heatmap_max;
            if (isDefault) {
                ruleset = user.playmode;
            }
        }
    }

    onMount(async () => {
        await fetchProfile();
        username = user.username;
        loaded = true;
    })
</script>

<Content>
    <profile>
        {#if loaded}
            <img src="https://a.ppy.sh/{id}" alt="{id}'s avatar" width='200' height='200'/>
            <div class='username'>{username}</div>
            <div class='rulesets'>
                <RulesetMenu id={id} ruleset={ruleset}/>
            </div>
            <div class='heatmap'>
                <Heatmap heatmapData={userHeatmapData} heatmapMax={userHeatmapMax} id={id} ruleset={ruleset}/>
            </div>
        {:else}
            <img src="https://s.ppy.sh/a/-1" alt="default avatar" width='200' height='200'/>
            <div class='username'>
                loading...
            </div>
            <div class='rulesets'>
                <span class="loading loading-spinner loading-md"></span>
                <span class="loading loading-spinner loading-md"></span>
                <span class="loading loading-spinner loading-md"></span>
                <span class="loading loading-spinner loading-md"></span>
            </div>
            <select class="select select-bordered w-32 max-w-xs" disabled>
                <option>loading...</option>
            </select>
            <div class='heatmap'>
                <div class="skeleton h-32 w-full"></div>
            </div>
        {/if}
    </profile>
</Content>

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