<?php

define("HOST", "localhost"); // The host you want to connect to.
define("USER", "ironworks_admin"); // The database username.
define("PASSWORD", "8IYdYXdtLb4gZoH3"); // The database password.
define("DATABASE", "desktop"); // The database name.

$mysqli = new mysqli(HOST, USER, PASSWORD, DATABASE);
// If you are connecting via TCP/IP rather than a UNIX socket remember to add the port number as a parameter.