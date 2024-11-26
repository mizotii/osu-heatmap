<script>
    import { onMount } from "svelte";
    import Heatmap from "../components/Heatmap.svelte";
    import RulesetMenu from "../components/RulesetMenu.svelte";
    import Content from "../components/Content.svelte";

    const apiEndpoint = process.env.BACKEND_API;

    export let id;
    export let ruleset;

    let user;
    let username;
    let userRuleset;
    let userHeatmapData;
    let userHeatmapMax;

    let playTime;

    let loaded = false;

    let isDefault = false;

    async function fetchProfile() {
        if (id) {
            let endpoint = `${apiEndpoint}/api/profile/${id}`;
            if (ruleset) {
                endpoint += `/${ruleset}`;
            } else {
                isDefault = true;
            }
            const response = await fetch(endpoint, {
                credentials: 'include',
            });
            const data = await response.json();
            console.log(data);
            user = data.user;
            userRuleset = data.user_ruleset;
            userHeatmapData = data.user_heatmap_data;
            userHeatmapMax = data.user_heatmap_max;
            username = user.username;
            if (isDefault) {
                ruleset = user.playmode;
            }
        }
    }

    function getPlayTime(value) {
        let hours = Math.floor(value / 3600);
        let minutes = Math.floor((value / 60) - (hours * 60));
        playTime = Math.floor(hours).toString() + 'h ' + minutes.toString() + 'm';
    }

    onMount(async () => {
        await fetchProfile();
        console.log(userRuleset)
        username = user.username;
        getPlayTime(userRuleset.accumulated_play_time);
        loaded = true;
    })
</script>

<Content>
    <profile class='w-full'>
        {#if loaded}
            <div class='box-border border-b container flex flex-row'>
                <div class='basis-1/3 p-4'>
                    <div class="avatar">
                        <div class="w-9/10 rounded flex-initial justify-center align-center">
                          <img src="https://a.ppy.sh/{id}" alt="{id}'s avatar" />
                        </div>
                    </div>
                    <div class='flex-initial pb-4' id='username'>{username}</div>
                </div>
                <div class='basis-2/3 p-4 text-left'>
                    <h class='font-extrabold text-xl'>
                        SINCE {user.registration_date}                        
                    </h>
                    <dl>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">play time</dt>
                        <dd class="text-sm">{playTime}</dd>
                      </div>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">play count</dt>
                        <dd class="text-sm">{userRuleset.accumulated_play_count}</dd>
                      </div>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">total hits</dt>
                        <dd class="text-sm">{userRuleset.accumulated_total_hits}</dd>
                      </div>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">ranked score</dt>
                        <dd class="text-sm">{userRuleset.accumulated_ranked_score}</dd>
                      </div>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">total score</dt>
                        <dd class="text-sm">{userRuleset.accumulated_total_score}</dd>
                      </div>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">current streak</dt>
                        <dd class="text-sm">{userRuleset.streak_current}</dd>
                      </div>
                      <div class="py-1 grid grid-cols-2 gap-x-1">
                        <dt class="text-sm">longest streak</dt>
                        <dd class="text-sm">{userRuleset.streak_longest}</dd>
                      </div>
                    </dl>                 
                </div>
            </div>
            <div class='rulesets'>
                <RulesetMenu id={id} ruleset={ruleset}/>
            </div>
            <div id='heatmap'>
                <Heatmap heatmapData={userHeatmapData} heatmapMax={userHeatmapMax} id={id} ruleset={ruleset}/>
            </div>
        {:else}
            <img src="https://s.ppy.sh/a/-1" alt="default avatar" width='200' height='200'/>
            <div id='username'>
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

    #heatmap {
        margin: 12px;
    }

    .rulesets {
        margin: 12px;
    }

    #username {
        color: white;
        font-weight: 500;
        font-size: 32px;
    }
</style>