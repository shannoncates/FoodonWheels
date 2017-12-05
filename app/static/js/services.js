
// services.js


angular.module('mainApp').factory('AuthService', ['$q', '$timeout', '$http',

    function($q, $timeout, $http) {
        // Create an instance of the user and set the default to false
        var user = false;

        // Register function starts here
        function register(idnumber, firstname, lastname, middleinitial, email, password) {
            // Create an instance of deferred
            var deferred = $q.defer();

            // Send a request to the server
            $http.post('/api/registeruser', {
                idnumber: idnumber,
                firstname: firstname,
                lastname: lastname,
                middleinitial: middleinitial,
                email: email,
                password: password
            })

            // If success
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

            // If error
            .error(
                function(data) {
                    console.log("Registration failed!");
                    deferred.reject();
                }
            )

            return deferred.promise;

        }
        // Register function ends here

        // Login function starts here
        function login(idnumber, password) {
            // Create an instance of deferred
            var deferred = $q.defer();

            // Send a request to the server
            $http.post('/api/loginuser', {
                idnumber: idnumber,
                password: password
            })

            // If success
            .success(
                function(data, status) {
                    if (status === 200 && data.result) {
                        user = true;
                        deferred.resolve();
                    } else {
                        user = false;
                        deferred.reject();
                    }
                })

            // If error
            .error(
                function(data) {
                    user = false;
                    deferred.reject();
                });

            // return promise object
            return deferred.promise;
        }
        // Login function ends here


        // Determine if the user is logged in
        function logged_in() {
            if (user) return true;
            else return false;
        }


        function logout() {
            var deferred = $q.defer();
            return deferred.promise;
        }


        function user_status() {

        }

        return ({
            logged_in: logged_in,
            login: login,
            logout: logout,
            register: register,
            user_status: user_status
        });

    }

]);