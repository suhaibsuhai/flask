
const SUBMIT = $("#submit");

const USERNAME = $("#uname");
const USERNAME_MSG = $("#user-msg");

const PASSWORD = $("#pwd");
const PASSWORD_MSG = $("#password-msg");

const CONFIRM = $("#confirmpwd");
const CONFIRM_MSG = $("#confirm-msg");

const FNAME = $("#fname");
const FNAME_MSG = $("#fname-msg");

const LNAME = $("#lname");
const LNAME_MSG = $("#lname-msg");

const EMAIL = $("#email");
const EMAIL_MSG = $("#email-msg");

function reset_form() {
    USERNAME_MSG.html("");
    USERNAME_MSG.hide();
    PASSWORD_MSG.html("");
    PASSWORD_MSG.hide();
    CONFIRM_MSG.html("");
    CONFIRM_MSG.hide();
    LNAME_MSG.html("");
    LNAME_MSG.hide();
    FNAME_MSG.html("");
    FNAME_MSG.hide();
    EMAIL_MSG.html("");
    EMAIL_MSG.hide();
    SUBMIT.show();
}

function validate() {
    let valid = true;
    reset_form();
    SUBMIT.hide();


    if (!USERNAME.val() || USERNAME.val().length < 5) {

        USERNAME_MSG.html("Username must be of atleast five characters");
        USERNAME_MSG.show();
        console.log("Bad username");
        valid = false;
    }


    if (USERNAME.val() != USERNAME.val().toLowerCase()) {
        USERNAME_MSG.html("Username must be in lowercase");
        USERNAME_MSG.show();
        valid = false;
    }

    if (!PASSWORD.val() || PASSWORD.val().length < 8) {
        PASSWORD_MSG.html("Password must be at least eight characters long");
        PASSWORD_MSG.show();
        valid = false;
    }

    if (!CONFIRM.val() || PASSWORD.val() != CONFIRM.val()) {
        CONFIRM_MSG.html("Enetered Passwords donot match");
        CONFIRM_MSG.show();
        valid = false;
    }

    if (!FNAME.val()) {
        FNAME_MSG.html("First Name cannot be empty");
        FNAME_MSG.show();
        valid = false;
    }

    if (!LNAME.val()) {
        LNAME_MSG.html("Last Name cannot be empty");
        LNAME_MSG.show();
        valid = false;
    }

    var x = EMAIL.val().trim();
    var atpos = x.indexOf("@");
    var dotpos = x.lastIndexOf(".");
    if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= x.length) {
        EMAIL_MSG.html("Enter a valid email address");
        EMAIL_MSG.show();
        valid = false;
    }

    if (valid) {
        reset_form();
    }
}

$(document).ready(validate);
USERNAME.change(validate);
PASSWORD.change(validate);
CONFIRM.change(validate);
LNAME.change(validate);
FNAME.change(validate);
EMAIL.change(validate);
