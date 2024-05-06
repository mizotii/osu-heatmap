import { writable } from 'svelte/store';

const isUserValid = writable(false);
const dataType = writable('note_count');

export { dataType, isUserValid };