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
    .factory('Locales', ['$http', function ($http) {
        return {
            query: function () {
                return $http.get('/api/locales').then(
                    function (result) {
                        return new Promise(function (resolve, reject) {
                            resolve(result.data);
                        });
                    },
                    function (error) {
                        return new Promise(function (resolve, reject) {
                            reject(error);
                        });
                    }
                );
            }
        }
    }])
    .directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if(event.which === 13) {
                    scope.$apply(function(){
                        scope.$eval(attrs.ngEnter, {'$event': event});
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
    ])
    .directive("clickGo", ['$location', function($location) {
        return function(scope, element, attrs) {
            element.bind('click', function(e) {
                $location.path(attrs.clickGo);
            })
        }
    }]);
