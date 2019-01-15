from smartchoke.targeting.trap_targeter import TrapTargeter

targeter = TrapTargeter()

for t in targeter.get_targets():
	print("Frame complete")
