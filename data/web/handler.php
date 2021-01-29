<?php
//$myfile = fopen("../../settings.json", "r");
$text = file_get_contents ("../../settings.json");
$text2=shell_exec('sudo python3 -m mh_z19 --all');
$ssid = shell_exec('sudo su -c "wpa_cli status | grep ^ssid="');
$json = json_decode($text, true);
$json2 = json_decode($text2, true);
$temp = intval($json2["temperature"])-3;
$json["temperature"]=$temp;
$ssid = substr($ssid, 5, -1);
$json2["ssid"]=$ssid;
$json3 =$json + $json2;
$response = json_encode($json3);
echo $response;
//fclose($myfile);
?>
