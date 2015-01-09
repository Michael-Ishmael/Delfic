'use strict';

var app = angular.module('delfic',
    ['delfic.directives', 'delfic.services']);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
        when('/', {
            controller: 'ListCtrl',
            resolve: {
                companies: ["MultiCompanyLoader", function (MultiCompanyLoader) {
                    return MultiCompanyLoader();
                }]
            },
            templateUrl: '/views/list.html'
        }).when('/edit/:companyId', {
            controller: 'EditCtrl',
            resolve: {
                company: ["CompanyLoader", function (CompanyLoader) {
                    return CompanyLoader();
                }]
            },
            templateUrl: '/views/companyForm.html'
        }).when('/view/:companyId', {
            controller: 'ViewCtrl',
            resolve: {
                company: ["CompanyLoader", function (CompanyLoader) {
                    return CompanyLoader();
                }]
            },
            templateUrl: '/views/viewCompany.html'
        }).when('/new', {
            controller: 'NewCtrl',
            templateUrl: '/views/companyForm.html'
        }).otherwise({redirectTo: '/'});
}]);

app.controller('ListCtrl', ['$scope', 'companies', 'CompanyWebsiteLocator',
    function ($scope, companies, CompanyWebsiteLocator) {
        $scope.companies = companies;

        $scope.getWebsiteUrl = function (id, idx) {
            companies[idx].loading = true;
            var promise = CompanyWebsiteLocator.getWebsiteUrl(id);
            promise.then(function (payload) {
                    $scope.companies[idx].websiteurl = payload;
                    companies[idx].loading = false;
                },
                function (errorPayload) {
                    $scope.companies[idx].websiteurl = errorPayload;
                    companies[idx].loading = false;
                }
            );
        };

    }]);

app.controller('ViewCtrl', ['$scope', '$location', 'company',
    function ($scope, $location, company) {
        $scope.company = company;

        $scope.edit = function () {
            $location.path('/edit/' + company.registerednumber);
        };
    }]);

app.controller('EditCtrl', ['$scope', '$location', 'company',
    function ($scope, $location, company) {
        $scope.company = company;

        $scope.save = function () {
            $scope.company.$save(function (company) {
                $location.path('/view/' + company.registerednumber);
            });
        };

        $scope.remove = function () {
            delete $scope.company;
            $location.path('/');
        };
    }]);

app.controller('NewCtrl', ['$scope', '$location', 'Company',
    function ($scope, $location, Company) {
        $scope.company = new Company({
            ingredients: [{}]
        });

        $scope.save = function () {
            $scope.company.$save(function (company) {
                $location.path('/view/' + company.registerednumber);
            });
        };
    }]);

app.controller('CompanyListController', function ($scope, CompanyRepository, MultiCompanyLoader) {

        $scope.repo = CompanyRepository;
        $scope.companies = [];

        $scope.$watch('repo.companies', function(){
            $scope.companies = $scope.repo.companies;
        });

        MultiCompanyLoader().then(function (companies) {
            $scope.repo.companies = companies;
        });

        $scope.selectCompany = function (idx, id) {
            $scope.repo.selectedIndex = idx;
        }
    }
);

app.controller('ManageCompanyController', function ($scope, CompanyRepository, CompanyWebsiteLocator) {

    $scope.repo = CompanyRepository;

    $scope.$watch('repo.selectedIndex', function () {
        if ($scope.repo.selectedIndex > -1
            && $scope.repo.companies.length > $scope.repo.selectedIndex) {
            $scope.company = $scope.repo.companies[CompanyRepository.selectedIndex]
        }
    });

    $scope.getWebsiteUrl = function (id) {
        $scope.websiteStatus = 'Finding website...';
        var promise = CompanyWebsiteLocator.getWebsiteUrl(id);
        promise.then(function (payload) {
                $scope.company.website = payload;
                $scope.websiteStatus = null;
            },
            function (errorPayload) {
                $scope.websiteStatus = errorPayload;
            }
        );
    };

    $scope.getWebsiteLinks = function () {
        var promise = CompanyWebsiteLocator.getWebsiteLinks($scope.company.website);
        promise.then(function (payload) {
                $scope.company.websitelinks = payload;
                $scope.websiteLinkStatus = null;
            },
            function (errorPayload) {
                $scope.websiteLinkStatus = errorPayload;
            }
        );
    }


});
