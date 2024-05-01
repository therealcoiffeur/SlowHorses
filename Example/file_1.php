<?php

$f = fopen($_GET["url"], "r");
$g = tmpfile();

while (!feof($f)) {
    $data = fread($f, 1024);
    fwrite($g, $data);
}

?>
