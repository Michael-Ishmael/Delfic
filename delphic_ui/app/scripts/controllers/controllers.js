'use strict';

var app = angular.module('delfic',
    ['ngRoute', 'delfic.directives', 'delfic.services']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {
            controller: 'ListCtrl',
            resolve: {
                companies: ["CompaniesLoader", function(CompaniesLoader) {
                    return CompaniesLoader();
                }]
            },
            templateUrl:'/views/list.html'
        }).when('/edit/:companyId', {
            controller: 'EditCtrl',
            resolve: {
                company: ["CompanyLoader", function(CompanyLoader) {
                    return CompanyLoader();
                }]
            },
            templateUrl:'/views/companyForm.html'
        }).when('/view/:companyId', {
            controller: 'ViewCtrl',
            resolve: {
                company: ["CompanyLoader", function(CompanyLoader) {
                    return CompanyLoader();
                }]
            },
            templateUrl:'/views/viewCompany.html'
        }).when('/new', {
            controller: 'NewCtrl',
            templateUrl:'/views/companyForm.html'
        }).otherwise({redirectTo:'/'});
}]);

app.controller('ListCtrl', ['$scope', 'companies',
    function($scope, companies) {
        $scope.companies = companies;
    }]);

app.controller('ViewCtrl', ['$scope', '$location', 'company',
    function($scope, $location, company) {
        $scope.company = company;

        $scope.edit = function() {
            $location.path('/edit/' + company.id);
        };
    }]);

app.controller('EditCtrl', ['$scope', '$location', 'company',
    function($scope, $location, company) {
        $scope.company = company;

        $scope.save = function() {
            $scope.company.$save(function(company) {
                $location.path('/view/' + company.id);
            });
        };

        $scope.remove = function() {
            delete $scope.company;
            $location.path('/');
        };
    }]);

app.controller('NewCtrl', ['$scope', '$location', 'Company',
    function($scope, $location, Company) {
        $scope.company = new Company({
            ingredients: [ {} ]
        });

        $scope.save = function() {
            $scope.company.$save(function(company) {
                $location.path('/view/' + company.id);
            });
        };
    }]);

app.controller('IngredientsCtrl', ['$scope',
    function($scope) {
        $scope.addIngredient = function() {
            var ingredients = $scope.company.ingredients;
            ingredients[ingredients.length] = {};
        };
        $scope.removeIngredient = function(index) {
            $scope.company.ingredients.splice(index, 1);
        };
    }]);
