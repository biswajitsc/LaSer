<?php

function httpGet($theUrl,$mathSnippet)
{
    //$curl = curl_init(theUrl.mathSnippet);
    //$result = curl_exec($curl);
    $result = '[';
    for($i = 0; $i < 4; $i ++) {
    	$result .= '{';
    	$result .= '"docID":"docID-'.$i.'",';
    	$result .= '"docLink":"docLink-'.$i.'",';
    	$result .= '"equation":"';
    	$result .= '<math xmlns:m=\"http://www.w3.org/1998/Math/MathML\" display=\"block\">   <mrow>     <mi mathvariant=\"normal\">Λ</mi>     <mo>=</mo>     <mrow>       <mfenced open=\"(\" close=\")\">         <mrow>           <mi>T</mi>           <mo>⁢</mo>           <mi>T</mi>         </mrow>       </mfenced>       
    	<mo>-</mo>       <mrow>         <mfrac>           <mn>3</mn>           <mn>10</mn>         </mfrac>         <mo>⁢</mo>         <mrow>           
 	<msup>             <mo>∂</mo>             <mn>2</mn>           </msup>           <mo>⁡</mo>           <mi>T</mi>         </mrow>       </mrr
	ow>     </mrow>   </mrow> </math>';
		$result .= '"}';

    	if($i < 3) $result .= ',';
    }
    $result .= ']';
    $resultJson = json_decode($result, true);
    return $resultJson;  
}

?>