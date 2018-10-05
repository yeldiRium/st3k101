<template>
    <modal name="modal-updateAllRangeLabels"
           height="auto"
           :width="width"
           @before-open="beforeOpen"
           class="modal"
           :scrollable="true"
    >
        <div class="modal__header">
            Update all range labels for dimension
        </div>
        <div class="container">
            <div v-if="rangesDiffer"
                 class="warning"
            >
                <p><b>Warning:</b> The questions in this dimension use different ranges!
                Is this on purpose?</p>
                <p><small>
                    Click on any question to show all questions with the same range.
                </small></p>
                <table cellpadding="0"
                       cellspacing="0"
                >
                    <thead>
                        <tr>
                            <th>Text</th>
                            <th>Start</th>
                            <th>Range</th>
                            <th>End</th>
                        </tr>
                    </thead>
                    <tbody class="selectable">
                        <template v-for="[range, questions] in Object.entries(uniqueRanges)"
                        >
                            <template v-if="rangeExpanded(range)">
                                <tr @click="toggleRangeExpanded(range)"
                                    v-for="question in questions"
                                    :key="question.id"
                                >
                                    <td class="highlight-left">{{question.text}}</td>
                                    <td>{{question.range.startLabel}}</td>
                                    <td>{{range}}</td>
                                    <td>{{question.range.endLabel}}</td>
                                </tr>
                            </template>
                            <tr v-else
                                @click="toggleRangeExpanded(range)"
                                class="unique-row"
                            >
                                <td>{{questions[0].text}}</td>
                                <td>{{questions[0].range.startLabel}}</td>
                                <td>{{range}}</td>
                                <td>{{questions[0].range.endLabel}}</td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>
            <div v-if="containsShadows"
                 class="warning"
            >
                <p>
                    <b>Warning:</b>
                    The dimension contains shadows! Updating the range labels will
                    only update the questions you've created yourself.
                </p>
                <p><small>
                    Below is a list of all shadows.
                </small></p>
                <table cellpadding="0"
                       cellspacing="0"
                >
                    <thead>
                        <tr>
                            <th>Text</th>
                            <th>Start</th>
                            <th>Range</th>
                            <th>End</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="thing in shadowQuestions"
                            :key="thing.href"
                        >
                            <td>{{thing.text}}</td>
                            <td>{{thing.range.startLabel}}</td>
                            <td>{{thing.range.start}} {{thing.range.end}}</td>
                            <td>{{thing.range.endLabel}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="label-editor">
                <label>
                    Start label:
                    <EditableText :value="rangeStartLabel"
                                  @input="updateStartLabel"
                                  class="label-editor__label"
                    >
                    </EditableText>
                </label>
                <label>
                    End label:
                    <EditableText :value="rangeEndLabel"
                                  @input="updateEndLabel"
                                  class="label-editor__label"
                    ></EditableText>
                </label>
            </div>
        </div>
        <div class="modal__buttons">
            <Button @action="cancel">Cancel</Button>
            <Button @action="apply">Apply</Button>
        </div>
    </modal>
</template>

<script>
import * as R from "ramda";
import EditableText from "../Form/EditableText";
import { anyTrue } from "../../../utility/functional";
import RangeSVG from "../SurveyBase/Config/RangeSVG";
import Button from "../Form/Button";

export default {
  name: "ModalUpdateAllRangeLabels",
  components: { RangeSVG, EditableText, Button },
  data() {
    return {
      dimension: null,
      rangeStartLabel: "Start Label",
      rangeEndLabel: "End Label",
      handler: null,
      expandedRanges: {},
      recomputeHack: false
    };
  },
  computed: {
    uniqueRanges() {
      if (R.isNil(this.dimension)) return {};

      const uniqueRanges = {};
      for (let question of this.dimension.questions) {
        let range = question.range;
        let rangeKey = `${range.start}-${range.end}`;
        if (!uniqueRanges[rangeKey]) {
          uniqueRanges[rangeKey] = [question];
        } else {
          uniqueRanges[rangeKey].push(question);
        }
      }
      return uniqueRanges;
    },
    rangesDiffer() {
      return Object.keys(this.uniqueRanges).length > 1;
    },
    shadowQuestions() {
      if (R.isNil(this.dimension)) return [];
      return R.filter(q => q.isShadow, this.dimension.questions);
    },
    containsShadows() {
      if (R.isNil(this.dimension)) return false;
      return anyTrue(R.map(q => q.isShadow, this.dimension.questions));
    },
    width() {
      return this.rangesDiffer ? "80%" : "50%";
    },
    rangeExpanded() {
      return range => {
        this.recomputeHack;
        if (R.isNil(this.expandedRanges[range])) {
          this.expandedRanges[range] = false;
        }
        return this.expandedRanges[range];
      };
    }
  },
  methods: {
    beforeOpen(event) {
      const { dimension, handler } = event.params;
      this.dimension = dimension;
      this.handler = handler;
    },
    cancel() {
      this.$modal.hide("modal-updateAllRangeLabels");
    },
    apply() {
      this.$modal.hide("modal-updateAllRangeLabels");
      this.handler(this.rangeStartLabel, this.rangeEndLabel);
    },
    toggleRangeExpanded(range) {
      if (this.uniqueRanges[range].length === 1) return; // don't toggle if only one element
      this.recomputeHack = !this.recomputeHack;
      if (R.isNil(this.expandedRanges[range])) {
        this.expandedRanges[range] = false;
      }
      this.expandedRanges[range] = !this.expandedRanges[range];
    },
    updateStartLabel(value) {
      this.rangeStartLabel = value;
    },
    updateEndLabel(value) {
      this.rangeEndLabel = value;
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../scss/_variables.scss";

hr {
  margin: 2em 0 2em 0;
}

.container {
  padding: 1.5em;
}

.highlight-left {
  border-left: $warning 2px solid;
  padding-left: 0.5em;
  margin-top: 1em;
}

td {
  padding: 0.5em 0 0.5em 0;
  border-bottom: $verydark 1px solid;
}

tr:last-child > td {
  border-bottom: none;
}

tbody.selectable > tr:hover {
  background-color: $warning;
}

table {
  width: 100%;
  margin: 2em 0 1em 0;
}

th {
  padding: 0.3em 1em 0.3em 1em;
  border-bottom: $warning 4px solid;
}

.label-editor {
  display: flex;
  justify-content: space-between;
  &__label {
    flex-basis: 40%;
  }
}

.warning {
  padding: 1em;
  margin: 0 0 2em 0;
  background-color: $warning-light;
  border: $warning 1px solid;
  border-radius: 10px;
}

.modal {
  display: grid;
  grid-template-rows: 2em auto 2em;
  grid-row-gap: 10px;

  &__header {
    background-color: $primary-light;

    font-size: 1.4em;
    text-align: center;
  }

  &__buttons {
    padding: 0 20px 0 20px;

    display: grid;
    grid-auto-columns: 1fr;
    grid-auto-flow: column;
    grid-column-gap: 1em;
    justify-content: center;
    > * {
      margin-bottom: 10px;
    }
  }
}
</style>
