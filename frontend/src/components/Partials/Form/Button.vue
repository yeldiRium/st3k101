<template>
    <div class="button"
         ref="button"
         :class="buttonClasses"
         v-on="$listeners"
         @keyup.enter="action"
         @mouseover="raise"
         @mouseleave="lower"
         tabindex="0"
    >
        <div class="button__ripple js-ripple"
             :class="rippleClasses"
             ref="ripple"
             @click="action"
        >
            <span class="button__circle"
                  :style="circleStyle"
            ></span>
        </div>
        <slot></slot>
    </div>
</template>

<script>
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
      offsetTop: 0,
      offsetLeft: 0,
      /*
       * Whether the ripple is currently moving. This is either false or a
       * timeout id.
       */
      isActive: false
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
    buttonClasses() {
      return [`elevation-${this.actualElevation}`];
    },
    /**
     * Styles for the ripple circle. Sets the ripple's centerpoint.
     */
    circleStyle() {
      return {
        top: `${this.offsetTop}px`,
        left: `${this.offsetLeft}px`
      };
    },
    rippleClasses() {
      return {
        "button__ripple--active": this.isActive
      };
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
      window.clearTimeout(this.isActive);
      this.isActive = false;

      this.$nextTick(() => {
        const buttonBoundingBox = event.target.getBoundingClientRect();
        const w = buttonBoundingBox.width;
        const h = buttonBoundingBox.height;
        this.offsetTop = "offsetY" in event ? event.offsetY : h / 2;
        this.offsetLeft = "offsetX" in event ? event.offsetX : w / 2;

        this.isActive = window.setTimeout(() => {
          this.isActive = false;
        }, 600);
      });
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

$border-thickness: 3px;
$ripple-color: rgba(255, 255, 255, 0.8);

.button {
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  border: $border-thickness solid transparent;

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
    border: $border-thickness solid $button-focus-color;
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

    &--active .button__circle {
      animation: a-ripple 0.6s ease-in;
    }
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
    background: $ripple-color;
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
    width: 400%;
    padding-bottom: 200%;
    opacity: 0;
  }
}
</style>
