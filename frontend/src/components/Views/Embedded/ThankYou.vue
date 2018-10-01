<template>
    <div>
        <div class="heading">
            <h1>Thank you! 🎉</h1>
            <p>Your submission has been saved.</p>
        </div>
        <hr/>
        <div class="container">
            <div v-if="schedule !== null && schedule !== undefined">
                You may retake this survey before {{schedule.end.toLocaleDateString()}}
            </div>
            <div v-for="notice in notices"
                 :key="notice"
            >
                {{notice}}
            </div>
        </div>
        <span>Survey created with <b>st3k101</b></span>
    </div>
</template>

<script>
import Button from "../../Partials/Form/Button";
export default {
  name: "ThankYou",
  components: { Button },
  props: {
    schedule: {
      type: Object,
      default: null
    },
    notices: {
      type: Array,
      default: () => []
    }
  }
};
</script>

<style scoped lang="scss">
@import "../../scss/variables";

.container > div {
  margin-left: 12%;
  margin-right: 12%;
  margin-top: 2em;

  padding: 1em;
  border-left: $primary 2px solid;
}

.heading {
  margin: 10% 12% 2em;
}

hr {
  border: $primary 10px solid;
}

span {
  position: absolute;
  bottom: 0;
  right: 0;
  margin: 1em;
  font-size: xx-small;
}
</style>
