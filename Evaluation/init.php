<?php
ini_set('display_errors', 1);
include 'sql-helper.php';

$username = db_quote($_POST['username']);

$query = "SELECT * FROM users WHERE name = " . $username . " LIMIT 1";
$result = db_select($query);
if($result === false)
{
	die('SQL Error: ' . db_error());
}

if(count($result) === 0)
{
	echo 
		'<script language="javascript">
			alert("Username doesn\'t exist in the database!"); 
			window.location = "index.php";
		</script>';
	die();
}

$row = $result[0];
if($row['state'] === '1')
{
	echo 
		'<script language="javascript">
			alert("You have already filled the form. Thank You!"); 
			window.location = "index.php";
		</script>';
	die();
}
$userid = $row['id'];

$query = "SELECT * FROM queries WHERE id >= (SELECT FLOOR( MAX(id) * RAND()) FROM queries ) ORDER BY id LIMIT 3";
$lorqid = db_select($query);

if($lorqid === false)
{
	die('SQL Error: ' . db_error());
}

// foreach ($lorqid as $value) 
// {
// 	print_r($value);
// 	echo '<br/>';
// }

$exptime = time() + 3600;
setcookie('userid', $userid, $exptime);
setcookie('username', $username, $exptime);
setcookie('counter', 1, $exptime);
setcookie('lorqid', serialize($lorqid), $exptime);

header("Location: evaluation.php");
?>