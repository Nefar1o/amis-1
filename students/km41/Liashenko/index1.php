<?php
    //  ��� ��������� �������� �� �������. ������ � ��� �������� ������  ������������, ���� �� ��������� �� �����. ����� ����� ��������� �� �  ����� ������ ���������!!!
    session_start();
    ?>
    <html>
    <head>
    <title>Site</title>
    </head>
    <body>
    <h2>Site</h2>
    <form action="testreg.php" method="post">

    <!--****  testreg.php - ��� ����� �����������. �� ����, ����� ������� �� ������  "�����", ������ �� ����� ���������� �� ��������� testreg.php �������  "post" ***** -->
 <p>
    <label>Login:<br></label>
    <input name="login" type="text" size="15" maxlength="15">
    </p>

    <p>

    <label>Password:<br></label>
    <input name="password" type="password" size="15" maxlength="15">
    </p>

    <p>
    <input type="submit" name="submit" value="Go">

    <!--**** �������� (type="submit") ���������� ������ �� ��������� testreg.php ***** --> 
<br>
 <!--**** ������ �� �����������, ���� ���-�� �� ������ ����� ���� �������� ***** --> 

    </p></form>
    <br>
    <?php
    // ���������, ����� �� ���������� ������ � id ������������
    if (empty($_SESSION['login']) or empty($_SESSION['id']))
    {
    // ���� �����, �� �� �� ������� ������
    echo "Fuck you GOST<br><a href='#'>Call me baybe +380986218875</a>";
    }
    else
    {

    // ���� �� �����, �� �� ������� ������
    echo "All OK ".$_SESSION['login']."<br><a  href='http://tvpavlovsk.sk6.ru/'>GO</a>";
    }
    ?>
    </body>
    </html>