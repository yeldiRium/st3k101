const angular = require("angular");
const $ = require("jquery");

require("spectrum-colorpicker");

Promise.waitAll = function (iterable) {
    return new Promise(function (resolve, reject) {
        let waitCount = 0;
        const results = [];

        function checkDone() {
            if (results.length === waitCount) {
                resolve(results);
            }
        }

        $.each(iterable, function (index, promise) {
            waitCount++;
            promise.then(
                function success(result) {
                    results.push({
                        success: result
                    });
                    checkDone();
                },
                function fail(error) {
                    results.push({
                        error: error
                    });
                    checkDone();
                }
            )
        })
    });
};

angular.module("Utility", [])
    .factory("StyleStuff", function () {
        return {
            /**
             * Equalizes the heights of checkboxes with the given selectors.
             *
             * Watches, if the selectable's DOM changes and resizes the checkbox
             * if needed.
             *
             * @param checkbox
             * @param selectable
             */
            "equalizeSelectboxes": function (checkbox, selectable) {
                $(checkbox).each(function (index, element) {
                    const e = $(element);

                    function resize() {
                        e.height(e.siblings(selectable).height())
                    }

                    resize();

                    (new MutationObserver(resize))
                        .observe(e.siblings(selectable)[0], {
                            "childList": true,
                            "subtree": true
                        });
                });
            },
            /**
             * Initializes a colorpicker on the given selector with a given ini-
             * tial value.
             *
             * On change the callback is called with the color as a hexstring.
             *
             * @param initial
             * @param selector
             * @param callback
             */
            "colorPicker": function (initial, selector, callback) {
                $(selector).spectrum({
                    color: initial,
                    change: function (color) {
                        callback(color.toHexString());
                    }
                });
            }
        }
    })
    .directive("ngEnter", function () {
        return function (scope, element, attrs) {
            element.bind("keydown keypress", function (event) {
                if (event.which === 13) {
                    scope.$apply(function () {
                        scope.$eval(attrs.ngEnter, {"$event": event});
                    });

                    event.preventDefault();
                }
            });
        };
    })
    .directive("mwConfirmClick", [
        function () {
            return {
                priority: -1,
                restrict: "A",
                scope: {confirmFunction: "&mwConfirmClick"},
                link: function (scope, element, attrs) {
                    element.bind("click", function (e) {
                        // message defaults to "Are you sure?"
                        var message = attrs.mwConfirmMessage ? attrs.mwConfirmMessage : "Are you sure?";
                        // confirm() requires jQuery
                        if (confirm(message)) {
                            scope.confirmFunction();
                        }
                    });
                }
            }
        }
    ])
    .directive("clickGo", ["$location", function ($location) {
        return function (scope, element, attrs) {
            element.bind("click", function (e) {
                scope.$apply(() => {
                    $location.path(attrs.clickGo);
                });
            })
        }
    }]);
