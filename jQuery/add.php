<?php
	$link = mysqli_connect("127.0.0.1","root","","user") or die("無法連接資料庫".mysqli_error());
	
	
	foreach($_GET as $key => $value){
		$$key = $value;
		if($value == ""){
			$error_msg .= "$key is empty; ";
		}
	}
	
	/*
	$query = "INSERT INTO user (account, password, name, mail)
	VALUES('".$_GET['account']."','".$_GET['password']."','".$_GET['name']."','".$_GET['mail']."')";
	*/
	
	if($error_msg != ""){
		echo "<script>alert('$error_msg');</script>";
		echo "<script>history.go(-1);</script>";
	}else{
		$query = "INSERT INTO user (account, password, name, mail)
		VALUES('$account','$password','$name','$mail')";
		
		$result = mysqli_query($link,$query) or die("無法送出".mysqli_error());
		
		echo "<script>alert('新增成功');</script>";
		echo "<script>location.href='list.php'</script>";
	}



?>