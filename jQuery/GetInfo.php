<?php
	$link = mysqli_connect("127.0.0.1","root","","user") or die("無法連接資料庫".mysqli_error());
	
	
	foreach($_GET as $key => $value){
		$$key = $value;
		if($value == ""){
			@$error_msg .= "$key is empty; ";
		}
	}

	
	if(@$error_msg != ""){
		echo "0";
	}else{
		$query = "INSERT INTO user (account, password, name, mail)
		VALUES('$account','$password','$name','$mail')";
		
		$result = mysqli_query($link,$query) or die("無法送出".mysqli_error());
		
		echo "1";
	}

	
//http://127.0.0.1/user/GetInfo.php?sensor_name=空氣感測器&sensor_value=111
//http://127.0.0.1/user/GetInfo.php?account=ggg&password=111&name=111&mail=111@gmail.com
?>

