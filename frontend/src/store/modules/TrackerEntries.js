import {filter} from "ramda";
import Future from "fluture";
import {fetchMyTrackerEntries, fetchTrackerEntriesByItemHref} from "../../api/TrackerEntry";
import * as R from "ramda";

const store = {
    namespaced: true,
    state: {
        myTrackerEntries: []
    },
    getters: {
        myTrackerEntries(state) {
            return state.myTrackerEntries.sort(
                (a, b) => a.timestamp - b.timestamp
            );
        },
        trackerEntriesByItemHref(state) {
            return href => filter(
                entry => entry.itemHref === href,
                filter(
                    entry => entry.itemHref !== undefined,
                    state.myTrackerEntries
                )
            )
        },
    },
    actions: {
        loadMyTrackerEntries({dispatch, commit}) {
           return fetchMyTrackerEntries()
               .chain(trackerEntries =>
                    Future((reject, resolve) => {
                            commit("replaceTrackerEntries", {trackerEntries});
                            resolve(trackerEntries);
                        }
                    )
               );
        },
        loadTrackerEntriesForItemHref({dispatch, commit}, href) {
            return fetchTrackerEntriesByItemHref(href)
                .chain(trackerEntries =>
                    Future((reject, resolve) => {
                        commit("replaceTrackerEntriesForItem", {trackerEntries, href})
                        resolve(trackerEntries);
                    })
                );
        }
    },
    mutations: {
        replaceTrackerEntries(state, {trackerEntries}) {
            state.myTrackerEntries =  trackerEntries;
        },
        replaceTrackerEntriesForItem(state, {trackerEntries, href}) {
            state.myTrackerEntries = state.myTrackerEntries.filter(
                oldEntry => oldEntry.itemHref === undefined || oldEntry.itemHref !== href
            ).concat(trackerEntries);
        }
    }

};

export default store;

export {
    store
};