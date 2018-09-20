<template>
    <modal name="dialog"
           height="auto"
           :width="width"
           @before-open="beforeOpen"
    >
        <div class="modal-dialog"
        >
            <div class="modal-dialog__title">
                {{ title }}
            </div>
            <div class="modal-dialog__text">
                {{ text }}
            </div>
            <div class="modal-dialog__buttons">
                <Button class="modal-dialog__button"
                        v-for="button in buttons"
                        :key="button.text"
                        @action="handle(button)"
                >
                    {{ button.text }}
                </Button>
            </div>
        </div>
    </modal>
</template>

<script>
import { mapState } from "vuex-fluture";
import {
  all,
  assoc,
  both,
  either,
  filter,
  head,
  identity,
  ifElse,
  is,
  isNil,
  map,
  pipe,
  prop,
  sum
} from "ramda";

import Button from "../Form/Button";

export default {
  name: "ModalDialog",
  components: {
    Button
  },
  data() {
    return {
      buttons: [],
      title: "",
      text: ""
    };
  },
  computed: {
    ...mapState("global", ["window"]),
    width() {
      if (this.window.width * 0.8 > 400) {
        return "400px";
      } else {
        return "80%";
      }
    }
  },
  methods: {
    beforeOpen(event) {
      let { buttons, title, text = "" } = event.params;

      buttons = this.validateButtons(buttons);

      this.buttons = buttons;
      this.title = title;
      this.text = text;
    },
    /**
     * Filters out all buttons with invalid parameters.
     *
     * Buttons must have a "text" of type String.
     * Buttons must have a "handler" of type Function or no "handler".
     * @param {Array<Object>} buttons
     * @returns {Array<Object>}
     */
    validateButtons: filter(
      both(
        pipe(
          prop("text"),
          is(String)
        ),
        pipe(
          prop("handler"),
          either(is(Function), isNil)
        )
      )
    ),
    onKeyUp() {
      // Enter key was pressed
      if (event.which == 13) {
        // take head, so that only the first button with
        // default=true is used
        const defaultButton = head(filter(prop("default"), this.buttons));
        if (!isNil(defaultButton)) {
          this.handle(defaultButton);
        }
      }
    },
    /**
     * Call the button's handler, if one exists.
     * @param button
     */
    handle(button) {
      if (!isNil(button.handler)) {
        button.handler();
      }
      this.$modal.hide("dialog");
    }
  },
  beforeMount() {
    window.addEventListener("keyup", this.onKeyUp);
  },
  beforeDestroy() {
    window.removeEventListener("keyup", this.onKeyUp);
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";

.modal-dialog {
  display: grid;
  grid-template-rows: 2em auto auto;
  grid-row-gap: 10px;

  &__title {
    background-color: $primary-light;

    font-size: 1.4em;
    text-align: center;
  }

  &__text {
    padding-left: 20px;
    padding-right: 20px;

    display: flex;
    flex-flow: column;
    align-items: center;

    > * {
      margin-bottom: 10px;
    }
  }

  &__buttons {
    padding: 0 20px 0 20px;

    display: flex;
    flex-wrap: wrap;
    //grid-auto-columns: 1fr;
    //grid-auto-flow: row;
    justify-content: space-between;
  }

  &__button {
    flex-grow: 1;
    margin: 0 0.5em 1em 0.5em;
  }
}
</style>
