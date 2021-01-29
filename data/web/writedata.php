<?php
parse_str($_SERVER["QUERY_STRING"],$myArray);
$myfile = fopen("../../settings.json", "w");
fwrite($myfile, json_encode($myArray));
fclose($myfile);
echo "OK";
?>
