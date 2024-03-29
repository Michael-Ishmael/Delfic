'use strict';

if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
    var msViewportStyle = document.createElement('style')
    msViewportStyle.appendChild(
        document.createTextNode(
            '@-ms-viewport{width:auto!important}'
        )
    )
    document.querySelector('head').appendChild(msViewportStyle)
}

var app = angular.module('delfic',
    ['ngRoute', 'delfic.directives', 'delfic.services',  'blueimp.fileupload']);

app.constant('WS_PREFIX', 'http://127.0.0.1:8000');
app.config(['$routeProvider', '$httpProvider', 'fileUploadProvider', function ($routeProvider, $httpProvider, fileUploadProvider) {
    $routeProvider.
        when('/', {
            templateUrl: '/views/landing.html'
        }).
        when('/upload', {
            templateUrl: '/views/companyUpload.html',
            controller: 'CompanyUploadCtrl'
        }).
        when('/extraction', {
            templateUrl: '/views/extractionViewer.html',
            controller: 'ExtractionCtrl'
        })
        .otherwise({redirectTo: '/'});

    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    fileUploadProvider.defaults.redirect = window.location.href.replace(
        /\/[^\/]*$/,
        '/cors/result.html?%s'
    );

}]);

app.controller('appCtrl', ['$scope', '$location', 'MultiCompanyLoader',
    function($scope, $location, MultiCompanyLoader){

        $scope.listQuery = {top: 20, filter: ''};

        $scope.isActive = function (viewLocation){
            return viewLocation === $location.path();
        };

        $scope.companies = [];

        $scope.loadCompanies = function(top, filter){

            top = top || 20;

            MultiCompanyLoader.list(top, filter).then(function (companies) {

                $scope.companies = companies;
            });
        };

        $scope.clearCompanies = function(){

            MultiCompanyLoader.clear().then(function(status){
                if(status){
                    $scope.companies = []
                }
            })
        }

        $scope.addNewCompany = function(company){
            MultiCompanyLoader.add(company).then(function(status){
                if(status){
                    $scope.companies.unshift(company)
                }
            })
        }

    }
]);


app.controller('CompanyUploadCtrl', ['$scope',
        function($scope){

            $scope.companyToAdd = {};

            $scope.addCompany = function(){
                if($scope.companyToAdd.name && $scope.companyToAdd.registerednumber)
                    $scope.addNewCompany($scope.companyToAdd);
            };

            $scope.$watch('listQuery.top', updateList);
            $scope.$watch('listQuery.filter', updateList);

            function updateList(){
                $scope.loadCompanies($scope.listQuery.top, $scope.listQuery.filter);
            }

            $scope.loadCompanies($scope.listQuery.top, null);

        }
    ]);

app.controller('ExtractionCtrl', ['$scope',
    function($scope) {

        $scope.selections = {selectedIndex: null, selectedUrl: '', linkHistory: []};

        $scope.selectCompany = function (idx, id) {
            $scope.selections.selectedIndex = idx;
        };

        $scope.$watch('listQuery.top', updateList);
        $scope.$watch('listQuery.filter', updateList);

        function updateList(){
            $scope.loadCompanies($scope.listQuery.top, $scope.listQuery.filter);
        }

        $scope.loadCompanies($scope.listQuery.top, null);

    }
]);

app.controller('CompanyListController',
    function ($scope) {

        $scope.repo = CompanyRepository;
        $scope.companies = [];

        $scope.showAddCompany = false;

        $scope.toggleAddCompanyVisible = function(){
          $scope.showAddCompany = !$scope.showAddCompany;
        };

        $scope.companyToAdd = {};

        $scope.addCompany = function(){
            if($scope.companyToAdd.name && $scope.companyToAdd.registerednumber)
                $scope.addNewCompany($scope.companyToAdd);
        };


        $scope.addNewCompany()

        $scope.$watch('repo.companies', function(){
            $scope.companies = $scope.repo.companies;
        });

        MultiCompanyLoader.list().then(function (companies) {
            $scope.repo.companies = companies;
        });

        $scope.selectCompany = function (idx, id) {
            $scope.repo.selectedIndex = idx;
        }
    }
);

