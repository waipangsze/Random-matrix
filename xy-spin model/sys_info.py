import os, platform, subprocess, re
import psutil

def sysinfo():

	print('='*50)
	pid = os.getpid()
	py = psutil.Process(pid)
	memoryUse = py.memory_info()[0]/2.**30
	print('PID = ', pid)
	print('Total memory = ', psutil.virtual_memory().total/(1024**3), ' GB')
	print('Memory use = ', memoryUse, ' GB') # memory use in GB...I think


	print('='*50)
	print('Psutil cpu count = ', psutil.cpu_count())
	print('Psutil cpu count (logical=False) = ', psutil.cpu_count(logical=False))

	def cpu():
		command = "cat /proc/cpuinfo"
		all_info = subprocess.check_output(command, shell=True).decode('utf8').strip()
		for line in all_info.split("\n"):
			if "model name" in line:
				print( re.sub( ".*model name.*:", "", line,1))
		return ""
	cpu()

	print('='*50)
	print('Uname = ', platform.uname())

	#Returns a tuple (bits, linkage) which contain information about the bit architecture and the linkage format used for the executable. Both values are returned as strings.
	print('Architecture = ', platform.architecture())

	#Returns the machine type, e.g. 'i386'. An empty string is returned if the value cannot be determined.
	print('Machine = ', platform.machine())

	#Returns a single string identifying the underlying platform with as much useful information as possible.
	print('Platform = ', platform.platform())

	#Returns a string identifying the compiler used for compiling Python.
	print('Python compiler = ', platform.python_compiler())

	#Returns a string identifying the Python implementation SCM branch.
	print('Python branch = ', platform.python_branch())

	#Returns a string identifying the Python implementation. Possible return values are: ‘CPython’, ‘IronPython’, ‘Jython’, ‘PyPy’.
	print('Python implementation = ', platform.python_implementation())

	print('Python version = ', platform.python_version())

	#Returns the system’s release version, e.g. '#3 on degas'. An empty string is returned if the value cannot be determined.
	print('system release version = ', platform.version())

	#Tries to determine the name of the Linux OS distribution name.
	print('Linux distribution = ', platform.linux_distribution())

	#Tries to determine the libc version against which the file executable (defaults to the Python interpreter) is linked. Returns a tuple of strings (lib, version) which default to the given parameters in case the lookup fails.
	print('Libc ver = ', platform.libc_ver())
	
	print('='*50)

