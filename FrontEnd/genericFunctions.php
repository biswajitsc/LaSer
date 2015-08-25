<?php

function httpGet($theUrl,$mathSnippet)
{
    //$curl = curl_init(theUrl.mathSnippet);
    //$result = curl_exec($curl);
    $result = '{"docID":"file:///1",
    "equation": "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <math xmlns:m=\"http://www.w3.org/1998/Math/MathML\" display=\"block\">  <mrow>    <mrow>      <msubsup>        <mo>∫</mo>        <mrow>          <mi>x</mi>          <mo>=</mo>          <mn>1</mn>        </mrow>        <mrow>          <mi>x</mi>          <mo>=</mo>          <mn>2</mn>        </mrow>      </msubsup>      <mi>a</mi>    </mrow>    <mo>=</mo>    <mn>1</mn>  </mrow></math>"}';
    $resultJson = json_decode($result, true);
	return $resultJson;  
}

?>