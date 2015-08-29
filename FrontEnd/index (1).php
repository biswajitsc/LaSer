<?php
    include_once 'genericFunctions.php';
?>

<!DOCTYPE html>
<meta charset="utf-8">

<head>
  <title>LaSer</title>
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="css/font-awesome.min.css">
  <link rel="stylesheet" href="css/index.css">
  <script src="js/jquery-1.11.0.min.js"></script>
</head>

<nav id="navBar" class="navbar navbar-static" role="navigation">
	<div class="navbar-header">
		<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
		  <span class="sr-only">Toggle navigation</span>
		  <span class="icon-bar"></span>
		  <span class="icon-bar"></span>
		  <span class="icon-bar"></span>
		</button>
		<a class="navbar-brand" href="index.php">LaSer</a>
	</div>

	<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
		<ul class="nav navbar-nav">
		  <li class= "active" ><a href="index.php">Home</a></li>
		  <li class= "" ><a href="about.php">About</a></li>
		</ul>
	</div>
</nav>

<body>

	<div class="container">
		
		<div class="row">
	        <div class="col-sm-6 col-sm-offset-3">
	            <div id="imaginary_container"> 
	                <div class="input-group stylish-input-group">
	                <form id="mathSnippetForm" action="index.php">
	                    <input type="text" name = 'mathSnippet' class="form-control" placeholder="Search" >
	                </form>    
	                <span class="input-group-addon">
	                   	<button id="submitButton" type="submit">
	                       	<span class="glyphicon glyphicon-search"></span>
	                   	</button>  
	                </span>
	                </div>
	            </div>
	        </div>
		</div>

		<div class="ranked-results">

            <?php
                $url = "localhost:8080"; //Put the url here
                $mathSnippet = $_GET['mathSnippet'];
                $mathSnippet = urlencode($mathSnippet);
                $mathSnippet = str_replace('+', '%20', $mathSnippet);
                $resultJson = httpGet($url,$mathSnippet);

                foreach ($resultJson as $key => $value) {
                    // echo $value['original_eqn'];
                    echo '<div class="hr-line-dashed"></div>';
                    echo '<div class="search-result">';
                    //echo $value['docID'];
                    echo '<center><a href='.'http://arxiv.org/abs/hep-th/'.$value['original_doc_id'].' target="_blank">'.$value['original_doc_id'].'</a></center>';
                    echo $value['original_eqn'];
                    echo $value['score'];
                    echo '</div>';
                }

                echo '<div class="hr-line-dashed"></div>';
            ?>
			
		</div>

		<div id="paginationDiv" class="text-center">
            <div class="btn-group">
                <button class="btn btn-white">First</button>
                <button class="btn btn-white" type="button"><i class="glyphicon glyphicon-backward"></i></button>
                <button class="btn btn-white" type="button"><i class="glyphicon glyphicon-chevron-left"></i></button>
                <button class="btn btn-white">1</button>
                <button class="btn btn-white">2</button>
                <button class="btn btn-white">3</button>
                <button class="btn btn-white">4</button>
                <button class="btn btn-white">5</button>
                <button class="btn btn-white">6</button>
                <button class="btn btn-white">7</button>
                <button class="btn btn-white" type="button"><i class="glyphicon glyphicon-chevron-right"></i> </button>
                <button class="btn btn-white" type="button"><i class="glyphicon glyphicon-forward"></i></button>
                <button class="btn btn-white">Last</button>
            </div>
        </div>

    </div>

    <script type="text/javascript">
    
    $('#submitButton').click(function() {
    $( "#mathSnippetForm" ).submit();
    });

    </script>


    
</body>
