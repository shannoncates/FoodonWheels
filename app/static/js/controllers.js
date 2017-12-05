// controllers.js
// landingController starts here
angular.module('mainApp').controller('landingController', ['$scope', '$location', 'AuthService',
    function($scope, $location, AuthService) {
        $scope.error = false;
        $scope.disabled = true;
        $location.path('/');
        if (Cookies.get('authed') == 'true') {
            Cookies.set('viewuser', Cookies.get('idnumber'))
            $location.path('/userprofile');
        };
        $scope.disabled = false;
    }
]);
// landingController ends here


// navbarController starts here
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
// navbarController ends here


// registerController starts here
angular.module('mainApp').controller('registerController', ['$scope', '$location', 'AuthService',
    function($scope, $location, AuthService) {
        $scope.register = function() {

            // Initializations
            $scope.error = false;
            $scope.disabled = true;

            // Call the register function
            AuthService.register($scope.registrationForm.idnumber,
                $scope.registrationForm.firstname,
                $scope.registrationForm.lastname,
                $scope.registrationForm.middleinitial,
                $scope.registrationForm.email,
                $scope.registrationForm.password,
                $scope.registrationForm.confirmpassword
            )

            // If the registration process was successful
            .then
                (function() {
                    // Redirect to login page
                    $location.path('/login');
                    $scope.disabled = false;
                    $scope.registrationForm = {};
                })

            // If the registration process encountered errors
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
// registerController ends here


// loginController starts here
angular.module('mainApp').controller('loginController', ['$scope', '$route', '$location', 'AuthService',
    function($scope, $route, $location, AuthService) {
        $scope.rload = function() {
            $location.path('/');
        };
        $scope.login = function() {
            // Initializations
            $scope.error = false;
            $scope.disabled = true;

            // Call the login function
            AuthService.login(scope.loginForm.idnumber, $scope.loginForm.password)

            // handle success
            .then
                (function() {
                    $location.path('/profile');
                    $scope.disabled = false;
                    $scope.loginForm = {};
                })

            // handle error
            .catch
                (function() {
                    $scope.error = true;
                    $scope.disabled = false;
                    $scope.loginForm = {};
                    $scope.errorMessage = "Incorrect id number or password";
                });
        };
    }
]);
// loginController ends here


// userprofileController starts here
angular.module('mainApp').controller('userprofileController', ['$scope', '$route', '$location', '$q',
    function($scope, $route, $location, $q) {
        var deferred = $q.defer();
        var image_version;
        var user_id = Cookies.get('idnumber');

        $scope.rload = function() {
            $route.reload();
        };

        // Profile picture
        // If the user has just registered and logged in immediately
        if ((Cookies.get('new_user') == '1') && (Cookies.get('idnumber') == Cookies.get('viewuser'))) {
            // Load the default thesis archive profile picture if new user
            $("#profilepicturediv").append('<center><img id="profilepicture" alt="" src="static/profile_pictures/default.jpg" data-original-title="Usuario"></center><br><br>');
            $("#editprofilepicturediv").append('<center><a href="#" data-toggle="modal" data-target="#myModal"><u>Change Profile Picture</u></a></center>');
        }
        // If the user has already registered
        else {
            // If the user views his own profile
            if (Cookies.get('idnumber') == Cookies.get('viewuser')) {
                $.ajax({
                    url: '/profilepictures/' + user_id,
                    type: 'get',
                    headers: {
                        "Authorization": "bearer " + Cookies.get("token")
                    },
                    success: function(data) {
                        $("#profilepicturediv").empty();
                        image_version = data['filename'].slice(-10);
                        console.log("Version:");
                        console.log(image_version);
                        $("#profilepicturediv").append('<center><img id="profilepicture" alt="" src="/static/profile_pictures/' + image_version + '" data-original-title="Usuario"></center><br><br>');
                        $("#editprofilepicturediv").append('<center><a href="#" data-toggle="modal" data-target="#myModal"><u>Change Profile Picture</u></a></center>');
                    }
                });
            }
            // If the user views other profiles
            else {
                $.ajax({
                    url: '/profilepictures/' + Cookies.get('viewuser'),
                    type: 'get',
                    headers: {
                        "Authorization": "bearer " + Cookies.get("token")
                    },
                    success: function(data) {
                        $("#profilepicturediv").empty();
                        image_version = data['filename'].slice(-10);
                        console.log("Version:");
                        console.log(image_version);
                        $("#profilepicturediv").append('<center><img id="profilepicture" alt="" src="/static/profile_pictures/' + image_version + '" data-original-title="Usuario"></center><br><br>');
                    }
                });
            }

        }

        if (Cookies.get('idnumber') == Cookies.get('viewuser')) {
            html = '<div class="row">' +
                '<div class="col-md-6">' +
                '<button id = "uploadmodalopen" type="button"  onclick="placeid();" class="btn btn-success" data-toggle="modal" data-target="#uploadModal" data-whatever="@mdo">' +
                'Share Thesis' +
                '</button>' +
                '&nbsp;&nbsp;' +
                '</div>' +
                '</div>';

            $("#sharethesis").append(html);
            $("#editprofile").append('<a href="#" onclick="get_user_records();" data-toggle="modal" data-target="#editprofileModal"><u>Edit Profile<u></a>');
        }

        $.ajax({
            url: '/api/user/' + Cookies.get('viewuser'),
            type: 'get',
            dataType: 'json',
            headers: {
                "Authorization": "bearer " + Cookies.get("token")
            },
            error: function() {
                $("div").append("<h1>error </h1>" + console.log());
            },
            success: function(data) {
                $("#idnumberlabel").append(data['user_info']['id_number']);
                $("#fnamelabel").append(data.user_info.firstname);
                $("#lnamelabel").append(data.user_info.lastname);
                $("#mnamelabel").append(data.user_info.middle_initial);
                $("#emaillabel").append(data.user_info.email);
                $("#role").append(data.user_info.role);
                $scope.id_number = data['user_info']['id_number'];

            }

        });

        $.ajax({
            url: '/api/thesis/' + Cookies.get('viewuser'),
            type: 'get',
            dataType: 'json',
            headers: {
                "Authorization": "bearer " + Cookies.get("token")
            },
            error: function() {
                $("#item1").append("<h1>error </h1>" + console.log());
            },
            success: function(data) {
                var n = 0;
                htmlstring = '';
                if (data["entries"] != "empty") {
                    for (n = 0; n < data["entries"].length; n = n + 1) {
                        htmlstring = '' +
                            '<tr>' +
                            '<td class="mailbox-star"><a href="#"><i class="fa fa-mail"></i></a></td>' +
                            '<td class="mailbox-name"><a href="/thesisinfo/' + data["entries"][n]["thesis_id"] + '" onclick="rememberthesisid(' + data["entries"][n]["thesis_id"] + ')">' + data["entries"][n]["thesis_name"] + '</a></td>' +
                            '<td class="mailbox-subject">' + data["entries"][n]["adviser_id_number"] + ' as Adviser' +
                            '</td>' +
                            '<td class="mailbox-attachment">' +
                            '<a onclick="updatethesis(' + data["entries"][n]["thesis_id"] + ');" style="cursor:pointer">Update</a>' + '&nbsp&nbsp&nbsp' +
                            '<a onclick="removethesis(' + data["entries"][n]["thesis_id"] + ');" style="cursor:pointer">Remove</a> ' + '&nbsp&nbsp&nbsp' +
                            '<a onclick="downloadthesis(' + data["entries"][n]["thesis_id"] + ');" style="cursor:pointer">Download</a>' + '&nbsp&nbsp&nbsp' +
                            '</td>' +
                            '<td class="mailbox-date">' + 'Published on ' + data["entries"][n]["date_published"] + '</td>' +
                            '</tr>';

                        if (Cookies.get('idnumber') != data['entries'][n]['uploader_id_number']) {
                            htmlstring = '' +
                                '<tr>' +
                                '<td class="mailbox-star"><a href="#"><i class="fa fa-mail"></i></a></td>' +
                                '<td class="mailbox-name"><a href="/thesisinfo/' + data["entries"][n]["thesis_id"] + '" onclick="rememberthesisid(' + data["entries"][n]["thesis_id"] + ')">' + data["entries"][n]["thesis_name"] + '</a></td>' +
                                '<td class="mailbox-subject">' + data["entries"][n]["adviser_id_number"] + ' as Adviser' +
                                '</td>' +
                                '<td class="mailbox-attachment">' +


                                '<a onclick="downloadthesis(' + data["entries"][n]["thesis_id"] + ');" style="cursor:pointer">Download</a>' + '&nbsp&nbsp&nbsp' +
                                '</td>' +
                                '<td class="mailbox-date">' + 'Published on ' + data["entries"][n]["date_published"] + '</td>' +
                                '</tr>';
                        }

                        $("#thesistablebody").append(htmlstring);

                    };
                }



            }
        });
    }
]);
// userprofileController ends here


//categoryController starts here
angular.module('mainApp').controller('categoryController', ['$scope', '$route', '$location', '$q',
    function($scope, $route, $location, $q) {
        var deferred = $q.defer();
        var thesis_id = Cookies.get('thesis_id');
        var user_id = Cookies.get('viewuser');
        var department_id = Cookies.get('department_id');



        // Generate the fullname of the adviser
        function generate_adviser(adviser_id) {
            var firstname;
            var middleinitial;
            var lastname;
            var fullname;

            // Retrieve the fullname of the uploader
            $.ajax({
                url: '/api/user/' + adviser_id,
                type: 'get',
                dataType: 'json',
                headers: {
                    "Authorization": "bearer " + Cookies.get("token")
                },
                error: function() {
                    $("div").append("<h1>error</h1>");
                },
                success: function(data) {
                    firstname = data['user_info']['firstname'];
                    middleinitial = data['user_info']['middle_initial'];
                    lastname = data['user_info']['lastname'];
                    fullname = firstname + ' ' + middleinitial + '.' + ' ' + lastname;
                    $("#adviser").append(fullname);
                }

            });
        }


        // Generate the name of the department
        function generate_department(department_id) {
            var departmentname;



            // Retrieve the name of the department
            $.ajax({
                url: '/api/department/' + Cookies.get('department_id'),
                type: 'get',
                dataType: 'json',
                error: function() {

                },
                success: function(data) {
                    departmentname = data['entry']['department_name'];
                    $("#department").append(data['entry']['departmentname']);
                    console.log(departmentname);
                    console.log(department_id);
                }

            });

        }

        $scope.rload = function() {
            $route.reload();
        };

        $.ajax({
            url: '/api/thesis/department/' + Cookies.get('department_id'),
            type: 'get',
            dataType: 'json',
            headers: {
                "Authorization": "bearer " + Cookies.get("token")
            },
            error: function() {
                $("div").append("<h1>error </h1>" + console.log());
            },
            success: function(data) {
                var n=0;
                if(data['match'].length != 0){
                    for(n=0; n<data['match'].length; n = n+1){
                        var htmlstring = ''+
                            '<tr>'+
                                '<td id="thesis_title">'+data['match'][n]['thesis_name']+'</td>'+
                                '<td id="abstract">'+data['match'][n]['abstract']+'</td>'+
                                '<td id="adviser">'+data['match'][n]['adviser_id_number']+'</td>'+
                                '<td id="date_published">'+data['match'][n]['date_published']+'</td>'+
                                '<td id="renderDocument" ng-controller="renderdocumentController"></td>'+
                            '</tr>';
                        $("#categorytablebody").append(htmlstring);
                    }
                }else{
                    $("#categorytablebody").append("<td>no entry</td>");
                }
            }

        });
    }
]);
//categoryController ends here


// feedbackController starts here
angular.module('mainApp').controller('feedbackController', ['$scope', '$route', '$location', '$q',
    function($scope, $route, $location, $q) {
        var current_user = Cookies.get('viewuser');
        var thesis_id = Cookies.get('thesis_id');
        var tmp;
        var uploader;

        $scope.rload = function() {
            $route.reload();
        };

        // Generate the fullname of the user who created the feedback
        function generate_user(user_id) {
            var firstname;
            var middleinitial;
            var lastname;
            var fullname;

            // Retrieve the fullname of the uploader
            $.ajax({
                url: '/api/user/' + user_id,
                type: 'get',
                dataType: 'json',
                headers: {
                    "Authorization": "bearer " + Cookies.get("token")
                },
                error: function() {
                    $("div").append("<h1>error</h1>");
                },
                success: function(data) {
                    firstname = data['user_info']['firstname'];
                    middleinitial = data['user_info']['middle_initial'];
                    lastname = data['user_info']['lastname'];
                    fullname = firstname + ' ' + middleinitial + '.' + ' ' + lastname;
                    $("#feedbacks").append(fullname);
                }

            });
        };



        // Retrive all feedbacks of the thesis which matches the thesis_id
        $.ajax({
            url: '/api/thesis/' + thesis_id + '/feedback',
            type: 'get',
            dataType: 'json',
            error: function() {
                $("div").append("<h1>error</h1>");
            },
            success: function(data) {

                if (data.count != 0) {
                    for (i = 0; i < data.count; i++) {
                        var user_id = String(data['entries'][i]['user_id']);
                        var feedback_id = data['entries'][i]['feedback_id'];

                        // edit feedback
                        // idnumber is the cookie set upon login
                        if (user_id == Cookies.get("idnumber")) {
                            $("#feedbacks").append("<div class='panel-heading'>");
                            $("#feedbacks").append("<blockquote><small>" + data['entries'][i]['body'] + "<br>" + "Submitted by " + data['entries'][i]['user_id'] + "<br>" + "Published on " + data['entries'][i]['date_published'] + "</small></blockquote>");
                            $("#feedbacks").append("<a id='edit-feedback-" + feedback_id + "' href='javascript:;' onclick='edit_feedback(" + feedback_id + ");'>Edit feedback</a>");
                            $("#feedbacks").append("</div>");
                            $("#feedbacks").append("<div id=" + feedback_id + "></div>");
                        } else {
                            $("#feedbacks").append("<div class='panel-heading'>");
                            $("#feedbacks").append("<blockquote><small>" + data['entries'][i]['body'] + "<br>" + "Submitted by " + data['entries'][i]['user_id'] + "<br>" + "Published on " + data['entries'][i]['date_published'] + "</small></blockquote>");
                            $("#feedbacks").append("</div>");
                        }

                    }
                }
            }
        });
    }
]);
// feedbackController ends here


// thesisinfoController starts here
angular.module('mainApp').controller('thesisinfoController', ['$scope', '$route', '$location', '$q',
    function($scope, $route, $location, $q) {
        var deferred = $q.defer();
        var thesis_id = Cookies.get('thesis_id');
        var user_id = Cookies.get('viewuser');


        // Generate the fullname of the current user
        function generate_user(uploader_id) {
            var firstname;
            var middleinitial;
            var lastname;
            var fullname;

            // Retrieve the fullname of the uploader
            $.ajax({
                url: '/api/user/' + uploader_id,
                type: 'get',
                dataType: 'json',
                headers: {
                    "Authorization": "bearer " + Cookies.get("token")
                },
                error: function() {
                    $("div").append("<h1>error</h1>");
                },
                success: function(data) {
                    firstname = data['user_info']['firstname'];
                    middleinitial = data['user_info']['middle_initial'];
                    lastname = data['user_info']['lastname'];
                    fullname = firstname + ' ' + middleinitial + '.' + ' ' + lastname;
                    $("#author").append(fullname);
                }

            });
        }

        // Generate the fullname of the adviser
        function generate_adviser(adviser_id) {
            var firstname;
            var middleinitial;
            var lastname;
            var fullname;

            // Retrieve the fullname of the uploader
            $.ajax({
                url: '/api/user/' + adviser_id,
                type: 'get',
                dataType: 'json',
                headers: {
                    "Authorization": "bearer " + Cookies.get("token")
                },
                error: function() {
                    $("div").append("<h1>error</h1>");
                },
                success: function(data) {
                    firstname = data['user_info']['firstname'];
                    middleinitial = data['user_info']['middle_initial'];
                    lastname = data['user_info']['lastname'];
                    fullname = firstname + ' ' + middleinitial + '.' + ' ' + lastname;
                    $("#adviser").append(fullname);
                }

            });
        }

        $scope.rload = function() {
            $route.reload();
        };

        $.ajax({
            url: '/api/thesis/' + thesis_id,
            type: 'get',
            dataType: 'json',
            headers: {
                "Authorization": "bearer " + Cookies.get("token")
            },
            error: function() {
                $("div").append("<h1>error </h1>" + console.log());
            },
            success: function(data) {

                adviser_id = String(data['match']['adviser_id_number']);

                $("#thesis_title").append(data['match']['thesis_name']);
                generate_user(user_id);
                generate_adviser(adviser_id);
                $("#abstract").append(data['match']['abstract']);
                $("#date_published").append(data['match']['date_published']);
            }

        });
    }
]);
// thesisinfoController ends here


// renderdocumentController starts here
angular.module('mainApp').controller('renderdocumentController', ['$scope', '$location',
    function($scope, $location) {
        var thesis_id = Cookies.get('thesis_id');
        var filename;

        // Retrieve the filename of the thesis
        $.ajax({
            url: '/api/thesis/' + thesis_id,
            type: 'get',
            headers: {
                "Authorization": "bearer " + Cookies.get("token")
            },
            error: function() {

            },
            success: function(data) {
                filename = data['match']['filename'];
                url = 'static/web/viewer.html?file=' + filename;
                $("#renderDocument").append("<center><a class='btn btn-success' href=" + url + " target='_blank' style='target-new: tab;'>Read Full Document</a></center>");

            }

        });
    }
]);
// renderdocumentController ends here


// logoutController starts here
angular.module('mainApp').controller('logoutController', ['$scope', '$location', 'AuthService',
    function($scope, $location, AuthService) {
        $scope.logout = function() {
            // Call the logout function
            AuthService.logout()
                .then(function() {
                    $location.path('/login');
                });
        };
    }
]);
// logoutController ends here


// inboxController starts here
angular.module('mainApp').controller('inboxController', ['$scope', '$location',
    function($scope, $location) {
        $.ajax({
            url: '/api/privatemessage/' + Cookies.get('idnumber'),
            type: 'get',
            error: function() {
                $("div").append("<h1>error </h1>" + console.log());
            },
            success: function(data) {
                var senderarray = [];
                var messind = 0;
                for (messind = 0; messind < data["entries"].length; messind = messind + 1) {
                    senderarray[data["entries"][messind]["sender_id"]] = data["entries"][messind]["message_body"];
                };
                senders = Object.keys(senderarray);
                for (messind = 0; messind < senders.length / 2; messind = messind + 1) {
                    var htmlstring = '<a href = "/api/privatemessage"' +
                        'class="list-group-item" onclick = "conversationpartner(\'' + senders[messind] + '\');">' +

                        ' <span class="glyphicon glyphicon-star-empty"></span> ' +
                        ' <span class="name" style="min-width: 120px; display: inline-block;"> ' + senders[messind] +

                        ' </span> ' +
                        ' <span class="">This is big title</span> ' +
                        ' <span class="text-muted" style="font-size: 11px;">' + senderarray[senders[messind]] + '</span> ' +
                        ' <span class="badge">12:10 AM</span> <span class="pull-right"> ' +
                        ' <span class="glyphicon glyphicon-paperclip"> ' +
                        '</span></span>' +
                        '</a>';
                    $("#inboxlist").append(htmlstring);
                };

            }
        });
    }
]);
// inboxController ends here


// pmController starts here
angular.module('mainApp').controller('pmController', ['$scope', '$location',
    function($scope, $location) {
        socket = io.connect();
        socket.emit('open_chat', {
            'receiver_id': Cookies.get('idnumber'),
            'sender_id': Cookies.get('partner')
        });
        socket.on('my_message', function(data) {
            if (data["sender_id"] == Cookies.get('partner')) {
                /* Message. Default to the left */
                htmlstring = '<div class="direct-chat-msg">' +
                    '<div class="direct-chat-info clearfix">' +
                    '<span class="direct-chat-name pull-left">' + data["sender_id"] + '</span>' +
                    '<span class="direct-chat-timestamp pull-right">23 Jan 2:00 pm</span>' +
                    '</div><!-- /.direct-chat-info -->' +
                    '<img class="direct-chat-img" src="/static/images/msuiit-logo-275x280.png" alt="message user image"><!-- /.direct-chat-img -->' +
                    '<div class="direct-chat-text">' +
                    '' + data["message_body"] +
                    '</div><!-- /.direct-chat-text -->' +
                    '</div><!-- /.direct-chat-msg -->';
            } else {
                /* Message to the right */
                htmlstring = '<div class="direct-chat-msg right">' +
                    '<div class="direct-chat-info clearfix">' +
                    '<span class="direct-chat-name pull-right">' + data["sender_id"] + '</span>' +
                    '<span class="direct-chat-timestamp pull-left">23 Jan 2:05 pm</span>' +
                    '</div><!-- /.direct-chat-info -->' +
                    '<img class="direct-chat-img" src="/static/images/msuiit-logo-275x280.png" alt="message user image"><!-- /.direct-chat-img -->' +
                    '<div class="direct-chat-text">' +
                    '' + data["message_body"] +
                    '</div><!-- /.direct-chat-text -->' +
                    '</div><!-- /.direct-chat-msg -->';
            };
            $("#chatdiv").append(htmlstring);
            $("#chatdiv").scrollTop($("#chatdiv")[0].scrollHeight);
            $("#message_body").val('');
        });
        $.ajax({
            url: '/api/privatemessage/' + Cookies.get('idnumber') + '/' + Cookies.get('partner'),
            type: 'get',
            error: function() {
                $("div").append("<h1>error </h1>" + console.log());
            },
            success: function(data) {
                var n = 0;
                var htmlstring = "";
                for (n = 0; n < data["conversation"].length; n = n + 1) {
                    if (data["conversation"][n]["sender_id"] == Cookies.get('partner')) {
                        /* Message. Default to the left */
                        htmlstring = '<div class="direct-chat-msg">' +
                            '<div class="direct-chat-info clearfix">' +
                            '<span class="direct-chat-name pull-left">' + data["conversation"][n]["sender_id"] + '</span>' +
                            '<span class="direct-chat-timestamp pull-right">23 Jan 2:00 pm</span>' +
                            '</div><!-- /.direct-chat-info -->' +
                            '<img class="direct-chat-img" src="/static/images/msuiit-logo-275x280.png" alt="message user image"><!-- /.direct-chat-img -->' +
                            '<div class="direct-chat-text">' +
                            '' + data["conversation"][n]["message_body"] +
                            '</div><!-- /.direct-chat-text -->' +
                            '</div><!-- /.direct-chat-msg -->';
                    } else {
                        /* Message to the right */
                        htmlstring = '<div class="direct-chat-msg right">' +
                            '<div class="direct-chat-info clearfix">' +
                            '<span class="direct-chat-name pull-right">' + data["conversation"][n]["sender_id"] + '</span>' +
                            '<span class="direct-chat-timestamp pull-left">23 Jan 2:05 pm</span>' +
                            '</div><!-- /.direct-chat-info -->' +
                            '<img class="direct-chat-img" src="/static/images/msuiit-logo-275x280.png" alt="message user image"><!-- /.direct-chat-img -->' +
                            '<div class="direct-chat-text">' +
                            '' + data["conversation"][n]["message_body"] +
                            '</div><!-- /.direct-chat-text -->' +
                            '</div><!-- /.direct-chat-msg -->';
                    };
                    $("#chatdiv").append(htmlstring);
                };
            }
        });
    }
]);
// pmController ends here


// searchpageController starts here
angular.module('mainApp').controller('searchpageController', ['$scope', '$location', '$route',
    function($scope, $location, $route) {

        var n = 0;
        var htmlstring = "";
        $.ajax({
            url: '/api/search',
            type: 'post',
            dataType: 'json',
            data: $("#search-box").serializeArray(),
            headers: {
                "Authorization": "bearer " + Cookies.get("token")
            },
            error: function() {
                $("#item1").append("<h1>error </h1>");
            },
            success: function(data) {
                if (data["count"] == 0) {


                    $("#seed").append("<h1>No matches found</h1>");
                } else {
                    /*$("#seed").append("<h2>No matches found</h2>");*/
                    for (n = 0; n < data["entries"].length; n = n + 1) {
                        var temp = data["entries"][n]["id_number"];
                        if (typeof temp == 'string') {
                            htmlstring = '<div>' +
                                '<div class="row">' +
                                '<div class = "col-sm-1" ></div>' +
                                '<div><a href="/userprofile" onclick = "setviewuser(\'' + data["entries"][n]["id_number"] + '\');"><strong>' +
                                '' + data["entries"][n]["last_name"] +
                                ' ' + data["entries"][n]["first_name"] +
                                ' ' + data["entries"][n]["middle_initial"] +
                                '.</strong></a></div>' +
                                '</div>' +
                                '<div class ="row">' +
                                '<div class = "col-sm-1" ></div>' +
                                '<div> ID Number: ' + data["entries"][n]["id_number"] +
                                '</div>' +
                                '<div class ="row">' +
                                '<div class = "col-sm-1" ></div>' +
                                '<div> email: ' + data["entries"][n]["email"] +
                                '</div>' +
                                '</div>' +
                                '</div>' + '<hr>';
                        } else {
                            htmlstring = '<div>' +
                                '<div class="row">' +
                                '<div class = "col-sm-1" ></div>' +
                                '<div><a href="/thesisinfo/' + data["entries"][n]["thesis_id"] + '"> <strong>' +
                                '' + data["entries"][n]["thesis_name"] +
                                '</strong></a></div>' +
                                '</div>' +
                                '<div class ="row">' +
                                '<div class = "col-sm-1" ></div>' +
                                '<div> adviser: ' + data["entries"][n]["adviser_id"] +
                                '</div>' +
                                '</div>' +
                                '<div class ="row">' +
                                '<div class = "col-sm-1" ></div>' +
                                '<div> uploader: ' + data["entries"][n]["user_id"] +
                                '</div>' +
                                '</div>' +
                                '</div>' + '<hr>';
                        };
                        $("#seed").append(htmlstring);
                    };
                };
            }
        });
        $("#search-bar").val('');

    }
]);
// searchpageController ends here