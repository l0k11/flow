from setup.setup_server import setup
import threads.server_control as control, threads.server_msg as msg

setup()

msg.MSGServer().start()
control.ControlServer().start()