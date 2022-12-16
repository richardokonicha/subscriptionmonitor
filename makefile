# @run
# ***python monitor.py



startrq : 
	rq worker --with-scheduler

forksafety:
	export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES