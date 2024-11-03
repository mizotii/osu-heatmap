import { writable } from 'svelte/store';

const isUserValid = writable(false);
const dataType = writable('total_hits');

export { dataType, isUserValid };