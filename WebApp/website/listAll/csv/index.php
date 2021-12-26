<html>
    <head>
        <title>Brevets Data</title>
    </head>

    <body>

        <h1>List of brevets</h1>
        <table border="0" cellspacing="2" cellpadding="2">
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
            if (array_key_exists('top', $_GET)) {
              $top = $_GET['top'];
            } else {
              $top = 9999;
            }

            $json = file_get_contents('http://api-service/listAll?top='.$top);
            $obj = json_decode($json);
            $brevets = $obj->brevets;
            foreach ($brevets as $brv) {
                foreach ($brv->controls as $ctrl) {
                  echo '<tr>
                            <td>'.$brv->distance.'</td>
                            <td>'.$brv->begin_date.'</td>
                            <td>'.$brv->begin_time.'</td>
                            <td>'.$ctrl->km.'</td>
                            <td>'.$ctrl->mi.'</td>
                            <td>'.$ctrl->location.'</td>
                            <td>'.$ctrl->open.'</td>
                            <td>'.$ctrl->close.'</td>
                        </tr>';

                  // echo '<td>'.$ctrl->DNE.'</td>'
                  // Throws Undefined property: stdClass::$DNE error
                  // Need to find out how to check for keys
                }
            }
            ?>
        </table>
    </body>
</html>
