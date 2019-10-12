import nhdk

while(1):
	if nhdk.runApp() == 1:
		print("1 Restart Program")
		continue
	else:
		print("0 Exit Program")
		break
