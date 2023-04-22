import pathlib, threads.server_control as control,\
    threads.server_msg as msg, functions.setup as setup,\
    threads.server_check_status as cs

settings = setup.server_setup()
msg.MSGServer(f"{pathlib.Path.home()}/.flow-server/").start()
control.ControlServer(f"{pathlib.Path.home()}/.flow-server/").start()
cs.CheckStatus(f"{pathlib.Path.home()}/.flow-server/.db").start()