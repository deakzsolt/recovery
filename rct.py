import os, essentials, options, connections, socks, sys, shutil
from time import sleep
from pathlib import Path

target = os.getcwd()+'/'

print('\033[92m'+'---------------- Recovery Initialised ----------------'+'\x1b[0m')

# --------------------------- Main file handlers ---------------------------
pubkeys = os.listdir('keys/pubkeys/')
privkeys = os.listdir('keys/privkeys/')

print('\033[1m'+'\nPublik keys: ', len(pubkeys),'found\x1b[0m')
print('\033[1m'+'Private keys: ', len(privkeys),'found\n'+'\x1b[0m')
sleep(0.5)

# get balance
def get_balance():
	config = options.Get()
	config.read()
	node_ip_conf = config.node_ip_conf
	port = config.port


	try:
		key, public_key_readable, private_key_readable, encrypted, unlocked, public_key_hashed, address = essentials.keys_load("privkey.der", "pubkey.der")

		s = socks.socksocket()
		s.settimeout(10)
		s.connect((node_ip_conf, int(port)))

		connections.send (s, "balanceget", 10)
		connections.send (s, address, 10)
		balanceget_result = connections.receive (s, 10)
		print ("Address balance: {}".format (balanceget_result[0]))
		if float(balanceget_result[0]) > 0:
			sys.exit("\033[1;31m Found it! \x1b[0m")
	except ValueError:
		pass

# Handle the files function
def file_handler(pubkey, privkey, target, counter):
	try:
		# os.remove('wallet.der')
		os.remove('pubkey.der')
		os.remove('privkey.der')
		print("Previous keys removed, pubkey.der and privkey.der")
	except OSError:
		pass
	try:
		shutil.copy("keys/pubkeys/%s" % pubkey,target)
		os.rename(pubkey, "pubkey.der")
		shutil.copy("keys/privkeys/%s" % privkey,target)
		os.rename(privkey, "privkey.der")
		print("\n \x1b[6;30;42mFiles copied Try No: %s\x1b[0m" %i)
	except IOError as e:
	    print('\033[93m'+'Unable to copy file. '+'\x1b[0m',e)
	except:
	    print('\033[93m'+'Unexpected error: '+'\x1b[0m', sys.exc_info())

# Main loop to combine the files
i = 1
for pubkey in pubkeys:
	for privkey in privkeys:
		wallet = Path(target+'wallet.der')
		if wallet.is_file():
			sys.exit("\033[1;31m Found it! \x1b[0m");
		if i == 2:
			break
		# file_handler(pubkey, privkey, target, i)
		try:
			essentials.keys_load()
		except ValueError as err:
			print('\033[93m'+str(err)+'\x1b[0m')
		# os.system('python3 node.py')
		# get_balance()
		print("----------------------------------------------------------------------------\n\n")
		i += 1

print('\033[92m'+'\nProcess Finished.\nExiting ...'+'\x1b[0m')
sleep(1)