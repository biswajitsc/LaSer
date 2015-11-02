<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="css/index.css">
	<script type="text/javascript">
	function loadlist(selobj, url, nameattr)
	{
		/*function to load a list from a JSON output generated from the query given as 'url'*/
		// selobj : element where the list is dumped
		// url : query that outputs JSON object to construct the list
		// nameattr : name of the field in the JSON object to use to construct the list
	    $(selobj).empty();
	    $.getJSON(url, {}, function(data)
	    {
	        $.each(data, function(i,obj)
	        {
	            $(selobj).append($('<option></option>').val(obj[nameattr]).html(obj[nameattr]));
	        });
	    });
	}
	</script>

	<title> LaSer Evaluation Engine </title>
</head>

<body>
	<h1> LaSer Evaluation Engine </h1>
	<div class="container" style="margin-top:50px">
		<div class="row" style="margin-top:20px" >
			<div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
				<form role = "form" autocomplete = "off" action = "init.php" method = "post">
					<fieldset>
						<div class="form-group">
				            <span class="input-group-addon"><span class="glyphicon glyphicon-user"></span></span>
			    			<input style="text-align: center;" type='text' name="username" id="username" class="form-control" 
			    				placeholder="Please Enter Your Name" list='user-list'>
				        </div>
				    	<div class="row" style="text-align: center;">
							<div class="col-xs-6 col-sm-6 col-md-6 col-sm-offset-2 col-md-offset-3">
								<button type="submit" class="btn btn-primary btn-block">Start Evaluation</button>
							</div>
				    	</div>
				    	<datalist id='user-list'></datalist>
					</fieldset>
				</form>
		    </div>
		</div>
	</div>

	<script type="text/javascript">
	// Generating drop down list of names of users from the database matching the user-name prefix entered
	$("#username").keyup(function(e)
	{
		if( !(e.which >= 37 && e.which <= 40) && e.which != 13 )
	   		loadlist($('datalist#user-list').get(0), 'get-users.php?prefix=' + $('#username').val(),'name');
	});
	</script>

	<div>
		<hr class="colorgraph">

		<div>
			<p>
				LaSer is a search engine for mathematical formulae. 
				<br/>The MathWebSearch system harvests the web for content representations (currently MathML) of formulae and indexes them using unigrams, 
				bigrams and trigrams.
				<br/>The query for now is limited to Latex format only and can and will be extended to free form queries. 
				<br/>Our Project can be found on <a href="https://github.com/biswajitsc/LaSer">GitHub.</a>
			</p>
		</div>

		<br/>

		<div>
			<h4> Guidelines for Evaluation </h4>
			<ul>
				<li> Each result can be marked as Relevant(2), Partially-Relevant(1) or Irrelevant(0) ;
					<br/>based on the extent of the relevance of the search query to the result (description of the paper + context) displayed. </li>
					<br/>
				<li> The ordering of the results can be modified to reflect the order of relevance among the search results, 
					<br/>with the most relevant results having the least rank (top most result). </li>
					<br/>
				<li> In case the same result (paper & context) is displayed multiple times then mark the first occourance as usual, and
					<br/>mark the rest of them as Irrelevant(0). </li>
			</ul>
		</div>
	</div>
</body>
