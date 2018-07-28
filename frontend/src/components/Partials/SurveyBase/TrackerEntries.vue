<template>
    <Collapsible>
        <span slot="head">edit history</span>
        <div slot="body"
             class="tracker-entries">
            <TrackerEntry v-for="trackerEntry in trackerEntriesByItemHref"
                  :key="trackerEntry.timestamp.getTime().toString().concat('_te')"
                  :trackerEntry="trackerEntry"
                          :all="all"
            />
        </div>
    </Collapsible>
</template>

<script>
    import {mapGetters} from "vuex-fluture";

    import {SurveyBase} from "../../../model/SurveyBase/SurveyBase";

    import Collapsible from "../Collapsible";
    import TrackerEntry from "./TrackerEntry";
    import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";

    export default {
        name: "TrackerEntries",
        components: {
            Collapsible,
            IconExpandLess,
            IconExpandMore,
            TrackerEntry
        },
        computed: {
            ...mapGetters("trackerEntries", ["myTrackerEntries"]),
            trackerEntriesByItemHref() {
                if (this.all) {
                    return this.myTrackerEntries
                }
                return this.myTrackerEntries.filter(
                    e =>  e.itemHref === this.surveyBase.href,
                );
            }
        },
        watch: {
            surveyBase(oldValue, newValue) {
                this.loadTrackerEntries();
            }
        },
        data() {
            return {
                trackerEntriesExpanded: false
            }
        },
        created() {
            this.loadTrackerEntries();
        },
        props: {
            surveyBase: {
                type: SurveyBase
            },
            all: {
                type: Boolean
            }
        },
        methods: {
            toggleTrackerEntriesExpanded() {
                this.trackerEntriesExpanded = !this.trackerEntriesExpanded;
            },
            loadTrackerEntries() {
                let future = null;
                if (this.all) {
                    future = this.$load(
                        this.$store.dispatch(
                            "trackerEntries/loadMyTrackerEntries"
                        )
                    )
                } else {
                    future = this.$load(
                        this.$store.dispatch(
                            "trackerEntries/loadTrackerEntriesForItemHref",
                            this.surveyBase.href
                        )
                    )
                }
                future.fork(
                    this.$handleApiError,
                    () => {
                    }
                )
            }
        }
    }
</script>

<style lang="scss">
    .tracker-entries {
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;
        justify-content: left;
    }
</style>