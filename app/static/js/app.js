
// app.js


var mainApp = angular.module("mainApp", ['ngRoute']);


mainApp.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) 
	{
        $routeProvider.
        when('/', {
            templateUrl: 'static/html/landing.html',
            controller: 'landingController'
        }).
        when('/register', {
            templateUrl: 'static/html/register.html',
            controller: 'registerController'
        }).
        when('/termsofagreement', {
            templateUrl: 'static/html/termsofagreement.html',
            controller: 'termsofagreementController'
        }).
        when('/login', {
            templateUrl: 'static/html/login.html',
            controller: 'loginController'
        }).
		when('/logout', {
			controller: 'logoutController'
		}).
        when('/about', {
            templateUrl: 'static/html/about.html',
            controller: 'aboutController'
        }).
        when('/inbox', {
            templateUrl: 'static/html/inbox.html',
            controller: 'inboxController',
            access:{restricted: false}
        }).
        when('/api/privatemessage', {
            templateUrl: 'static/html/privatemessage.html',
            controller: 'pmController',
            access:{restricted: false}
        }).
        when('/userprofile', {
            controller: 'userprofileController',
            templateUrl: 'static/html/userprofile.html',
            access:{restricted: false}
        }).
        when('/search', {
            templateUrl: 'static/html/searchpage.html',
            controller: 'searchpageController',
            access:{restricted: false}
        }).
        when('/upload', {
            templateUrl: 'static/html/upload.html',
            controller: 'uploadController'
        }).
        when('/thesisinfo/:thesis_id', {
            controller: 'thesisinfoController',
            templateUrl: 'static/html/thesisinfo.html'
        }).
        when('/category', {
            controller: 'categoryController',
            templateUrl: 'static/html/category.html'
        }).
        otherwise({
            redirectTo: '/'
        });

        // Remove the # in urls
        $locationProvider.html5Mode(true);   
    }
]);


