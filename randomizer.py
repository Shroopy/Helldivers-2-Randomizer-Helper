from enum import Enum, auto
import random
import os
import argparse

class itemType(Enum):
	SUPPORT = auto()
	BACKPACK = auto()
	BOT_DEFEATING = auto() # Direct fire medium 1 (level 3) AP or higher to take out gunships, as well as tanks
	FAB_DEFEATING = auto() # Has to have enough to take out large base (4?)
	NEST_DEFEATING = auto() # Has to have enough to take out large nest (8?), be refillable from resupply, or infinite
	VEHICLE = auto()
	STANDOFF = auto()
	CQC = auto()

class inventorySlots(Enum):
	PRIMARY = auto()
	SECONDARY = auto()
	THROWABLE = auto()
	STRAT1 = auto()
	STRAT2 = auto()
	STRAT3 = auto()
	STRAT4 = auto()

primaries: dict[str, set[itemType]] = {
	"AR-23 Liberator": set(),
	"AR-23P Liberator Penetrator": {itemType.BOT_DEFEATING},
	"AR-23C Liberator Concussive": set(),
	"AR-23A Liberator Carbine": set(),
	"AR-61 Tenderizer": set(),
	"BR-14 Adjudicator": {itemType.BOT_DEFEATING},
	"R-63 Diligence": set(),
	"R-63CS Diligence Counter Sniper": {itemType.BOT_DEFEATING},
	"MP-98 Knight": set(),
	"SMG-37 Defender": set(),
	"SMG-72 Pummeler": set(),
	"SG-8 Punisher": set(),
	"SG-8S Slugger": {itemType.BOT_DEFEATING},
	"SG-225 Breaker": set(),
	"SG-225SP Breaker Spray & Pray": set(),
	"SG-225IE Breaker Incendiary": set(),
	"CB-9 Exploding Crossbow": {itemType.BOT_DEFEATING, itemType.STANDOFF},
	"JAR-5 Dominator": {itemType.BOT_DEFEATING},
	"R-36 Eruptor": {itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.NEST_DEFEATING, itemType.STANDOFF},
	"SG-8P Punisher Plasma": {itemType.BOT_DEFEATING, itemType.STANDOFF},
	"ARC-12 Blitzer": set(),
	"LAS-5 Scythe": set(),
	"LAS-16 Sickle": set(),
	"PLAS-1 Scorcher": {itemType.BOT_DEFEATING, itemType.STANDOFF},
	"PLAS-101 Purifier": {itemType.BOT_DEFEATING, itemType.STANDOFF}
}

secondaries: dict[str, set[itemType]] = {
	"P-2 Peacemaker": set(),
	"P-19 Redeemer": set(),
	"GP-31 Grenade Pistol": {itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.NEST_DEFEATING, itemType.STANDOFF},
	"LAS-7 Dagger": {itemType.STANDOFF},
	"P-113 Verdict": set(),
	"P-4 Senator": set(),
	"SG-22 Bushwhacker": set()
}

throwables: dict[str, set[itemType]] = {
	"G-6 Frag": {itemType.FAB_DEFEATING, itemType.NEST_DEFEATING},
	"G-12 High Explosive": {itemType.FAB_DEFEATING, itemType.NEST_DEFEATING},
	"G-10 Incendiary": {itemType.FAB_DEFEATING, itemType.NEST_DEFEATING},
	"G-16 Impact": {itemType.FAB_DEFEATING, itemType.NEST_DEFEATING},
	"G-13 Incendiary Impact": {itemType.FAB_DEFEATING, itemType.NEST_DEFEATING},
	"G-23 Stun": set(),
	"G-3 Smoke": set(),
	"G-123 Thermite": {itemType.FAB_DEFEATING, itemType.NEST_DEFEATING},
	"K-2 Throwing Knife": set()
}

