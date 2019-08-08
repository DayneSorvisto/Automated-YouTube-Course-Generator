/* eslint-disable func-names */
/* eslint-disable prefer-arrow-callback */


$(document).ready(function () {
  $('.left_box').hide();

  $('#first_name').keyup(function (e) {
    if ($('#first_name').val().length < 2) {
      $('#fname_result').html("At least 2 characters");
    }
    else {
      $('#fname_result').html("");
    }
  });


  $('#last_name').keyup(function (e) {
    if ($('#last_name').val().length < 2) {
      $('#lname_result').html("At least 2 characters");
    }
    else {
      $('#lname_result').html("");
    }
  });


  $('#register_email').keyup(function (e) {
    var data = $('#register_form').serialize()
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if ( !regex.test($('#register_email').val())) {
      $('#register_email_result').html("Please enter a valid email");
    }
    else{
      $('#register_email_result').html("");
      $.ajax({
        url: "/email_check",
        method: "POST",
        data: data
      })
      .done(function(res) {
          $('#register_email_result').html(res);
      })
    }
  });


  $('#confirm_password').keyup(function (e) {
    if ($('#password').val() != $('#confirm_password').val() ) {
      $('#password_result').html("Passwords must match");
    }
    else {
      $('#password_result').html("");
    }
  });


  $(document).on("submit", "#register_form", function (e) {
    var error = $('#password_result').html() || $('#register_email_result').html() || $('#lname_result').html() || $('#fname_result').html();
    if (error != "") {
      e.preventDefault();
      alert("Please fix all errors before submitting")
      // alert(error)
      return false;
    }
  });

  $('#start_registration').on('click', function () {
    $('.left_box').show();
    $('.right_box').hide();
  });

  $('#start_login').on('click', function () {
    $('.right_box').show();
    $('.left_box').hide();
  });
});
