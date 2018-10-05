<template>
    <div class="button"
         ref="button"
         :class="classes"
         v-on="$listeners"
         @click="action"
         @keyup.enter="action"
         @mouseover="raise"
         @mouseleave="lower"
         tabindex="0"
    >
        <div class="button__ripple js-ripple">
            <span class="button__circle"></span>
        </div>
        <slot></slot>
    </div>
</template>

<script>
import { dissoc, has } from "ramda";
import { Linear, TimelineMax } from "gsap";

/**
 * A button that is styled and supports raising elevation on mouseover.
 */
export default {
  name: "Button",
  props: {
    elevation: {
      type: Number,
      default: 0
    },
    offset: {
      type: Number,
      default: 6
    },
    /**
     * Whether a ripple effect should be shown on click.
     */
    ripple: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      elevationOffset: 0,
      circleX: 0,
      circleY: 0
    };
  },
  computed: {
    /**
     * Calculate elevation based on offset and initial elevation.
     * Maximum is 24, since elevation level are only defined up to 24.
     *
     * @returns {Number}
     */
    actualElevation() {
      return Math.min(this.elevation + this.elevationOffset, 24);
    },
    /**
     * Sets the elevation class for the button.
     * @returns {Array<String>}
     */
    classes() {
      return [`elevation-${this.actualElevation}`];
    }
  },
  methods: {
    /**
     * Executes the action associated with the Button.
     * Is often triggered by an event and thus takes one as parameter.
     *
     * @param {Event} event
     */
    action(event) {
      if (this.ripple !== false) {
        this.rippleAnimation(event);
      }

      if ("action" in this.$listeners) {
        this.$listeners.action();
      }
    },
    /**
     * Raises the button elevation offset to the predefined offset.
     */
    raise() {
      this.elevationOffset = this.offset;
    },
    /**
     * Lowers the button elevation offset to 0.
     */
    lower() {
      this.elevationOffset = 0;
    },
    /**
     * https://tympanus.net/codrops/2015/09/14/creating-material-design-ripple-effects-svg/
     *
     * @param event
     */
    rippleAnimation(event) {}
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";
@import "../../scss/_elevation";

$button-color: $primary-light;
$button-ripple-color: $primary;
$button-focus-color: $secondary;

.button {
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;

  background-color: $button-color;

  position: relative;
  display: inline-block;
  padding: 0.3em 0.5em 0.3em 0.5em;
  vertical-align: middle;
  overflow: visible;
  text-align: center;
  transition: all 0.2s ease;

  &:hover,
  &:focus {
    outline: 0;
    text-decoration: none;
  }
  &:not(:disabled) {
    cursor: pointer;
  }

  &:focus {
    border-color: $button-focus-color;
  }

  &--grey {
    background-color: $slightlylight;

    &:focus {
      border-color: $slightlydark;
    }
  }

  &__ripple {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: transparent;
  }

  &__circle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 0;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.25);
    .button__ripple.is-active & {
      animation: a-ripple 0.4s ease-in;
    }
  }
}

@keyframes a-ripple {
  0% {
    opacity: 0;
  }
  25% {
    opacity: 1;
  }
  100% {
    width: 200%;
    padding-bottom: 200%;
    opacity: 0;
  }
}
</style>
