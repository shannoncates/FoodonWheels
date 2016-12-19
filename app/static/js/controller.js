//landingController starts here
angular.module('mainApp').controller('landingController', ['$scope', '$location', 'AuthService',
	function($scope, $location, AuthService) {
		$scope.error = false;
		$scope.disabled = true;
		$location.path('/');
		if (Cookies.get('authed') == 'true') {
			Cookies.set('viewuser', Cookies.get('user_id'))
			$location.path('/search');
		};
		$scope.disabled = false;
	}
]);
//landingController ends here


//navbarController starts here
angular.module('mainApp').controller('navbarController', ['$scope', '$route', '$location',
	function($scope, $route, $location) {
		$scope.rload = function() {
			$route.reload();
		};
		$scope.logout2 = function() {

			Cookies.set('authed', false);
			$location.path('/');
			logout();
		};
		Cookies.set('authed', false);
		$scope.error = false;
		$scope.disabled = true;
		$location.path('/');
		$scope.authed = function() {
			if (Cookies.get('authed') == 'true') {
				return true
			} else {
				return false
			}
		};
		$scope.disabled = false;
	}
]);
//navbarController ends here


//registerController starts here
angular.module('mainApp').controller('registerController', ['$scope', '$location', 'AuthService',
	function($scope, $location, AuthService) {
		$scope.register = function() {

			//Initializations
			$scope.error = false;
			$scope.disabled = true;

			//Call the register function
			AuthService.register($scope.registrationForm.email,
				$scope.registrationForm.firstname,
				$scope.registrationForm.middleinitial,
				$scope.registrationForm.lastname,
				$scope.registrationForm.password,
				$scope.registrationForm.contactno,
				$scope.registrationForm.address
			)

			//If the registration process was successful
			.then
				(function() {
					//Redirect to login page
					$location.path('/login');
					$scope.disabled = false;
					$scope.registrationForm = {};
				})

			//If the registration process encountered errors
			.catch
				(function() {
					$scope.error = true;
					$scope.disabled = false;
					$scope.registrationForm = {};
					$scope.errorMessage = "An error was encountered";
				});
		};
	}
]);
//registerController ends here