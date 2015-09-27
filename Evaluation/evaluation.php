<?php

ini_set('display_errors', 1);
include 'sql-helper.php';

$userid = $_COOKIE['userid'];
$username = $_COOKIE['username'];
$counter = $_COOKIE['counter'];
$lorqid = unserialize($_COOKIE['lorqid']);

if( count($lorqid) === ($counter - 1) )
{
	header("Location: thanks.php");
	die();
}
$qid = $lorqid[$counter - 1]['id'];

$query = "SELECT value FROM queries WHERE id = " . $qid . " LIMIT 1";
$result = db_select($query);
if($result === false) die("SQL Error: " . db_error());
$qval = $result[0]['value'];

?>

<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<style type="text/css"> th, td { text-align: center; } </style>

	<title> LaSer Evaluation Engine </title>
</head>

<body>
	<table class="table table-bordered">
		<tr>
			<td>
				<div>
					Query : <?php echo $qval; ?> 
				</div>
			</td>
			<td>
				<div>
					User : <?php echo trim($username, '\''); ?> 
				</div>
			</td>
		</tr>
	</table>
	
	<hr class="colorgraph">

	<form action = "eval-submit.php" method = "post">
		<table class="table table-bordered">
			<tr>
				<th colspan=5> SYSTEM X </th>
				<th colspan=5> SYSTEM Y </th>
			</tr>
			<tr>
				<th> Rank </th>
				<th> PID </th>
				<th> Paper </th>
				<th> Context </th>
				<th> Relevance </th>

				<th> Rank </th>
				<th> PID </th>
				<th> Paper </th>
				<th> Context </th>
				<th> Relevance </th>
			</tr>
			<?php
				$systems = array(0, 1);
				shuffle($systems);
				$x = $systems[0];
				$y = $systems[1];
				echo '<input type="hidden" name="x-value" value="' . strval($x) . '"/> <input type="hidden" name="y-value" value="' . strval($y) . '"/>';

				$query = "SELECT * FROM modelresults WHERE qid = " . $qid . " and systyp = '" . strval($x) . "' ORDER BY rank";
				$systemx = db_select($query);
				if($systemx === false) die("SQL Error: " . db_error());

				$query = "SELECT * FROM modelresults WHERE qid = " . $qid . " and systyp = '" . strval($y) . "' ORDER BY rank";
				$systemy = db_select($query);
				if($systemy === false) die("SQL Error: " . db_error());

				$mincount = min(count($systemx), count($systemy));
				echo '<input type="hidden" name="mincount" value="' . strval($mincount) . '"/>';
				for($i = 0; $i < $mincount; $i++)
				{
					$query = "SELECT * FROM papers WHERE id = " . trim($systemx[strval($i)]['pid'], '\'');
					$result = db_select($query);
					if($result === false) die("SQL Error: " . db_error());
					$paperxval = $result['0']['value'];

					$query = "SELECT * FROM papers WHERE id = " . trim($systemy[strval($i)]['pid'], '\'');
					$result = db_select($query);
					if($result === false) die("SQL Error: " . db_error());
					$paperyval = $result['0']['value'];

					echo '
						<tr>
							<td> ' . $systemx[strval($i)]['rank'] . ' </td>
							<input type="hidden" name="oldrank-x-' . strval($i) . '" value="' . $systemx[strval($i)]['rank'] . '"/>
							<td> ' . $systemx[strval($i)]['pid'] . ' </td>
							<input type="hidden" name="pid-x-' . strval($i) . '" value="' . $systemx[strval($i)]['pid'] . '"/>
							<td> ' . $paperxval . ' </td>
							<td> ' . $systemx[strval($i)]['context'] . ' </td>
							<td> <input type="range" min="0" max="2" step="1" value="1" name = "rel-bar-x-' . strval($i) . '"/> </td>

							<td> ' . $systemy[strval($i)]['rank'] . ' </td>
							<input type="hidden" name="oldrank-y-' . strval($i) . '" value="' . $systemy[strval($i)]['rank'] . '"/>
							<td> ' . $systemy[strval($i)]['pid'] . ' </td>
							<input type="hidden" name="pid-y-' . strval($i) . '" value="' . $systemy[strval($i)]['pid'] . '"/>
							<td> ' . $paperyval . ' </td>
							<td> ' . $systemy[strval($i)]['context'] . ' </td>
							<td> <input type="range" min="0" max="2" step="1" value="1" name = "rel-bar-y-' . strval($i) . '"/> </td>
						</tr>';
				}
			?>
			<tr>
				<th colspan=10>
					<button type="submit" class="btn btn-primary">Submit</button>
		    	</th>
			</tr>
		</table>
	</form>
</body>