app.controller('ManageCompanyController', function ($scope, CompanyWebsiteLocator) {

    $scope.$watch('selections.selectedIndex', function () {
        if ($scope.selections.selectedIndex > -1
            && $scope.companies.length > $scope.selections.selectedIndex) {
            $scope.company = $scope.companies[$scope.selections.selectedIndex]
        }
    });

    $scope.getWebsiteUrl = function (id) {
        $scope.websiteStatus = 'Finding website...';
        var promise = CompanyWebsiteLocator.getWebsiteUrl(id);
        promise.then(function (payload) {
                $scope.company.website = payload;
                if(payload) $scope.selections.selectedUrl = payload;
                $scope.websiteStatus = null;
            },
            function (errorPayload) {
                $scope.websiteStatus = errorPayload;
            }
        );
    };

    $scope.loadSiteData  = function() {
        getWebsiteMetaTags();
        getWebsiteLinks();
    };

    $scope.setAnalyseUrl = function (url) {
      $scope.selectedUrl = url;
    };

    function getWebsiteMetaTags () {
        $scope.pageLoadStatus = 'Finding metadata...';
        var promise = CompanyWebsiteLocator.getWebsiteMeta($scope.company.website);
        promise.then(function (payload) {
                $scope.company.metatags = payload;
                $scope.pageLoadStatus = null;
            },
            function (errorPayload) {
                $scope.pageLoadStatus = errorPayload;
            }
        );
    };

    function getWebsiteLinks() {
        $scope.pageLoadStatus += '<br>Finding top level links...';
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


app.controller('CompanyMetadataController', function ($scope, CompanyPageResults) {

    $scope.pageUrl = '';

    $scope.$watch('selections.selectedUrl', function () {
        $scope.pageUrl = $scope.selections.selectedUrl;
        $scope.loadPageResults();
    });

    $scope.loadPageResults  = function() {
        if(!$scope.pageUrl) return;
        getPageCalais();
        getPageText();
    };

    function getPageCalais () {
        $scope.status = 'Finding page Open Calais results...';
        var promise = CompanyPageResults.getCalaisTags($scope.pageUrl);
        promise.then(function (payload) {
                $scope.calaisTags = payload;
                $scope.status = null;
            },
            function (errorPayload) {
                $scope.status = errorPayload;
            }
        );
    }

    function getPageText(){
        $scope.status = 'Finding page Open Calais results...';
        var promise = CompanyPageResults.getPageText($scope.pageUrl);
        promise.then(function (payload) {
                $scope.pageText = payload;
                $scope.status = null;
            },
            function (errorPayload) {
                $scope.status = errorPayload;
            }
        );

    }

    function getWebsiteLinks() {
        $scope.websiteStatus += '<br>Finding top level links...';
        var promise = CompanyPageResults.getWebsiteLinks($scope.company.website);
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


app.controller('DemoFileUploadController', [
    '$scope', '$http', '$filter', '$window',
    function ($scope, $http) {
        var url = 'http://127.0.0.1:8000/upload/uploadcompanyfilex';
        $scope.options = {
            url: url
        };

        //$scope.getList = function(){
            $http.get(url)
                .then(
                function (response) {
                    $scope.loadingFiles = false;
                    $scope.queue = response.data.files || [];
                },
                function () {
                    $scope.loadingFiles = false;
                }
            );
        //};

        $scope.loadingFiles = false;


    }
]);



/*
app.controller('FileDestroyController', [
    '$scope', '$http',
    function ($scope, $http) {
        var file = $scope.file,
            state;
        if (file.url) {
            file.$state = function () {
                return state;
            };
            file.$destroy = function () {
                state = 'pending';
                return $http({
                    url: file.deleteUrl,
                    method: file.deleteType
                }).then(
                    function () {
                        state = 'resolved';
                        $scope.clear(file);
                    },
                    function () {
                        state = 'rejected';
                    }
                );
            };
        } else if (!file.$cancel && !file._index) {
            file.$cancel = function () {
                $scope.clear(file);
            };
        }
    }
]);



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

*/
