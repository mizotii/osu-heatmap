<script lang="ts">
    import { onMount } from "svelte";
    import { createUsersIndex, searchUsersIndex } from "./search"
    import { navigate } from "svelte-routing";

    let search: 'loading' | 'ready' = 'loading'
    let searchTerm = ''
    let results = []

    onMount(async() => {
        const users = await fetch(`/api/search`).then((res) => res.json())
        createUsersIndex(users)
        search = 'ready'
        console.log(users)
    })

    $: if (search === 'ready') {
        results = searchUsersIndex(searchTerm)
    }
</script>

{#if search === 'ready'}
    <div class='search'>
        <input
           bind:value={searchTerm}
           placeholder='player...'
           autocomplete='off'
           spellcheck='false'
           type='search' 
        />

        <div class='results'>
            {#if results}
                <ul>
                    {#each results as result}
                        <li>
                            <a href='/profile/{result.id}'>
                                {@html result.username}
                            </a>
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>
    </div>
{/if}

<style>
</style>