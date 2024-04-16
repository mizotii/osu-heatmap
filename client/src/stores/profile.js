import { writable } from 'svelte/store';

const isUserValid = writable(false);

export { isUserValid };