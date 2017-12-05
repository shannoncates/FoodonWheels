var socket;
var files; // Variable to store your files


// Add events
$('input[type=file]').on('change', prepareUpload);


// Grab the files and set them to our variable
function prepareUpload(event) {
    files = event.target.files;
};


function emitprivatemessage() {
    socket.emit('new_message', {
        data: {
            'messagebody': $("#message_body").val(),
            'senderid': sender
        }
    });
}


function closechat(receiver, sender) {

    socket.emit('close_chat', {
        'receiver_id': receiver,
        'sender_id': sender
    })
}


function sendprivatemessage() {
    $.ajax({
        url: '/api/privatemessage/' + Cookies.get('idnumber') + '/' + Cookies.get('partner'),
        type: 'post',
        dataType: 'json',
        data: $("#message_body").serializeArray(),
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {
            $("div").append("<h1>error </h1>" + console.log());
        },
        success: function(data) {

            socket.emit('new_message', {
                'messagebody': $("#message_body").val(),
                'sender_id': Cookies.get('idnumber'),
                'receiver_id': Cookies.get('partner')
            });

        },

    });
};


function modalpm() {
    $.ajax({
        url: '/api/privatemessage/' + Cookies.get('idnumber'),
        type: 'post',
        dataType: 'json',
        data: $("#pmmodalform").serializeArray(),
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {
            $("#item1").append("<h1>error </h1>" + console.log());
            $("#pmmodalclose").trigger("click");
        },
        success: function(data) {
            if (data["status"] == "ok") {
                $("#message_body").val(data["status"])
                $("#pmmodalclose").trigger("click");
            } else {
                $("#message_title").val(data["status"])
            };

        }

    });
};


function removethesis(key) {
    $.ajax({
        url: '/api/thesis/' + key + '/delete',
        type: 'put',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {
            $("#item1").append("<h1>error </h1>" + console.log());
        },
        success: function(data) {
            $("#item1").append(data["message"]);
            $("#clicker").trigger("click");
        }
    });
};


function removethesiswithoutkey() {
    var key = Cookies.get('thesis_id');

    $.ajax({
        url: '/api/thesis/' + key + '/delete',
        type: 'put',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {
            $("#item1").append("<h1>error </h1>" + console.log());
        },
        success: function(data) {
            $("#item1").append(data["message"]);
        }
    });
};


function downloadthesis(key) {
    var form = $('<form method="GET">').attr('action', '/api/thesis/' + key + '/download');
    form.submit();
};


function downloadthesiswithoutkey() {
    var key = Cookies.get('thesis_id');

    var form = $('<form method="GET">').attr('action', '/api/thesis/' + key + '/download');
    form.submit();
}


function placeid() {

    $("#id_number").val(Cookies.get('idnumber'));
    $("#uploadmodalsubmit").attr("onclick", "uploadthesis('0');");
    Cookies.set("upload", "upload");
    $("#department_id").val("");
    $("#adviser_id").val("");
    $("#thesis_name").val("");
    $("#abstract").val("");
};


function uploadthesis(thesisid) {

    formdata = new FormData($("#file"));
    var rest = "";
    var meth = "";

    if (Cookies.get("upload") == "upload") {
        rest = '/api/thesis';
        meth = "post";
    } else {
        rest = '/api/thesis/' + Cookies.get("thesisid") + '/update';
        meth = "put"
    };

    formdata.append('file', $("#file")[0].files[0]);
    formdata.append('department_id', $("#department_id").val());
    formdata.append('id_number', $("#id_number").val());
    formdata.append('adviser_id', $("#adviser_id").val());
    formdata.append('thesis_name', $("#thesis_name").val());
    formdata.append('abstract', $("#abstract").val());

    $.ajax({
        url: rest,
        type: meth,
        data: formdata,
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {

            alert("An error was encountered.");
        },
        success: function(data) {
            $("#clicker").trigger("click");

        },
        processData: false, // tell jQuery not to process the data
        contentType: false // tell jQuery not to set contentType
    });
    $("#uploadmodalclose").trigger("click");
    $("#department_id").val("");
    $("#id_number").val("");
    $("#adviser_id").val("");
    $("#thesis_name").val("");
    $("#abstract").val("");
};


function updatethesis(key) {
    $("#uploadmodalopen").trigger("click");
    $.ajax({
        url: '/api/thesis/' + key,
        type: 'get',
        dataType: 'json',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {

            alert("An error was encountered.");
        },
        success: function(data) {
            $("#department_id").val(data["match"]["department_id"]);
            $("#id_number").val(data["match"]["uploader_id_number"]);
            $("#adviser_id").val(data["match"]["adviser_id_number"]);
            $("#thesis_name").val(data["match"]["thesis_name"]);
            $("#abstract").val(data["match"]["abstract"]);
        }
    });

    $("#uploadmodalsubmit").attr("onclick", "uploadthesis('" + key + "');");

    Cookies.set("upload", "not");
    Cookies.set("thesisid", key);
};


function setdepartmentid(key) {
    Cookies.set("department_id", key);
};


function setviewuser(key) {
    Cookies.set("viewuser", key);
};


function conversationpartner(key) {
    Cookies.set("partner", key);
};


function rememberthesisid(thesis_id) {
    Cookies.set("thesis_id", thesis_id);
};


function logout() {
    $.ajax({
        url: '/api/logout',
        type: 'get',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        success: function() {
            Cookies.set('authed', false);
            Cookies.set('token', "");
            console.log("Logged out.");
        }
    });
};


function login() {

    $.ajax({
        url: '/api/loginuser',
        type: 'post',
        dataType: 'json',
        data: $("#loginForm").serializeArray(),
        error: function() {

            alert("An error was encountered.");
        },
        success: function(data) {
            if (data["status"] == "error") {

                alert("Email or password is incorrect.");
            } else {

                Cookies.set('idnumber', data["User_Information"]["id_number"]);
                Cookies.set('token', data["User_Information"]["token"]);
                Cookies.set('authed', true);
                $("#clicker").trigger("click");
            }
        }
    });

    $.ajaxSetup({
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        }
    });
}


function register() {

    var idnumber = $("#idnumber").val();
    var firstname = $("#firstname").val();
    var lastname = $("#lastname").val();
    var middleinitial = $("#middleinitial").val();
    var role = $("#role").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var confirmpassword = $("#confirmpassword").val();

    if (password == confirmpassword) {
        $.ajax({
            url: '/api/registeruser',
            type: 'post',
            dataType: 'json',
            data: $("#registrationForm").serializeArray(),
            error: function() {

                alert("An error was encountered.");
            },
            success: function(data) {

                $("#idnumber").val('');
                $("#firstname").val('');
                $("#lastname").val('');
                $("#middleinitial").val('');
                $("#role").val('');
                $('input[type=radio]').prop('checked',false);
                $("#email").val('');
                $("#password").val('');
                $("#confirmpassword").val('');
                $("#thankyou").append("<br><br><h3>Thank you and we welcome you to the community.</h3><br>");
                $("#thankyou").append("<p>Click <a href='login/'>here</a> to login</p>")
                Cookies.set("new_user", '1'); // Tell the system that it is a new user
            }
        });
    } else
        alert("Passwords do not match.");

};


function show_feedbacks(thesis_id) {

    $("#feedbacks").empty();

    // Retrive all feedbacks of the thesis which matches the thesis_id
    $.ajax({
        url: '/api/thesis/' + thesis_id + '/feedback',
        type: 'get',
        dataType: 'json',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
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


function add_feedback() {
    var body = $("#feedback").val();
    var thesis_id = Cookies.get('thesis_id');
    var user_id = Cookies.get("idnumber"); // idnumber is a cookie set upon log in

    $.ajax({
        url: '/api/thesis/feedback',
        type: 'post',
        dataType: 'json',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        data: {
            body: body,
            user_id: user_id,
            thesis_id: thesis_id
        },

        error: function() {

            alert("An error was encountered.");
        },
        success: function(data) {
            $("#feedback").val('');
        }
    });

    // Retrive all feedbacks of the thesis which matches the thesis_id
    $.ajax({
        url: '/api/thesis/' + thesis_id + '/feedback',
        type: 'get',
        dataType: 'json',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {
            $("div").append("<h1>error</h1>");
        },
        success: function(data) {

        }
    });

    show_feedbacks(thesis_id);

};


function update_feedback(feedback_id) {

    // This function will be called when the user is done editing the feedback body
    // and hits the 'Update' button

    var thesis_id = Cookies.get('thesis_id');
    var user_id = Cookies.get('idnumber');
    var body = $("#updatefeedbackForm-" + feedback_id).val();

    $.ajax({
        url: '/api/thesis/' + thesis_id + '/feedback/' + feedback_id,
        type: 'put',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        data: {
            body: body,
            user_id: user_id
        },
        success: function() {
            $("#" + feedback_id).empty();
            $("#edit-feedback-" + feedback_id).show();
        }
    });

    show_feedbacks(thesis_id);
};


function edit_feedback(feedback_id) {

    // This function will be called whenever the user clicks the 'edit feedback' link

    var thesis_id = Cookies.get('thesis_id');
    var feedback_body;
    var feedback_id = String(feedback_id);
    var i = 0;

    $.ajax({
        url: '/api/thesis/' + thesis_id + '/feedback',
        type: 'get',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        success: function(data) {

            while (i < data['count']) {
                if (feedback_id == data['entries'][i]['feedback_id']) {
                    $("#edit-feedback-" + feedback_id).hide(); // hide the 'edit feedback' link
                    $("#" + feedback_id).append("<form name='updateForm'><textarea id='updatefeedbackForm-" + feedback_id + "'></textarea></form><br><button class='btn btn-success' type='submit' onclick='update_feedback(" + feedback_id + ");'>Update</button>");

                    feedback_body = data['entries'][i]['body'];
                    // document.updateForm.updatefeedbackForm.value = feedback_body;
                    document.getElementById("updatefeedbackForm-" + feedback_id).value = feedback_body;
                    console.log(data['entries'][i]['body']);
                }

                i = i + 1;
            }

        }
    });

};


function clear_search() {
    $("#search-bar").val('');
};


function userprofile() {
    // Get the fullname of the logged in user and display it on the title

    var user_id = Cookies.get('idnumber');
    var user_name;

    $.ajax({
        url: '/api/user/' + user_id,
        type: 'get',
        success: function(data) {
            user_name = data['user_info']['firstname'] + ' ' + data['user_info']['middle_initial'] + '.' + ' ' + data['user_info']['lastname'];
            $("#title").empty();
            $("#title").append("Home | " + user_name);
        }

    });
}


function thesisinfo() {
    // Get the title of the thesis and display it on the title

    var thesis_id = Cookies.get('thesis_id');
    var thesis_title;

    $.ajax({
        url: '/api/thesis/' + thesis_id,
        type: 'get',
        success: function(data) {
            thesis_title = data['match']['thesis_name'];
            $("#title").empty();
            $("#title").append(thesis_title + " | Thesis Archive");
        }
    });
}


function uploadprofilepicture(photoid) {
    var user_id = Cookies.get('idnumber');
    var formdata = new FormData($("#photo"));
    var random = Math.random().toString();
    var image_version;

    formdata.append('photo', $("#photo")[0].files[0]);

    $.ajax({
        url: '/profilepicture/' + user_id,
        type: 'post',
        data: formdata,
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        success: function(data) {
            console.log("success");
            $("#profilepicturediv").empty();
            $("#profilepicturediv").append('<center><img id="profilepicture" alt="" src="static/profile_pictures/' + Cookies.get('idnumber') + '"  data-original-title="Usuario"></center><br><br>');
            $("#changeprofilepicturemodal").trigger("click");
            Cookies.set('new_user', '2'); // Prevent the default profile picture from showing
            $("#profilepicturediv").empty();
            // update the profile picture :)
            // $("#profilepicturediv").append('<center><img id="profilepicture" alt="" src="static/profile_pictures/' + Cookies.get('idnumber') + '"  data-original-title="Usuario"></center><br><br>');
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
                }
            });
        },
        processData: false, // tell jQuery not to process the data
        contentType: false // tell jQuery not to set contentType
    });
}


function get_user_records() {
    // Get the records of a user before updating

    var user_id = Cookies.get('idnumber');

    // Get the old records
    $.ajax({
        url: '/api/user/' + user_id,
        type: 'get',
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        success: function(data) {
            document.getElementById("firstname").value = data['user_info']['firstname'];
            document.getElementById("middleinitial").value = data['user_info']['middle_initial'];
            document.getElementById("lastname").value = data['user_info']['lastname'];
            document.getElementById("email").value = data['user_info']['email'];
            console.log("success");
        }

    });
}


function update_user() {
    var user_id = Cookies.get('idnumber');

    var firstname = $("#firstname").val();
    var middleinitial = $("#middleinitial").val();
    var lastname = $("#lastname").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var new_password = $("#new_password").val();
    var confirm_password = $("#confirm_password").val();
    var role = $("#rolechoice").val();
    role = '2';

    $.ajax({
        url: '/api/user/' + user_id,
        type: 'get',
        success: function(data) {
            role = data['user_info']['role'];
            console.log(role);
        },
        async: false
    });

    $.ajax({

        url: '/api/user/update/' + user_id,
        type: 'put',
        data: {
            firstname: firstname,
            middleinitial: middleinitial,
            lastname: lastname,
            email: email,
            password: password,
            new_password: new_password,
            confirm_password: confirm_password,
            role: role
        },
        headers: {
            "Authorization": "bearer " + Cookies.get("token")
        },
        error: function() {
            console.log("error");
        },
        success: function(data) {

            console.log("success");
            console.log(role);
            reload_user();

        },
        async: false
    });

}


function close_modal(id) {
    $("#" + id).modal('hide');
}


function reload_user() {
    // Profile picture

    if (Cookies.get('idnumber') == Cookies.get('viewuser')) {
        html = '<div class="row">' +
            '<div class="col-md-6">' +
            '<button id = "uploadmodalopen" type="button"  onclick="placeid();" class="btn btn-success" data-toggle="modal" data-target="#uploadModal" data-whatever="@mdo">' +
            'Share Thesis' +
            '</button>' +
            '&nbsp;&nbsp;' +
            '</div>' +
            '</div>';

        $("#sharethesis").empty();
        $("#sharethesis").append(html);
    }

    $("#idnumberlabel").empty();
    $("#fnamelabel").empty();
    $("#lnamelabel").empty();
    $("#mnamelabel").empty();
    $("#emaillabel").empty();
    $("#role").empty();
    $("#editprofile").empty();

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
            $("#idnumberlabel").append(Cookies.get('idnumber'));
            $("#fnamelabel").append(data.user_info.firstname);
            $("#lnamelabel").append(data.user_info.lastname);
            $("#mnamelabel").append(data.user_info.middle_initial);
            $("#emaillabel").append(data.user_info.email);
            $("#role").append(data.user_info.role);
            $("#editprofile").append('<a href="#" onclick="get_user_records();" data-toggle="modal" data-target="#editprofileModal"><u>Edit Profile<u></a>');
            
        }

    });

}


