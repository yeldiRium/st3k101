import Vue from "vue";
import Router from "vue-router";
import SurveyForSubmission from "../components/SurveyForSubmission";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/survey/:id",
      name: "SurveyForSubmission",
      component: SurveyForSubmission
    }
  ]
})