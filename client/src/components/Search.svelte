<script lang="ts">
    import { onMount } from "svelte";
    import { createUsersIndex, searchUsersIndex } from "./search"

    const apiEndpoint = process.env.BACKEND_API;

    let search: 'loading' | 'ready' = 'loading'
    let searchTerm = ''
    let results = []

    onMount(async() => {
        const users = await fetch(`${apiEndpoint}/api/search`).then((res) => res.json())
        createUsersIndex(users)
        search = 'ready'
    })

    $: if (search === 'ready') {
        results = searchUsersIndex(searchTerm)
    }
</script>

{#if search === 'ready'}
    <div class='search'>
        <input type="text" bind:value={searchTerm} placeholder="player..." autocomplete='off' spellcheck='false' class="input w-full max-w-xs" />

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