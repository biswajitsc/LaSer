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
			<div class="hr-line-dashed"></div>
	        <div class="search-result">
		        <h3><a href="#">Bootdey</a></h3>
		        <a href="#" class="search-link">www.bootdey.com</a>
		        <p>

		        </p>
			</div>
			
			<div class="hr-line-dashed"></div>

            <div class="search-result">
                <h3><a href="#">Bootdey</a></h3>
                <a href="#" class="search-link">https://bootdey.com/</a>
                <p>
                  Bootdey is a gallery of free snippets resources templates and utilities for bootstrap css hmtl js framework.Codes for developers and web designers
                </p>
            </div>
            
            <div class="hr-line-dashed"></div>

            <div class="search-result">
                <h3><a href="#">Bootdey | Facebook</a></h3>
                <a href="#" class="search-link">https://www.facebook.com/bootdey</a>
                <p>
                    Bootdey is a gallery of free snippets resources templates and utilities for bootstrap css hmtl js framework. Codes for developers and web designers
                </p>
            </div>

            <div class="hr-line-dashed"></div>

            <div class="search-result">
                <h3><a href="#">Bootdey | Twitter</a></h3>
                <a href="#" class="search-link">www.twitter.com/bootdey</a>
                <p>
                    Bootdey is a gallery of free snippets resources templates and utilities for bootstrap css hmtl js framework. Codes for developers and web designers
                </p>
            </div>
            
            <div class="hr-line-dashed"></div>

            <div class="search-result">
                <h3><a href="#">Bootdey | Twitter</a></h3>
                <a href="#" class="search-link">www.twitter.com/bootdey</a>
                <p>
                    Bootdey is a gallery of free snippets resources templates and utilities for bootstrap css hmtl js framework. Codes for developers and web designers
                </p>
            </div>

            <div class="hr-line-dashed"></div>

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

    <?php    
        $url = "localhost:8080"; //Put the url here
        $mathSnippet = $_GET['mathSnippet'];
        $mathSnippet = urlencode($mathSnippet);
        $mathSnippet = str_replace('+', '%20', $mathSnippet);
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url . '/' . $mathSnippet);
        $result = curl_exec($curl);
        echo $result;
    ?>
    
</body>