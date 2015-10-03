<?php

	ini_set('display_errors', 1);
	include 'sql-helper.php';

	$uid = $_COOKIE['userid'];
	$counter = $_COOKIE['counter'];
	$lorqid = unserialize($_COOKIE['lorqid']);
	$qid = $lorqid[$counter - 1]['id'];

	$nsystems = db_noquote($_POST['nsystems']);
	$ntopres = db_noquote($_POST['mincount']);

	for($s = 0; $s < $nsystems; $s++)
	{
		for($i = 0; $i < $ntopres; $i++)
		{
			$systyp = db_quote($_POST[chr($s + 65) . '-value']);
			$oldrank = $i + 1;
			$newrank = db_noquote($_POST['newrank-' . chr($s + 65) . '-' . strval($i)]);
			$pid = db_noquote($_POST['pid-' . chr($s + 65) . '-' . strval($i)]);
			$relevant = db_quote($_POST['rel-bar-' . chr($s + 65) . '-' . strval($i)]);
			$query = "INSERT INTO evalresults (uid, systyp, qid, oldrank, newrank, pid, relevant) 
				VALUES (" . $uid . ", " . $systyp . ", " . $qid . ", " . $oldrank . ", " . $newrank . ", " . $pid . ", " . $relevant . " )";
			$result = db_query($query);
			if($result === false) die("SQL Error: " . db_error());
		}
	}

	setcookie('counter', $counter + 1, time() + 3600);
	header('Location: evaluation.php');
?>