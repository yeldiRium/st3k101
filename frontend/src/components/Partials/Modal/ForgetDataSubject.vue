<template>
    <modal name="modal-forget-datasubject"
           height="auto"
           width="80%"
           @before-open="beforeOpen"
           :scrollable="true"
    >
        <div class="container">
            <span class="container__header">Forget DataSubject</span>
            <div class="container__body">
                <FuzzySearchableList :keys="searchableKeys"
                                     :displayOnlyKeys="displayOnlyKeys"
                                     :items="shownDataSubjects"
                                     :focusOnOpen="true"
                                     @input="onSearchStringChanged"
                                     @item-clicked="forget"
                ></FuzzySearchableList>
                <p v-if="searchString.length < fetchAfter">
                    Please type at least {{fetchAfter}} characters to begin the search.
                </p>
                <p v-else-if="dataSubjects.length === 0">
                    No DataSubjects match your query.
                </p>
            </div>
            <div class="container__footer">
                <Button @action="dismiss">Cancel</Button>
            </div>
        </div>
    </modal>
</template>

<script>
import FuzzySearchableList from "../List/FuzzySearchableList";
import * as R from "ramda";
import { fetchDataSubjectsByQuery } from "../../../api/DataSubject";
import { mapState } from "vuex-fluture";
import Button from "../Form/Button";

export default {
  name: "ForgetDataSubject",
  components: { Button, FuzzySearchableList },
  props: {
    fetchAfter: {
      type: Number,
      default: 3
    }
  },
  data() {
    return {
      dataSubjects: [],
      searchableKeys: [
        { key: "email", display: "Email" },
        { key: "moodleUsername", display: "External username" }
      ],
      displayOnlyKeys: [{ key: "ltiUserId", display: "External user id" }],
      cancelQueryFuture: null,
      handler: null,
      searchString: "",
      state: "init"
    };
  },
  computed: {
    ...mapState("session", ["sessionToken"]),
    shownDataSubjects() {
      return this.searchString.length >= this.fetchAfter
        ? this.dataSubjects
        : [];
    }
  },
  methods: {
    beforeOpen({ params: { handler } }) {
      if (R.isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      this.dataSubjects = [];
      this.searchString = "";
      this.handler = handler;
    },
    hasPrefixChanged(oldValue, newValue) {
      return (
        newValue.length >= oldValue.length && !newValue.startsWith(oldValue)
      );
    },
    doFetch(searchString) {
      if (!R.isNil(this.cancelQueryFuture)) {
        this.cancelQueryFuture();
      }
      this.cancelQueryFuture = this.fetchDataSubjectsByQuery(searchString).fork(
        this.$handleApiError,
        dataSubjects => {
          this.dataSubjects = dataSubjects;
          this.state = "hasFetched";
        }
      );
    },
    onSearchStringChanged(searchString) {
      switch (this.state) {
        case "init":
          if (searchString.length === this.fetchAfter) {
            this.doFetch(searchString);
          }
          break;
        case "hasFetched":
          if (searchString.length < this.fetchAfter) {
            this.state = "init";
            this.dataSubjects = [];
          }
          if (
            this.hasPrefixChanged(this.searchString, searchString) &&
            searchString.length >= this.fetchAfter
          ) {
            this.doFetch(searchString);
          }
          break;
      }
      this.searchString = searchString;
    },
    fuzzify: R.pipe(
      R.split(" "),
      R.map(word => `%${word}%`),
      R.join(" ")
    ),
    fetchDataSubjectsByQuery(searchString) {
      return fetchDataSubjectsByQuery(this.sessionToken, {
        email: this.fuzzify(searchString),
        moodleUsername: this.fuzzify(searchString)
      });
    },
    forget(dataSubject) {
      this.dismiss();
      this.handler({ dataSubject });
    },
    dismiss() {
      this.$modal.hide("modal-forget-datasubject");
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../scss/_variables";
.container {
  display: grid;
  grid-template-rows: 2em auto 2em;
  grid-row-gap: 10px;

  &__header {
    background-color: $primary;
    color: white;
    font-weight: bold;
    text-align: center;
  }

  &__body {
    padding-left: 20px;
    padding-right: 20px;

    > * {
      margin-bottom: 10px;
    }
  }
}
</style>
