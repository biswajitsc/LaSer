<?php

function httpGet($theUrl,$mathSnippet)
{
    $curl = curl_init(theUrl.mathSnippet);
    $result = curl_exec($curl);
    $result = '1';
    return $result;
}

?>