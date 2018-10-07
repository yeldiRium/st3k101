<template>
    <Collapsible>
        <span slot="head">edit history</span>
        <div slot="body"
             class="tracker-entries">
            <TrackerEntry v-for="trackerEntry in trackerEntriesByItemHref"
                  :key="trackerEntry.toString()"
                  :trackerEntry="trackerEntry"
                          :all="all"
            />
            <span v-if="trackerEntriesByItemHref.length === 0">
                There are no changes yet.
            </span>
        </div>
    </Collapsible>
</template>

<script>
import { mapGetters } from "vuex-fluture";

import { SurveyBase } from "../../../model/SurveyBase/SurveyBase";

import Collapsible from "../Collapsible";
import TrackerEntry from "./TrackerEntry";
import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";
import * as R from "ramda";

export default {
  name: "TrackerEntries",
  components: {
    Collapsible,
    IconExpandLess,
    IconExpandMore,
    TrackerEntry
  },
  props: {
    surveyBase: {
      type: SurveyBase
    },
    all: {
      type: Boolean
    },
    recurse: {
      type: Boolean,
      default: false
    },
    loadData: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters("trackerEntries", ["myTrackerEntries"]),
    trackerEntriesByItemHref() {
      if (this.all) {
        return this.myTrackerEntries;
      }

      if (R.isNil(this.surveyBase)) {
        return [];
      }

      let the_href = this.surveyBase.href;
      if (this.surveyBase.isShadow) {
        the_href = this.surveyBase.referenceTo.href;
      }

      let ownTrackerEntries = this.myTrackerEntries.filter(
        e => e.itemHref === the_href
      );

      if (!this.recurse) {
        return ownTrackerEntries;
      }

      let childrenTrackerEntries = R.flatten(
        R.map(
          child =>
            this.myTrackerEntries.filter(
              entry => entry.itemHref === child.href
            ),
          this.surveyBase.getAllChildren()
        )
      );
      return ownTrackerEntries.concat(childrenTrackerEntries);
    }
  },
  watch: {
    surveyBase() {
      this.loadTrackerEntries(); // TODO: this causes lots of updates
    }
  },
  data() {
    return {
      trackerEntriesExpanded: false
    };
  },
  created() {
    if (this.loadData) {
      this.loadTrackerEntries();
    }
  },
  methods: {
    toggleTrackerEntriesExpanded() {
      this.trackerEntriesExpanded = !this.trackerEntriesExpanded;
    },
    loadTrackerEntries() {
      let future = null;
      if (this.all || this.recurse) {
        future = this.$load(
          this.$store.dispatch("trackerEntries/loadMyTrackerEntries")
        );
      } else {
        future = this.$load(
          this.$store.dispatch(
            "trackerEntries/loadTrackerEntriesForItemHref",
            this.surveyBase.href
          )
        );
      }
      future.fork(this.$handleApiError, () => {});
    }
  }
};
</script>

<style lang="scss">
.tracker-entries {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: left;
}
</style>
