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
  <script type="text/javascript" src="js/MathJax.js?config=MML_HTMLorMML-full"></script>
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
 
        <div>

            <?php
                $varString = '<m:math xmlns="http://www.w3.org/1998/m:Math/m:MathML" display="block">
  <m:mi>x</m:mi> <m:mo>=</m:mo>
  <m:mrow>
    <m:mfrac>
      <m:mrow>
        <m:mo>−</m:mo>
        <m:mi>b</m:mi>
        <m:mo>±</m:mo>
        <m:msqrt>
          <m:msup><m:mi>b</m:mi><m:mn>2</m:mn></m:msup>
          <m:mo>−</m:mo>
          <m:mn>4</m:mn><m:mi>a</m:mi><m:mi>c</m:mi>
        </m:msqrt>
      </m:mrow>
      <m:mrow> <m:mn>2</m:mn><m:mi>a</m:mi> </m:mrow>
    </m:mfrac>
  </m:mrow>
  <m:mtext>.</m:mtext>
</m:math>';
            
            echo str_replace('m:', '', $varString);

                echo '<div class="hr-line-dashed"></div>';
            ?>
            <!-- <div id="paginationDiv" class="text-center">
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
            </div> -->
 
    </div>
 
 
 
   
</body>