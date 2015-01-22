'use strict';

var services = angular.module('delfic.services',
    ['ngResource']);

services.factory('Company', ['$resource', 'WS_PREFIX',
    function ($resource, WS_PREFIX) {
        var prefix = WS_PREFIX.replace(':8', '\\:8');
        return $resource(prefix + '/company/:id', {id: '@id'});
    }]);


services.factory('MultiCompanyLoader', ['Company', '$q', '$http',
    function (Company, $q, $http) {
        return {
            list: function (top, filter) {
                var delay = $q.defer();
                var query = {};
                if (top) query.top = top;
                if (filter && filter.length && filter.length > 2) query.filter = filter;
                Company.query(query, function (companies) {
                    delay.resolve(companies);
                }, function () {
                    delay.reject('Unable to fetch companies');
                });
                return delay.promise;
            },
            clear: function(){
                var delay = $q.defer();

                $http.post(WS_PREFIX + '/upload/clearcompanies')
                    .success(function (data, status, headers, config) {
                        if (data.success) {
                            delay.resolve(data.success)
                        } else {
                            delay.reject(data.message);
                        }

                    }).
                    error(function (data, status, headers, config) {
                        delay.reject('Clear companies failed');
                    });

                return delay.promise;
            },
            add: function(company){
                var delay = $q.defer();

                $http.post(WS_PREFIX + '/upload/addcompany', company)
                    .success(function (data, status, headers, config) {
                        if (data.success) {
                            delay.resolve(data)
                        } else {
                            delay.reject(data.message);
                        }

                    }).
                    error(function (data, status, headers, config) {
                        delay.reject('Clear companies failed');
                    });

                return delay.promise;
            }
        };
    }]);

services.factory('CompanyLoader', ['Company', '$route', '$q',
    function (Company, $route, $q) {
        return function () {
            var delay = $q.defer();
            Company.get({id: $route.current.params.companyId}, function (company) {
                delay.resolve(company);
            }, function () {
                delay.reject('Unable to fetch company ' + $route.current.params.companyId);
            });
            return delay.promise;
        };
    }]);

services.factory('CompanyRepository', ['Company', '$q',
    function (Company, $q) {

        var repo = {};
        repo.companies = [];
        repo.selectedIndex = -1;

        /*getCompanies();

         function getCompanies(){
         var delay = $q.defer();
         Company.query(function (companies) {
         delay.resolve(companies);
         }, function () {
         delay.reject('Unable to fetch companies');
         });
         return delay.promise;
         }*/

        return repo;

    }
]);

services.factory('CompanyWebsiteLocator', ['$http', '$q', 'WS_PREFIX', function ($http, $q, WS_PREFIX) {

    var service = {};

    service.getWebsiteUrl = function (registeredNumber) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/company/' + registeredNumber + '/website')
            .success(function (data, status, headers, config) {
                if(data.success){
                    delay.resolve(data.url)
                } else {
                    delay.reject(data.message)
                }

            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch website for company ' + registeredNumber);
            });

        return delay.promise;
    };

    service.getWebsiteMeta = function (url) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/getwebsitemeta/?url=' + url)
            .success(function (data, status, headers, config) {
                if (data.success) {
                    delay.resolve(data.tags)
                } else {
                    delay.reject('No website found at: ' + url);
                }

            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch links for website: ' + url);
            });

        return delay.promise;

    };

    service.getWebsiteLinks = function (url) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/findcompanylinks/?url=' + url)
            .success(function (data, status, headers, config) {
                if (data.success) {
                    delay.resolve(data.links)
                } else {
                    delay.reject('No website found at: ' + url);
                }
            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch links for website: ' + url);
            });

        return delay.promise;

    };
    service.getPageText = function (url) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/getpagetext?url=' + url)
            .success(function (data, status, headers, config) {
                if (data.success) {
                    delay.resolve(data.result)
                } else {
                    delay.reject('No text found at: ' + url);
                }
            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch text for page: ' + url);
            });

        return delay.promise;

    };

    service.getCalaisTags = function (url) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/getcalaistags?url=' + url)
            .success(function (data, status, headers, config) {
                if (data.success) {
                    delay.resolve(data.links)
                } else {
                    delay.reject('No website found at: ' + url);
                }
            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch links for website: ' + url);
            });

        return delay.promise;

    };

    return service;

}]);

services.factory('CompanyPageResults', ['$http', '$q', 'WS_PREFIX', function ($http, $q, WS_PREFIX) {

    var service = {};

    service.getCalaisTags = function (url) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/getcalaistags/?url=' + url)
            .success(function (data, status, headers, config) {
                if (data.success) {
                    delay.resolve(data)
                } else {
                    delay.reject('No OpenCalais results found for page: ' + url);
                }
            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch OpenCalais results for page: ' + url);
            });

        return delay.promise;

    };

    service.getPageText = function (url) {

        var delay = $q.defer();

        $http.get(WS_PREFIX + '/getpagetext?url=' + url)
            .success(function (data, status, headers, config) {
                if (data.success) {
                    delay.resolve(data.result)
                } else {
                    delay.reject('No text found at: ' + url);
                }
            }).
            error(function (data, status, headers, config) {
                delay.reject('Unable to fetch text for page: ' + url);
            });

        return delay.promise;

    };


    return service;

}]);