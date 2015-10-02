<?php
ini_set('display_errors', 1);
include 'sql-helper.php';

require_once "json-util.php";

if( !empty($_GET['prefix']) )
{
	$prefix = db_noquote($_GET['prefix']);

	$query = "SELECT name FROM users WHERE name LIKE '" . $prefix . "%'";
	$result = db_select($query);
	if($result === false) die('SQL Error: ' . db_error());

	echo json_encode(array_slice($result, 0, 5));
}
?>