var mainApp = angular.module("mainApp", ['ngRoute']);


mainApp.config(['$routeProvider', '$locationProvider',
	function($routeProvider, $locationProvider)
	{
		$routeProvider.
		when('/', {
			templateUrl: 'static/html/index.html',
			controller: 'landingController'
		}).
		when('/register', {
			templateUrl: 'static/html/register.html',
			controller: 'registerController'
		}).
		otherwise({
			redirectTo: '/'
		});

		$locationProvider.html5Mode(true);
	}
]);