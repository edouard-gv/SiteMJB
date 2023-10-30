<?php
//fichier à mettre dans wp-content/uploads/inventaire/
$repertoire_images = getcwd();
foreach (new DirectoryIterator($repertoire_images) as $fileInfo) {
    if($fileInfo->isDot()) continue;
    echo $fileInfo->getFilename() . "<br>\n";
}
?>