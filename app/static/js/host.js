var socket;
var files; //Variable to store your files


//Add events
$('input[type=file]').on('change', prepareUpload);


//Grab the files and set them to our variable
function prepareUpload(event) {
	files = event.target.files;
};


function register() {

	var email = $("#email").val();
    var firstname = $("#firstname").val();
    var middleinitial = $("#middleinitial").val();
    var lastname = $("#lastname").val();
    var contactno = $("#contactno").val();
    var address = $("address").val();
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

                $("#email").val('');
                $("#firstname").val('');
                $("#middleinitial").val('');
                $("#lastname").val('');
                $("#contactno").val('');
                $("#address").val('');
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
}