<?php

ini_set('display_errors', 1);
include 'sql-helper.php';

$userid = $_COOKIE['userid'];
$username = $_COOKIE['username'];

$query = "UPDATE users SET state = '1' WHERE id = " . $userid;
$result = db_query($query);
if($result === false) die("SQL Error: " . db_error());

?>

<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<style type="text/css"> div { text-align: center; vertical-align: center;} </style>

	<title> LaSer Evaluation Engine </title>
</head>

<body>
	<div>
		<br/>
		<img height="80%" src="http://www.remarkableriverrun.com/wp-content/uploads/2014/05/20-thank-you.jpg"/> <br/>
		<h4> <em>Thank you! <?php echo trim($username, '\''); ?>. Your response has been successfully recorded.</em> </h4>
	</div>
</body>