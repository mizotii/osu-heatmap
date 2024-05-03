import FlexSearch from 'flexsearch'

let usersIndex: FlexSearch.Index
let users: any[]

export function createUsersIndex(data: any[]) {
    usersIndex = new FlexSearch.Index({ tokenize: 'forward' })

    data.forEach((user, i) => {
        const item = `${user.username}`
        usersIndex.add(i, item)
    })

    users = data
}

export function searchUsersIndex(searchTerm: string) {
    // escape special regex
    const match = searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const results = usersIndex.search(match)

    return results
        .map(index => users[index as number])
        .map(({ username, id }) => {
            return { username, id }
        })
}