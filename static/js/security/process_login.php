<?php

include 'db_connect.php';
include 'functions.php';
sec_session_start(); // Our custom secure way of starting a php session. 
 
if(isset($_POST['email'], $_POST['p'])) { 
   $email = $_POST['email'];
   $password = $_POST['p']; // The hashed password.
   if(login($email, $password, $mysqli) == true) {
      // Login success
      echo 'Success: You have been logged in!';
   } else {
      // Login failed
      echo 'Login Failed';
      print_r(error_get_last());   }
} else { 
   // The correct POST variables were not sent to this page.
   echo 'Invalid Request';
}
?>