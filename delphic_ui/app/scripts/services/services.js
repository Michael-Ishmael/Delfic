'use strict';

var services = angular.module('delfic.services',
    ['ngResource']);

services.factory('Company', ['$resource',
    function($resource) {
        return $resource('/companies/:id', {id: '@id'});
    }]);

services.factory('CompaniesLoader', ['Company', '$q',
    function(Company, $q) {
        return function() {
            var delay = $q.defer();
            Company.query(function(companies) {
                delay.resolve(companies);
            }, function() {
                delay.reject('Unable to fetch companies');
            });
            return delay.promise;
        };
    }]);

services.factory('CompanyLoader', ['Company', '$route', '$q',
    function(Company, $route, $q) {
        return function() {
            var delay = $q.defer();
            Company.get({id: $route.current.params.comnpanyId}, function(company) {
                delay.resolve(company);
            }, function() {
                delay.reject('Unable to fetch company '  + $route.current.params.comnpanyId);
            });
            return delay.promise;
        };
    }]);
