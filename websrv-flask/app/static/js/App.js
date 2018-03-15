const angular = require("angular");

const $ = jQuery = require("jquery");
require("radar-chart-d3");
require("bootstrap");
require("./Languagepicker");
require("./Surveys");
require("./Statistics");
require("./Account");
require("./API");
require("./Utility");

angular.module("App", ["Surveys", "Statistics", "Account", "API", "Utility"]);
