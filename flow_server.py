import pathlib, threads.server_control as control,\
    threads.server_msg as msg, functions.setup as setup

settings = setup.server_setup()
msg.MSGServer(f"{pathlib.Path.home()}/.flow-server/").start()
control.ControlServer(f"{pathlib.Path.home()}/.flow-server/").start()