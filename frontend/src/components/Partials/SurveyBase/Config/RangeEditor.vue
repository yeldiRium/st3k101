<template>
    <div class="range-editor">
        <div class="range-editor__config">
            <label>
                start
                <input class="range-editor__input"
                       type="number"
                       name="start"
                       min="0"
                       :max="value.end - 1"
                       step="1"
                       :value="value.start"
                       @input="updateStart"
                >
            </label>
            <label>
                end
                <input class="range-editor__input"
                       type="number"
                       name="end"
                       :min="value.start + 1"
                       step="1"
                       :value="value.end"
                       @input="updateEnd"
                >
            </label>
        </div>
        <div class="range-editor__preview">
            <EditableText :value="value.startLabel"
                          :edit-left="true"
                          @input="updateStartLabel"
                          class="range-editor__preview__label"
            >
            </EditableText>
            <RangeSVG :range="value"
                      :preview="true"
                      :showLabels="false"
                      class="range-editor__preview__range"
            />
            <EditableText :value="value.endLabel"
                          @input="updateEndLabel"
                          class="range-editor__preview__label"
            >
            </EditableText>
        </div>
    </div>
</template>

<script>
import RangeSVG from "./RangeSVG";

import Range from "../../../../model/SurveyBase/Config/Range";
import EditableText from "../../Form/EditableText";

export default {
  name: "RangeEditor",
  components: {
    EditableText,
    RangeSVG
  },
  props: {
    /** @type {Range} */
    value: {
      type: Range
    }
  },
  methods: {
    updateStart(event) {
      this.$emit(
        "input",
        new Range({
          start: Number(event.target.value),
          end: this.value.end,
          startLabel: this.value.startLabel,
          endLabel: this.value.endLabel
        })
      );
    },
    updateEnd(event) {
      this.$emit(
        "input",
        new Range({
          start: this.value.start,
          end: Number(event.target.value),
          startLabel: this.value.startLabel,
          endLabel: this.value.endLabel
        })
      );
    },
    updateStartLabel(value) {
      this.$emit(
        "input",
        new Range({
          start: this.value.start,
          end: this.value.end,
          startLabel: value,
          endLabel: this.value.endLabel
        })
      );
    },
    updateEndLabel(value) {
      this.$emit(
        "input",
        new Range({
          start: this.value.start,
          end: this.value.end,
          startLabel: this.value.startLabel,
          endLabel: value
        })
      );
    }
  }
};
</script>

<style lang="scss">
@import "../../../scss/_variables";

.range-editor {
  display: grid;
  justify-items: center;

  &__input {
    width: 3em;
  }

  &__preview {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    &__label {
      flex-basis: 10%;
    }

    &__range {
      flex-basis: 80%;
    }
  }
}
</style>
