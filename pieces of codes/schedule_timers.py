# import schedule
# import time
#
threadlocal={}
def job(task_uuid, start_time):
    print("I'm changing DB[%s, %s]..." % (task_uuid, start_time))

def api(uuid):
	from threading import Timer
	t = Timer(2, job, args=["WOW", "2"])
	t.start()
	print("api: [%s]" % t)
	global threadlocal
	threadlocal[uuid] = t

def api2():
	print("api2: [%s]" % threadlocal)
	threadlocal[1].cancel()
	print("api2(after cancel 1): [%s]" % threadlocal)


api(1)
api(2)
api(3)
api2()

