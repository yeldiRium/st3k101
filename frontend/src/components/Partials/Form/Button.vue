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
        <div class="button__content">
            <slot></slot>
        </div>
        <svg class="button__ripple"
             ref="ripple"
             version="1.1"
             xmlns="http://www.w3.org/2000/svg"
        >
            <circle class="button__ripple-circle"
                    ref="circle"
                    r="1"
                    x="0"
                    y="0"
            />
        </svg>
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
    rippleAnimation(event) {
      // Can only ripple, if the event's target has a bounding box.
      if (typeof event.target.getBoundingClientRect !== "function") {
        return;
      }

      const timing = 0.75;
      const tl = new TimelineMax();

      const buttonBoundingBox = event.target.getBoundingClientRect();
      const w = buttonBoundingBox.width;
      const h = buttonBoundingBox.height;
      const x = "offsetX" in event ? event.offsetX : w / 2;
      const y = "offsetY" in event ? event.offsetY : h / 2;

      const offsetX = Math.abs(w / 2 - x);
      const offsetY = Math.abs(h / 2 - y);
      const deltaX = w / 2 + offsetX;
      const deltaY = h / 2 + offsetY;
      const scale_ratio = Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));

      tl.fromTo(
        this.$refs.circle,
        timing,
        {
          x: x,
          y: y,
          transformOrigin: "50% 50%",
          scale: 0,
          opacity: 1,
          ease: Linear.easeIn
        },
        {
          scale: scale_ratio,
          opacity: 0
        }
      );
    }
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

  display: grid;
  grid-template-areas: "content";
  grid-template-columns: fit-content(0px);

  &:focus {
    border-color: $button-focus-color;
  }

  &__content {
    grid-area: content;
    min-height: 1em;

    text-align: center;
    padding: 0.3em 0.5em 0.3em 0.5em;

    white-space: nowrap;
  }

  &__ripple {
    grid-area: content;

    width: 100%;
    height: 100%;

    pointer-events: none;

    &-circle {
      fill: $button-ripple-color;
      opacity: 0;
    }
  }

  &--grey {
    background-color: $slightlylight;

    &:focus {
      border-color: $slightlydark;
    }

    .button__ripple-circle {
      fill: $slightlydark;
    }
  }
}
</style>
