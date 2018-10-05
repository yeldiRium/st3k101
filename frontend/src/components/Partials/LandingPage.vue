<template>
    <div v-if="questionnaire !== null">
        <div class="heading">
            <h1>{{questionnaire.name}}</h1>
        </div>
        <hr/>
        <div class="container">
            <p>
                This survey does not currently accept submissions. You may still view it's contents, but you won't be
                able to submit your answers.
            </p>
            <p v-for="message in messages">
                {{message}}
            </p>
            <Button @action="action">
                View survey
            </Button>
        </div>
        <span>Survey created with <b>st3k101</b></span>
    </div>
</template>

<script>
import Button from "./Form/Button";

export default {
  name: "LandingPage",
  components: { Button },
  props: {
    questionnaire: {
      type: Object,
      default: null
    }
  },
  computed: {
    messages() {
      return []; // for later displaying information about scheduling etc
    }
  },
  methods: {
    action($event) {
      this.$emit("action", $event);
    }
  }
};
</script>

<style scoped lang="scss">
@import "../scss/variables";

.container > p {
  padding: 1em;
  border-left: $primary 2px solid;
}

.container > * {
  margin-left: 12%;
  margin-right: 12%;
  margin-top: 2em;
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
