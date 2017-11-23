Promise.waitAll = function (iterable) {
    return new Promise(function(resolve, reject) {
        var waitCount = 0;
        var results = [];

        function checkDone() {
            if (results.length == waitCount) {
                resolve(results);
            }
        }

        $.each(iterable, function(index, promise) {
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

angular.module('Utility', [])
    .directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if(event.which === 13) {
                    scope.$apply(function(){
                        scope.$eval(attrs.ngEnter, {'event': event});
                    });

                    event.preventDefault();
                }
            });
        };
    })
    .directive( "mwConfirmClick", [
        function( ) {
            return {
                priority: -1,
                restrict: 'A',
                scope: { confirmFunction: "&mwConfirmClick" },
                link: function( scope, element, attrs ){
                    element.bind( 'click', function( e ){
                        // message defaults to "Are you sure?"
                        var message = attrs.mwConfirmMessage ? attrs.mwConfirmMessage : "Are you sure?";
                        // confirm() requires jQuery
                        if( confirm( message ) ) {
                            scope.confirmFunction();
                        }
                    });
                }
            }
        }
    ]);
