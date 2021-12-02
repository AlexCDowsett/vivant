<?php

// VIVANT PROJECT PHP Layer to allow Xcode communication with SQL database
// Created by Alex, Sam, Mihir
// USAGE: vivant-db.com/sql.php?password=<PASSWORD>&query=<SQL_QUERY>
// 		  (Replace <PASSWORD> and <SQL_QUERY> respectfully)

// Variables
$servername = 'vivant-db.c04gl03xq7f6.eu-west-2.rds.amazonaws.com';
$username = 'admin';
//$password = '8Am5v9Ni'; // REMOVE THIS IS FINAL
$password = $_GET['password'];
$dbname = 'Vivant_DB';

// Create connection
$con=mysqli_connect($servername, $username, $password, $dbname) or die ( mysqli_error($MySQL_Handle) );

// Check Character set is returned as utf8
$sSQL= 'SET CHARACTER SET utf8';
mysqli_query($con,$sSQL) or die ('Can\'t charset in database');

// Retrieve query from xcode (input)
$sql = $_GET['query'];

// SELECT STATEMENT
if (strlen(strpos($sql, "SELECT"))) {

	if ($result = mysqli_query($con, $sql)) {
		$resultArray = array();
		$tempArray = array();
 
		// Loop through each row in the result set
		while($row = $result->fetch_object())
		{
			// Add each row into our results array
			$tempArray = $row;
			array_push($resultArray, $tempArray);
		}
 
		// Finally, encode the array to JSON and output the results
		echo json_encode($resultArray);
	}
	
// INSERT STATEMENT
} elseif (strlen(strpos($sql, "INSERT"))) {

	if ($con->query($sql) === TRUE) {
		echo "New record created successfully";
	} else {
		echo "Error: " . $sql . "<br>" . $con->error;
		echo "<br> Note: SQL statement unreconigised, please check it is correct";
	}
	
// UPDATE STATEMENT
} elseif (strlen(strpos($sql, "UPDATE"))) {
	
	if ($con->query($sql) === TRUE) {
		echo "Records updated successfully";
	} else {
		echo "Error: " . $sql . "<br>" . $con->error;
		echo "<br> Note: SQL statement unreconigised, please check it is correct";
	}
	
// DELETE STATEMENT
} elseif (strlen(strpos($sql, "DELETE"))) {
	
	if ($con->query($sql) === TRUE) {
		echo "Records deleted successfully";
	} else {
		echo "Error: " . $sql . "<br>" . $con->error;
		echo "<br> Note: SQL statement unreconigised, please check it is correct";
	}
	
// OTHER STATEMENT
} else {
	
	if ($con->query($sql) === TRUE) {
		echo "SQL statement executed successfully";
	} else {
		echo "Error: " . $sql . "<br>" . $con->error;
		echo "<br> Note: SQL statement unreconigised, please check it is correct";
	}
	
}

// Close connection
$con->close();

?>


