<template>

    <div class="container">
        <div class="title">{{title}}</div>
        <hr/>
        <p>
            {{text}}
        </p>
        <Button @action="onClick()"
                class="start"
        >
                    Start
                </Button>
        <span>Survey created with <b>st3k101</b></span>
    </div>
</template>

<script>
import Button from "../../../Partials/Form/Button";

export default {
  name: "WelcomePage",
  components: {
    Button
  },
  props: {
    title: {
      type: String,
      default: ""
    },
    text: {
      type: String,
      default: ""
    }
  },
  methods: {
    onClick() {
      this.$emit("startClicked");
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../../scss/variables";

.container {
  grid-template-columns: [c-start] 25% [c-skip] auto [c-right] 100em [c-end];
  grid-template-rows: [r-start] 25% [r-title-end] 30% [r-skip] auto [r-footer] 2em [r-end];
}

.title {
  margin-top: 16vh;
  margin-left: 12vw;
  margin-bottom: 2vw;

  font-size: x-large;
}

hr {
  border: 10px $primary solid;
}

p {
  margin-left: 8vw;
  margin-right: 8vw;
  margin-top: 2vh;
  margin-bottom: 2vh;
  text-align: justify;
  max-width: 600px;
}

.start {
  margin-top: auto;
}

span {
  position: absolute;
  bottom: 0;
  right: 0;
  margin: 1em;
  font-size: xx-small;
}
</style>
