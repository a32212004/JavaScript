<?php
	
	$link = mysqli_connect("127.0.0.1","root","","user") or die("無法連接資料庫".mysqli_error());
	$query = "select * from user where id = '".$_GET['id']."'";
	$result = mysqli_query($link,$query) or die("無法送出".mysqli_error());
	
?>
<?php
	while($row = mysqli_fetch_array($result)){
?>

<html>
	<meta charset="utf-8">
	<form action="update.php" method="GET">
		帳號：<input type="text" name="account" value="<?=$row['account'];?>"><br>
		密碼：<input type="text" name="password" value="<?=$row['password'];?>"><br>
		姓名：<input type="text" name="name" value="<?=$row['name'];?>"><br>
		信箱：<input type="text" name="mail" value="<?=$row['mail'];?>"><br>
		<input type="hidden" name="id" value="<?=$row['id'];?>">
		<input type="submit" value="send">
	</form>

	
</html>	
<?php
	}	
	
?>