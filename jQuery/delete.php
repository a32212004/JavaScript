<?php
	print_r($_GET);
	$link = mysqli_connect("127.0.0.1","root","","user") or die("無法連接資料庫".mysqli_error());
	$query = "delete from user where id = '".$_GET['id']."'";
	$result = mysqli_query($link,$query) or die("無法送出".mysqli_error());

	echo "<script>alert('刪除成功');</script>";
	echo "<script>location.href='list.php'</script>";
	
	
?>