# Facility Management System - webSCADA

Application is a webSCADA system written in Python and JavaScript. Backend is made in Flask micro-framework and frontend is based on JavaScript (JQuery) and Bootstrap v5.

To connect to devices supporting OPC UA standard asynchronous tasks were used. Connection is based on python-opcua module.

Admin user can manage devices and users (add, delete), normal non-admin user is only permitted to view visualized data from connected devices.

Application uses two databases - one relational (SQLite) and one non-relational (MongoDB). First one is used to save user and devices data, second one is used as a container for acquised data from devices.

Dashboard shows data in real-time, refreshing interval is set to 0.3s.

This project is a result of engineering work at the Rzeszów University of Technology.

<hr>
Some screenshots from application:
<hr>
<div align="center">
  <a href="https://ibb.co/mBwkKPn"><img src="https://i.ibb.co/Sx8bgZk/1.png" alt="1" border="0"></a>
  <p align="center"><i>Sign In page</i> </p>
  
  <a href="https://ibb.co/94Dz4M4" align="center"><img src="https://i.ibb.co/M1vW1X1/2.png" alt="2" border="0"></a>
  <p align="center"><i>Dashboard</i></p>
  
  <a href="https://ibb.co/CwFpc0y"><img src="https://i.ibb.co/VL801BG/3.png" alt="3" border="0"></a>
  <p align="center"><i>Device adding panel</i></p>
  
  <a href="https://ibb.co/KyzXmKf"><img src="https://i.ibb.co/pXrxnhM/4.png" alt="4" border="0"></a>
  <p align="center"><i>Device management panel</i></p>
  
  <a href="https://ibb.co/LPKYhkR"><img src="https://i.ibb.co/W3CGpx5/5.png" alt="5" border="0"></a>
  <p align="center"><i>User adding panel</i></p>
</div>
