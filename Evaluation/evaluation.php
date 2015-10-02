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
	<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
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
		<table class="grid table table-bordered">
			<tr>
				<th> SYSTEM X </th>
				<th> SYSTEM Y </th>
			</tr>
			<?php
				$systems = array(0, 1);
				$systemlabels = array('x', 'y');
				shuffle($systems);
				$x = $systems[0];
				$y = $systems[1];
				echo '<input type="hidden" name="x-value" value="' . strval($x) . '"/> <input type="hidden" name="y-value" value="' . strval($y) . '"/>';
			?>
			<tr>
				<?php
					$systemResults = array();
					for($s = 0; $s < count($systems); $s++)
					{
						$query = "SELECT * FROM modelresults WHERE qid = " . $qid . " and systyp = '" . strval($systems[$s]) . "' ORDER BY rank";
						$systemResults[] = db_select($query);
						if($systemResults[$s] === false) die("SQL Error: " . db_error());
					}

					$mincount = count($systemResults[0]);
					for($s = 1; $s < count($systems); $s++)
						$mincount = min($mincount, count($systemResults[$s]));
					echo '<input type="hidden" name="mincount" value="' . strval($mincount) . '"/>';

					for($s = 0; $s < count($systems); $s++)
					{
						echo
						'<td>
							<table class="grid table table-bordered" class="sortab" id="sortable' . $systemlabels[$s] . '">
								<thead>
									<tr>
										<th> Rank </th>
										<th> PID </th>
										<th> Paper </th>
										<th> Context </th>
										<th> Relevance </th>
									</tr>
								</thead>
								<tbody>';

						// Generating the result-table contents
						for($i = 0; $i < $mincount; $i++)
						{
							$query = "SELECT * FROM papers WHERE id = " . trim($systemResults[$s][strval($i)]['pid'], '\'');
							$result = db_select($query);
							if($result === false) die("SQL Error: " . db_error());
							$paperval = $result['0']['value'];

							echo '<tr>
							<td> ' . $systemResults[$s][strval($i)]['rank'] . ' </td>
							<input type="hidden" class="newrank" name="newrank-'.$systemlabels[$s].'-'.strval($i).'" 
								value="'.$systemResults[$s][strval($i)]['rank'].'"/>
							<td> ' . $systemResults[$s][strval($i)]['pid'] . ' </td>
							<input type="hidden" name="pid-'.$systemlabels[$s].'-'.strval($i).'" value="'.$systemResults[$s][strval($i)]['pid'].'"/>
							<td> ' . $paperval . ' </td>
							<td> ' . $systemResults[$s][strval($i)]['context'] . ' </td>
							<td class="Center-Container"> <input class="rel-bar Absolute-Center" style="width:50%" type="range" min="0" max="2" step="1" value="1" name="rel-bar-'.$systemlabels[$s].'-'.strval($i).'"/> </td>
							</tr>';
						}

						echo
						'		</tbody>
							</table>
						</td>';
					}
				?>
			</tr>
			<tr>
				<th colspan=2>
					<button type="submit" class="btn btn-primary">Submit</button>
		    	</th>
			</tr>
		</table>
	</form>
	<script>
		// Assigns proper ranks to the reordered result list
		function setnewrank()
		{
			<?php for($s = 0; $s < count($systems); $s++)
			{
				echo '$("#sortable' . $systemlabels[$s] . '>tbody>tr").each(function( index, value ) {
				$(this).children(".newrank").get(0).value = index + 1; });';
			} ?>
			
		}

		// var fixHelper = function(e, ui) {
		// 	ui.children().each(function() {
		// 		$(this).width($(this).width());
		// 	});
		// 	return ui;
		// };

		$(document).ready(function() {
			// Implementation for drag 'n drop feature for reordering the results of a particular system
			// to use fixHelper use '{ helper: fixHelper }' as argument to sortable()
			<?php for($s = 0; $s < count($systems); $s++)
			{
				echo '$( "#sortable' . $systemlabels[$s] . ' tbody" ).sortable({cursor: "move", 
					stop: function(ev,ui){
						setnewrank();
						newrank = $(ui.item[0]).children(".newrank").get(0).value;
						myrel = $(ui.item[0]).find(".rel-bar").get(0).value;

						if(newrank > 1)
						{
							prevrel = $( "#sortable' . $systemlabels[$s] . '>tbody>tr" ).find(".rel-bar").get((newrank-1) - 1).value;
							if(prevrel < myrel)
							{
								$(this).sortable("cancel");
								setnewrank();
								return;
							}
						}

						if(newrank < ' . $mincount . ')
						{
							nextrel = $( "#sortable' . $systemlabels[$s] . '>tbody>tr" ).find(".rel-bar").get((newrank-1) + 1).value;
							if(nextrel > myrel)
							{
								$(this).sortable("cancel");
								setnewrank();
								return;
							}
						}
					}
				});
				$( "#sortable' . $systemlabels[$s] . ' tbody" ).disableSelection();';
			} ?>

			// Reordering the results when the user changes the value of relevance of a particular result
			<?php
				echo '$(".rel-bar").change(function(){
						myrow = $(this).parents("tr:first");
						myrank = parseInt($(myrow).children(".newrank").get(0).value);
						myrel = $(myrow).find(".rel-bar").get(0).value;

						while(myrank > 1)
						{
							prevrow = myrow.prev();
							prevrel = $(prevrow).find(".rel-bar").get(0).value;
							if(prevrel < myrel)
							{
								myrow.insertBefore(myrow.prev());
								myrank -= 1;
							} else break;
						}

						while(myrank < ' . $mincount . ')
						{
							nextrow = myrow.next();
							nextrel = $(nextrow).find(".rel-bar").get(0).value;
							if(nextrel > myrel)
							{
								myrow.insertAfter(myrow.next());
								myrank += 1;
							} else break;
						}

						setnewrank();
					});'
			?>
		});
	</script>
	<style type="text/css">
		.Center-Container {
		  position: relative;
		}

		.Absolute-Center {
		  width: 50%;
		  height: 50%;
		  overflow: auto;
		  margin: auto;
		  position: absolute;
		  top: 0; left: 0; bottom: 0; right: 0;
		}

		<?php for($s = 0; $s < count($systems); $s++)
		{
			echo '#sortable' . $systemlabels[$s] . ' tbody tr:hover {cursor: pointer;}';
			echo '#sortable' . $systemlabels[$s] . ' tbody tr.ui-sortable-helper {cursor: move;}';
		} ?>

		input[type=range]{
		    -webkit-appearance: none;
		}

		input[type=range]::-webkit-slider-runnable-track {
		    width: 300px;
		    height: 5px;
		    background: #ddd;
		    border: none;
		    border-radius: 3px;
		}

		input[type=range]::-webkit-slider-thumb {
		    -webkit-appearance: none;
		    border: none;
		    height: 16px;
		    width: 16px;
		    border-radius: 50%;
		    background: goldenrod;
		    margin-top: -4px;
		}

		input[type=range]:focus {
		    outline: none;
		}

		input[type=range]:focus::-webkit-slider-runnable-track {
		    background: #ccc;
		}
	</style>
</body>

