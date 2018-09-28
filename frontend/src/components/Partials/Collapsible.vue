<template>
    <div class="collapsible"
    >

        <div class="collapsible__header"
            v-on:click="toggleExpanded"
        >

            <span v-if="expanded"
                  class="collapsible__header__label"
            >
                Hide
                <slot name="head"></slot>
            </span>
            <span v-else
                  class="collapsible__header__label"
            >
                Show
                <slot name="head"></slot>
            </span>

            <div class="collapsible__buttons">
                <IconExpandLess class="list-item__icon"
                                v-if="expanded"
                />
                <IconExpandMore class="list-item__icon"
                                v-else
                />
            </div>
        </div>
        <div v-if="expanded"
             class="collapsible__body"
        >
            <slot name="body"></slot>
        </div>
    </div>
</template>

<slot name="header"></slot>

<script>
import IconExpandLess from "../../assets/icons/baseline-expand_less-24px.svg";
import IconExpandMore from "../../assets/icons/baseline-expand_more-24px.svg";

export default {
  name: "Collapsible",
  components: {
    IconExpandLess,
    IconExpandMore
  },
  props: {
    startExpanded: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      expanded: false
    };
  },
  methods: {
    toggleExpanded() {
      this.expanded = !this.expanded;
    }
  },
  created() {
    this.expanded = this.startExpanded;
  }
};
</script>

<style lang="scss">
@import "../scss/variables";

.collapsible {
  grid-column: 1 / span 2;

  display: flex;
  flex-flow: column;

  border: 1px solid $primary;
  width: 100%;

  &--no-border {
    border: 0;
  }

  &--border-top {
    border-top: $primary 1px solid;
  }

  &--primary-light {
    background: $primary-light;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: $primary;

    &__label {
      margin-left: 1em;
    }
  }

  &__body {
    padding: 1em;
    border-top: $primary 1px solid;
  }

  &__buttons {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-right: 1em;
  }

  &__content {
    grid-column: 1 / span 2;
  }
}
</style>