stratagems: dict[str, set[itemType]] = {
	"MG-43 Machine Gun": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"APW-1 Anti-Materiel Rifle": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"M-105 Stalwart": {itemType.SUPPORT},
	"EAT-17 Expendable Anti-Tank": {itemType.SUPPORT, itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.STANDOFF},
	"GR-8 Recoilless Rifle": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.NEST_DEFEATING, itemType.STANDOFF},
	"FLAM-40 Flamethrower": {itemType.SUPPORT},
	"AC-8 Autocannon": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.NEST_DEFEATING, itemType.STANDOFF},
	"MG-206 Heavy Machine Gun": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"RL-77 Airburst Rocket Launcher": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.STANDOFF},
	"MLS-4x Commando": {itemType.SUPPORT, itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.STANDOFF},
	"RS-422 Railgun": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"FAF-14 Spear": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.NEST_DEFEATING, itemType.STANDOFF},

	"Orbital Gatling Barrage": set(),
	"Orbital Airburst Strike": set(),
	"Orbital 120mm HE Barrage": set(),
	"Orbital 380mm HE Barrage": set(),
	"Orbital Walking Barrage": set(),
	"Orbital Laser": set(), # Does everything but only two uses
	"Orbital Napalm Barrage": set(),
	"Orbital Railcannon Strike": set(),

	"Eagle Strafing Run": set(),
	"Eagle Airstrike": set(),
	"Eagle Cluster Bomb": set(),
	"Eagle Napalm Airstrike": set(),
	"LIFT-850 Jump Pack": {itemType.BACKPACK},
	"Eagle Smoke Strike": set(),
	"Eagle 110mm Rocket Pods": set(),
	"Eagle 500kg Bomb": set(), # Too slow recharge to be reasonably used against structures

	"Orbital Precision Strike": set(),
	"Orbital Gas Strike": set(),
	"Orbital EMS Strike": set(),
	"Orbital Smoke Strike": set(),
	"E/MG-101 HMG Emplacement": set(), # Technically can destroy heavies but you'd need to hit their weakpoint and this is static
	"FX-12 Shield Generator Relay": set(),
	"A/ARC-3 Tesla Tower": set(),

	"MD-6 Anti-Personnel Minefield": set(),
	"B-1 Supply Pack": {itemType.BACKPACK},
	"GL-21 Grenade Launcher": {itemType.SUPPORT, itemType.FAB_DEFEATING, itemType.NEST_DEFEATING, itemType.STANDOFF},
	"LAS-98 Laser Cannon": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"MD-I4 Incendiary Mines": set(),
	"AX/LAS-5 \"Guard Dog\" Rover": {itemType.BACKPACK},
	"SH-20 Ballistic Shield Backpack": {itemType.BACKPACK},
	"ARC-3 Arc Thrower": {itemType.SUPPORT, itemType.STANDOFF, itemType.BOT_DEFEATING},
	"MD-17 Anti-Tank Mines": set(),
	"LAS-99 Quasar Cannon": {itemType.SUPPORT, itemType.BOT_DEFEATING, itemType.FAB_DEFEATING, itemType.STANDOFF},
	"SH-32 Shield Generator Pack": {itemType.BACKPACK},

	"A/MG-43 Machine Gun Sentry": set(), # Technically can destroy heavies but you'd need to hit their weakpoint and this is static
	"A/G-16 Gatling Sentry": set(), # Technically can destroy heavies but you'd need to hit their weakpoint and this is static
	"A/M-12 Mortar Sentry": set(), # Technically can destroy structures but inconsistent due to being automated
	"AX/AR-23 \"Guard Dog\"": {itemType.BACKPACK},
	"A/AC-8 Autocannon Sentry": set(),
	"A/MLS-4X Rocket Sentry": set(),
	"A/M-23 EMS Mortar Sentry": set(),
	"EXO-45 Patriot Exosuit": {itemType.VEHICLE}, # Does everything but only two uses
	"EXO-49 Emancipator Exosuit": {itemType.VEHICLE} # Does everything but only two uses
}

def isStratagem(slot: inventorySlots):
	return slot in {inventorySlots.STRAT1, inventorySlots.STRAT2, inventorySlots.STRAT3, inventorySlots.STRAT4}

def isEquipGun(slot: inventorySlots):
	return slot in {inventorySlots.PRIMARY, inventorySlots.SECONDARY}

def main(bots: bool, bugs: bool):
	
	requirements: set[itemType] = {itemType.CQC}
	if bots:
		requirements.update({itemType.BOT_DEFEATING, itemType.FAB_DEFEATING})
	elif bugs:
		requirements.update({itemType.NEST_DEFEATING})

	myPrimary: str
	mySecondary: str
	myThrowable: str
	myStrats: set[str] = set()

	inventorySlotsList = [i for i in inventorySlots]
	random.shuffle(inventorySlotsList)
	firstSlot = random.choice((inventorySlots.PRIMARY, inventorySlots.SECONDARY, inventorySlots.THROWABLE, inventorySlots.STRAT1))
	inventorySlotsList.insert(0, inventorySlotsList.pop(inventorySlotsList.index(firstSlot)))

	haveSupport: bool = False
	haveBackpack: bool = False

	for i in range(len(inventorySlotsList)):
		slot = inventorySlotsList[i]
		items: dict[str, set[itemType]]
		if slot == inventorySlots.PRIMARY:
			items = primaries
		elif slot == inventorySlots.SECONDARY:
			items = secondaries
		elif slot == inventorySlots.THROWABLE:
			items = throwables
		else:
			items = stratagems

		itemKeys = list(items.keys())
		random.shuffle(itemKeys)
		for item in itemKeys:
			itemFlags = items[item]

			if isStratagem(slot) and item in myStrats:
				continue
			if haveSupport and itemType.SUPPORT in itemFlags:
				continue
			if haveBackpack and itemType.BACKPACK in itemFlags:
				continue
			
			if len(requirements) > 0 and not (isStratagem(slot) and haveSupport):
				goodItem: bool = False
				for flag in itemFlags:
					if flag in requirements:
						goodItem = True
						requirements.remove(flag)
				if not goodItem and (isEquipGun(slot) or itemType.SUPPORT in itemFlags) and itemType.STANDOFF not in itemFlags and itemType.CQC in requirements:
					goodItem = True
					requirements.remove(itemType.CQC) 
				if not goodItem:
					continue

			break
		
		if slot == inventorySlots.PRIMARY:
			myPrimary = item
		elif slot == inventorySlots.SECONDARY:
			mySecondary = item
		elif slot == inventorySlots.THROWABLE:
			myThrowable = item
		else:
			myStrats.add(item)

		haveSupport = haveSupport or itemType.SUPPORT in itemFlags
		haveBackpack = haveBackpack or itemType.BACKPACK in itemFlags
	
	print(f"Primary: {myPrimary}")
	print(f"Secondary: {mySecondary}")
	print(f"Throwable: {myThrowable}")
	print("Stratagems:\n\t", end="")
	print(*myStrats, sep="\n\t")
	os.system("pause")

parser = argparse.ArgumentParser("Helldivers 2 Randomizer Helper")
parser.add_argument("--enemy", help="Randomize specifically for fighting automatons or terminids.", choices={"bots", "bugs"})
#args = parser.parse_args(["--enemy", "bugs"])
args = parser.parse_args()
bots = args.enemy == "bots"
bugs = args.enemy == "bugs"
main(bots, bugs)