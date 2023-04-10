import socket_server_control, socket_server_msg

socket_server_msg.MSGServer().start()
socket_server_control.ControlServer().start()