angular.module('mainApp').factory('AuthService', ['$q', '$timeoute', '$http',

	function($q, $timeout, $http) {
		//Create an instance of the user and set the default to false
		var user = false;

		//Register function starts here
		function register(email, firstname, middleinitial, lastname, password, contactno, address) {
			//Create an instance of deferred
			var deferred = $q.defer();

			//Send a request to the server
			$http.post('/api/registeruser', {
				email: email,
				firstname: firstname,
				middleinitial: middleinitial,
				lastname: lastname,
				password: password,
				contactno: contactno,
				address: address
			})

			//If success
			.success(
				function(data, status) {
					if (status == 200 && data.result) {
						console.log("Registration was successful!");
						deferred.resolve();
					} else {
						console.log("Registration failed!");
						deferred.reject();
					}
				}
			)

			//If error
			.error(
				function(data) {
					console.log("Registration failed!");
					deferred.reject();
				}
			)

			return deferred.promise;

		}
		//Register function ends here
	}

]);