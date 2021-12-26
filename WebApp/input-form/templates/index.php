<html>
    <head>
        <title>Brevets Data</title>
    </head>

    <body>

        <h1>List of Brevets</h1>
        <table border="1" cellspacing="2" cellpadding="2">
        <tr>
            <td> <font face="Arial">Distance</font> </td>
            <td> <font face="Arial">Begin Date</font> </td>
            <td> <font face="Arial">Begin Time</font> </td>
            <td> <font face="Arial">Control (km)</font> </td>
            <td> <font face="Arial">Control (mi)</font> </td>
            <td> <font face="Arial">Control Location</font> </td>
            <td> <font face="Arial">Control Open Time</font> </td>
            <td> <font face="Arial">Control Close Time</font> </td>
        </tr>
            <?php
            $json = file_get_contents('http://api-service/listAll');
            $obj = json_decode($json);
            $brevets = $obj->brevets;
            foreach ($brevets as $brv) {
                foreach ($brv["control"] as $ctrl) {
                  echo '<tr>
                            <td>'.$brv["distance"].'</td>
                            <td>'.$brv["begin_date"].'</td>
                            <td>'.$brv["begin_time"].'</td>
                            <td>'.$ctrl["km"].'</td>
                            <td>'.$ctrl["mi"].'</td>
                            <td>'.$ctrl["location"].'</td>
                            <td>'.$ctrl["open"].'</td>
                            <td>'.$ctrl["close"].'</td>
                        </tr>';
                }
            }
            ?>
    </body>
</html>
