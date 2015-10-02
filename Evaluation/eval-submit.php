<?php

	ini_set('display_errors', 1);
	include 'sql-helper.php';

	$uid = $_COOKIE['userid'];
	$counter = $_COOKIE['counter'];
	$lorqid = unserialize($_COOKIE['lorqid']);
	$qid = $lorqid[$counter - 1]['id'];

	$x = db_quote($_POST['x-value']);
	$y = db_quote($_POST['y-value']);
	$cnt = db_noquote($_POST['mincount']);

	for($i = 0; $i < $cnt; $i++)
	{
		$systyp = $x;
		$oldrank = $i + 1;
		$newrank = db_noquote($_POST['newrank-x-' . strval($i)]);
		$pid = db_noquote($_POST['pid-x-' . strval($i)]);
		$relevant = db_quote($_POST['rel-bar-x-' . strval($i)]);
		$query = "INSERT INTO evalresults (uid, systyp, qid, oldrank, newrank, pid, relevant) 
			VALUES (" . $uid . ", " . $systyp . ", " . $qid . ", " . $oldrank . ", " . $newrank . ", " . $pid . ", " . $relevant . " )";
		$result = db_query($query);
		if($result === false) die("SQL Error: " . db_error());

		$systyp = $y;
		$oldrank = $i + 1;
		$newrank = db_noquote($_POST['newrank-y-' . strval($i)]);
		$pid = db_noquote($_POST['pid-y-' . strval($i)]);
		$relevant = db_quote($_POST['rel-bar-y-' . strval($i)]);
		$query = "INSERT INTO evalresults (uid, systyp, qid, oldrank, newrank, pid, relevant) 
			VALUES (" . $uid . ", " . $systyp . ", " . $qid . ", " . $oldrank . ", " . $newrank . ", " . $pid . ", " . $relevant . " )";
		$result = db_query($query);
		if($result === false) die("SQL Error: " . db_error());
	}

	setcookie('counter', $counter + 1, time() + 3600);
	header('Location: evaluation.php');
?>