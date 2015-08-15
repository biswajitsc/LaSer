<body>

<?php
$data = array(
	array(
		"token" => "fuck",
		"result" => array(
				array(
					"classifier" => "ADULT",
					"score"		=> 0.9
					)
			)
		),
	array(
		"token" => "damn",
		"result" => array(
				array(
					"classifier" => "ADULT",
					"score"		=> 0.25
					)
			)
		),
	);
	// echo json_encode($data); 
?>

<script src="jquery.min.js"></script>
<script src="jquery.xcolor.js"></script>
<h1>

<?php 
$i = 1;
foreach ($data as $word) {
	echo '<span id="'.$i.'">'. $word['token'] .'</span> ';
	$i += 1;
}

?>

</h1>

<script type="text/javascript">
function color(itemName, num) {
	$(itemName).colorize("green", "red", function() { return num;});
}

$(document).ready(function() {
	<?php
	$i = 1;
	foreach ($data as $word) {
		echo 'color("span#'.$i.'", '.$word['result'][0]['score'].'); ';
		$i += 1;
	}
	
	?>
});
</script>
</body?