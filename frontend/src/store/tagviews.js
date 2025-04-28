import { defineStore } from "pinia"

export const tagviewsStore = {
    state: () => ({
        visitedViews: [],
        cachedViews: []
    })
}