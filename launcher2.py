import os
import sys
import time

def main():
	while(1):
		oscommand = os.popen("ps aux | grep nhdk.py | awk '{print $12}' ").readlines()
		check_p = '%s' % (oscommand[0])
		if (check_p.find("launcher.py") == -1 ):
			os.system("./launcher.py &")
		    
		try:
			time.sleep(3)
		except Exception, e:
		        print e
		        sys.exit()
								 
if __name__ == "__main__" :
	main()
		
