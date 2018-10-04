<template>
    <div class="authentication"
         :style="style"
    >
        <div class="authentication__login">
            <div class="authentication__title">
                Login
            </div>

            <div class="authentication__body">
                <div class="authentication__error-row"
                     v-for="error in this.errors.login"
                >
                    {{error}}
                </div>

                <div class="authentication__input-row">
                    <label for="email">
                        E-Mail:
                    </label>
                    <input v-model="inputData.email"
                           id="email"
                           type="email"
                           @keyup.enter="login"
                    />
                </div>
                <div class="authentication__input-row">
                    <label for="password">
                        Password:
                    </label>
                    <input v-model="inputData.password"
                           id="password"
                           type="password"
                           @keyup.enter="login"
                    />
                </div>
            </div>

            <div class="authentication__buttons">
                <Button :offset="3"
                        @action="login"
                >
                    Login
                </Button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState } from "vuex-fluture";
import { either, propEq, propOr } from "ramda";

import { register, requestSession } from "../../../api/Authentication";

import Button from "../../Partials/Form/Button";

import ErrorIcon from "../../../assets/icons/baseline-error-24px.svg";
import { BadRequestError, ConflictError } from "../../../api/Errors";

export default {
  name: "Authentication",
  components: {
    Button,
    ErrorIcon
  },
  data() {
    return {
      isLogin: true,

      inputData: {
        email: "",
        password: "",
        passwordConfirmation: ""
      },

      errors: {
        login: [],
        email: [],
        password: []
      }
    };
  },
  computed: {
    ...mapState("global", ["window"]),
    ...mapGetters("session", ["isLoggedIn"]),
    width() {
      if (this.window.width * 0.8 > 400) {
        return `400px`;
      }
      return `80%`;
    },
    style() {
      return {
        "grid-template-columns": `auto ${this.width} auto`
      };
    }
  },
  watch: {
    // Re-routes to the private area, if a user is already logged in
    // or after a successful login.
    isLoggedIn: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal === true) {
          this.$router.push({ name: "Dashboard" });
        }
      }
    }
  },
  methods: {
    setIsLogin(newValue) {
      this.isLogin = newValue;
    },
    clearErrors() {
      this.errors.login = [];
      this.errors.email = [];
      this.errors.password = [];
    },
    login() {
      this.clearErrors();

      this.$load(
        this.$store.dispatch("session/requestSession", {
          email: this.inputData.email,
          password: this.inputData.password
        })
      ).fork(
        error => {
          if (
            either(
              propEq("name", "NotFoundError"),
              propEq("name", "BadRequestError")
            )(error)
          ) {
            this.errors.login.push(
              "User or password is incorrect. Please try again."
            );
            this.$notify({
              type: "error",
              title: "Login error",
              text:
                "An error occured while logging in. Please check your information and try again."
            });
          } else {
            this.$handleApiError(error);
          }
        },
        () => {}
      );
    }
  }
};
</script>

<style lang="scss">
@import "../../scss/_variables";
@import "../../scss/_elevation";

.authentication {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;

  display: grid;
  grid-template-areas: ". . ." ". content ." ". . .";
  grid-template-rows: 25% auto auto;
  justify-items: center;
  align-items: start;

  &__login {
    grid-area: content;

    //border-radius: 15px;
    //padding: 15px;

    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 3em auto 3em 2em;
    grid-template-areas: "title" "body" "buttons" "bottom-link";
  }

  &__title {
    justify-self: center;
  }

  &__body {
    grid-area: body;

    padding: 0 15px 0 15px;

    display: flex;
    flex-flow: column;
  }

  &__input-row {
    margin-bottom: 8px;

    display: grid;
    grid-template-columns: 30% 60% 10%;
    align-items: center;
  }

  &__error-icon {
    transform: scale(0.8, 0.8);
    fill: $danger;
  }

  &__success-row,
  &__error-row {
    margin-bottom: 8px;
    text-decoration: underline;
  }

  &__buttons {
    grid-area: buttons;

    align-self: center;
  }

  &__bottom-link {
    grid-area: bottom-link;

    justify-self: center;
    align-self: center;
  }
}
</style>
