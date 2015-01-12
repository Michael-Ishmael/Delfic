'use strict';

var services = angular.module('delfic.services',
    ['ngResource']);

services.factory('Company', ['$resource',
    function ($resource) {
        return $resource('http://127.0.0.1\\:8000/company/:id', {id: '@id'});
    }]);

services.factory('MultiCompanyLoader', ['Company', '$q',
    function (Company, $q) {
        return function () {
            var delay = $q.defer();
            Company.query(function (companies) {
                delay.resolve(companies);
            }, function () {
                delay.reject('Unable to fetch companies');
            });
            return delay.promise;
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
    function(Company, $q){

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

services.factory('CompanyWebsiteLocator', function ($http, $q){

        var service = {};

        service.getWebsiteUrl = function(registeredNumber){

            var delay = $q.defer();

            $http.get('http://127.0.0.1:8000/company/' + registeredNumber + '/website')
                .success(function(data, status, headers, config) {
                    delay.resolve(data.url)
                }).
                error(function(data, status, headers, config) {
                    delay.reject('Unable to fetch website for company ' + registeredNumber);
                });

            return delay.promise;
        };

        service.getWebsiteMeta = function(url){

            var delay = $q.defer();

            $http.get('http://127.0.0.1:8000/getwebsitemeta/?url=' + url)
                .success(function(data, status, headers, config) {
                    if(data.success){
                        delay.resolve(data.tags)
                    } else {
                        delay.reject('No website found at: ' + url);
                    }

                }).
                error(function(data, status, headers, config) {
                    delay.reject('Unable to fetch links for website: ' + url);
                });

            return delay.promise;

        };

        service.getWebsiteLinks = function(url){

            var delay = $q.defer();

            $http.get('http://127.0.0.1:8000/findcompanylinks/?url=' + url)
                .success(function(data, status, headers, config) {
                    if(data.success){
                        delay.resolve(data.links)
                    } else {
                        delay.reject('No website found at: ' + url);
                    }
                }).
                error(function(data, status, headers, config) {
                    delay.reject('Unable to fetch links for website: ' + url);
                });

            return delay.promise;

        };

        service.getCalaisTags = function (url) {

            var delay = $q.defer();

            $http.get('http://127.0.0.1:8000/getcalaistags?url=' + url)
                .success(function(data, status, headers, config) {
                    if(data.success){
                        delay.resolve(data.links)
                    } else {
                        delay.reject('No website found at: ' + url);
                    }
                }).
                error(function(data, status, headers, config) {
                    delay.reject('Unable to fetch links for website: ' + url);
                });

            return delay.promise;

        };

        return service;

    });

services.factory('CompanyPageResults', function ($http, $q){

    var service = {};

    service.getCalaisTags = function (url) {

        var delay = $q.defer();

        $http.get('http://127.0.0.1:8000/getcalaistags/?url=' + url)
            .success(function(data, status, headers, config) {
                if(data.success){
                    delay.resolve(data)
                } else {
                    delay.reject('No OpenCalais results found for page: ' + url);
                }
            }).
            error(function(data, status, headers, config) {
                delay.reject('Unable to fetch OpenCalais results for page: ' + url);
            });

        return delay.promise;

    };

    service.getPageText = function(url){

        var delay = $q.defer();

        $http.get('http://127.0.0.1:8000/getwebsitemeta/?url=' + url)
            .success(function(data, status, headers, config) {
                if(data.success){
                    delay.resolve(data.tags)
                } else {
                    delay.reject('No website found at: ' + url);
                }

            }).
            error(function(data, status, headers, config) {
                delay.reject('Unable to fetch links for website: ' + url);
            });

        return delay.promise;

    };


    return service;

});