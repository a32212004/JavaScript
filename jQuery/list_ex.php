<html>
<meta charset = "utf-8">


<body>
<a href="insert.php"><img src="https://www.clipartmax.com/png/middle/41-410376_add-item-comments-add-icon-png-white.png" height="20" > 新增</a>

<table border="1">
	<thead>
		<tr>
			<th>編號</th>
			<th>帳號</th>
			<th>密碼</th>
			<th>姓名</th>
			<th>信箱</th>
			<th>建立日期</th>
			<th>動作</th>
		</tr>
	</thead>

<tbody>
<?php
	$link = mysqli_connect("127.0.0.1","root","","user") or die("無法連接資料庫".mysqli_error());
	$query = "select*from user";
	$result = mysqli_query($link,$query) or die("無法送出".mysqli_error());
?>
<?php
	while($row = mysqli_fetch_array($result)){
?>
	
	<tr>
		<td><?=$row['id'];?></td> <!--?=：省略echo-->
		<td><?=$row['account'];?></td>
		<td><?=$row['password'];?></td>
		<td><?=$row['name'];?></td>
		<td><?=$row['mail'];?></td>
		<td><?=$row['datetime'];?></td>
		<td>
			<a href="edit.php?id=<?=$row['id'];?>"><img src="edit.png" height="20" width="20"> 修改</a>
			<a href="delete.php?id=<?=$row['id'];?>"><img src="delete.png" height="20" width="20"> 刪除</a>
		</td>
	</tr>
	

<?php
	}
?>
</tbody>
</table>
</body>
<html>