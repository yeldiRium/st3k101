<template>
    <modal name="modal-use-dimension-template"
           height="auto"
           width="80%"
           @before-open="beforeOpen"
           :scrollable="true"
    >
        <div class="modal-use-dimension-template__header">
            use Dimension template
        </div>
        <div class="modal-use-dimension-template__body">
            <FuzzySearchableList :keys="searchableKeys"
                                 :items="dimensionTemplates"
                                 v-on:item-clicked="use"
            >
            </FuzzySearchableList>
            <span
                    v-if="dimensionTemplates.length === 0"
            >
                Keine Templates gefunden!
            </span>
            <Button @action="cancel">
                Cancel
            </Button>
        </div>
    </modal>
</template>

<script>
import { mapGetters } from "vuex-fluture";
import { isNil } from "ramda";

import Button from "../Form/Button";
import FuzzySearchableList from "../List/FuzzySearchableList";
import ClosableModal from "./ClosableModal";

export default {
  name: "ModalUseDimensionTemplate",
  extends: ClosableModal,
  components: {
    FuzzySearchableList,
    Button
  },
  data() {
    return {
      dimension: null,
      handler: null,
      searchableKeys: [
        { key: "name", display: "Name" },
        { key: "referenceId", display: "xAPI Activity ID" }
      ]
    };
  },
  computed: {
    ...mapGetters("dimensions", ["dimensionTemplates"])
  },
  methods: {
    close() {
      this.cancel();
    },
    beforeOpen({ params: { handler } }) {
      if (isNil(handler)) {
        throw new Error("Parameter handler required!");
      }
      this.handler = handler;
    },
    cancel() {
      this.$modal.hide("modal-use-dimension-template");
    },
    /**
     * Emits a "dimension-create" event with all needed data to cre-
     * ate the dimension.
     */
    use(dimension) {
      this.$modal.hide("modal-use-dimension-template");
      this.handler({
        dimension
      });
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";

.modal-use-dimension-template {
  display: grid;
  grid-template-rows: 2em auto 2em;
  grid-row-gap: 10px;

  &__header {
    background-color: $primary-light;

    font-size: 1.4em;
    text-align: center;
  }

  &__body {
    padding-top: 10px;
    padding-left: 20px;
    padding-right: 20px;

    display: flex;
    flex-flow: column;
    align-items: center;

    > * {
      margin-bottom: 10px;
    }
  }
}
</style>
