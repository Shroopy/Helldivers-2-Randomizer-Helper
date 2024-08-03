from enum import Enum, auto
import random
import os
import argparse

class itemType(Enum):
	SUPPORT = auto()
	BACKPACK = auto()
	BOT_DEFEATING = auto() # Direct fire medium 1 AP or higher to take out gunships, as well as tanks
	STRUCTURE_DEFEATING = auto()
	VEHICLE = auto()

class inventorySlots(Enum):
	PRIMARY = auto()
	SECONDARY = auto()
	THROWABLE = auto()
	STRAT1 = auto()
	STRAT2 = auto()
	STRAT3 = auto()
	STRAT4 = auto()

primaries = {
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
	"CB-9 Exploding Crossbow": {itemType.BOT_DEFEATING},
	"JAR-5 Dominator": {itemType.BOT_DEFEATING},
	"R-36 Eruptor": {itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"SG-8P Punisher Plasma": {itemType.BOT_DEFEATING},
	"ARC-12 Blitzer": {itemType.BOT_DEFEATING},
	"LAS-5 Scythe": set(),
	"LAS-16 Sickle": set(),
	"PLAS-1 Scorcher": {itemType.BOT_DEFEATING},
	"PLAS-101 Purifier": {itemType.BOT_DEFEATING}
}

secondaries = {
	"P-2 Peacemaker": set(),
	"P-19 Redeemer": set(),
	"GP-31 Grenade Pistol": {itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"LAS-7 Dagger": set(),
	"P-113 Verdict": set(),
	"P-4 Senator": set(),
	"SG-22 Bushwhacker": set()
}

throwables = {
	"G-6 Frag": {itemType.STRUCTURE_DEFEATING},
	"G-12 High Explosive": {itemType.STRUCTURE_DEFEATING},
	"G-10 Incendiary": {itemType.STRUCTURE_DEFEATING},
	"G-16 Impact": {itemType.STRUCTURE_DEFEATING},
	"G-13 Incendiary Impact": {itemType.STRUCTURE_DEFEATING},
	"G-23 Stun": set(),
	"G-3 Smoke": set(),
	"G-123 Thermite": {itemType.STRUCTURE_DEFEATING},
	"K-2 Throwing Knife": set()
}

stratagems = {
	"MG-43 Machine Gun": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"APW-1 Anti-Materiel Rifle": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"M-105 Stalwart": {itemType.SUPPORT},
	"EAT-17 Expendable Anti-Tank": {itemType.SUPPORT, itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"GR-8 Recoilless Rifle": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"FLAM-40 Flamethrower": {itemType.SUPPORT},
	"AC-8 Autocannon": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"MG-206 Heavy Machine Gun": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"RL-77 Airburst Rocket Launcher": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING},
	"MLS-4x Commando": {itemType.SUPPORT, itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"RS-422 Railgun": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"FAF-14 Spear": {itemType.SUPPORT, itemType.BACKPACK, itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},

	"Orbital Gatling Barrage": set(),
	"Orbital Airburst Strike": set(),
	"Orbital 120mm HE Barrage": {itemType.STRUCTURE_DEFEATING},
	"Orbital 380mm HE Barrage": {itemType.STRUCTURE_DEFEATING},
	"Orbital Walking Barrage": {itemType.STRUCTURE_DEFEATING},
	"Orbital Laser": set(), # Does everything but only two uses
	"Orbital Railcannon Strike": {itemType.BOT_DEFEATING},

	"Eagle Strafing Run": set(), # Might be able to hurt armor but needs testing
	"Eagle Airstrike": {itemType.STRUCTURE_DEFEATING},
	"Eagle Cluster Bomb": set(), # Might be able to hurt armor but needs testing
	"Eagle Napalm Airstrike": set(), # Might be able to hurt armor but needs testing
	"LIFT-850 Jump Pack": {itemType.BACKPACK},
	"Eagle Smoke Strike": set(),
	"Eagle 110mm Rocket Pods": {itemType.BOT_DEFEATING},
	"Eagle 500kg Bomb": set(), # Too slow recharge to be reasonably used against structures

	"Orbital Precision Strike": {itemType.STRUCTURE_DEFEATING}, # Just barely fast enough to be reasonably used against structures
	"Orbital Gas Strike": set(),
	"Orbital EMS Strike": set(),
	"Orbital Smoke Strike": set(),
	"E/MG-101 HMG Emplacement": set(), # Technically can destroy heavies but you'd need to hit their weakpoint and this is static
	"FX-12 Shield Generator Relay": set(),
	"A/ARC-3 Tesla Tower": set(),

	"MD-6 Anti-Personnel Minefield": set(),
	"B-1 Supply Pack": {itemType.BACKPACK},
	"GL-21 Grenade Launcher": {itemType.SUPPORT, itemType.STRUCTURE_DEFEATING},
	"LAS-98 Laser Cannon": {itemType.SUPPORT, itemType.BOT_DEFEATING},
	"MD-I4 Incendiary Mines": set(), # Might be able to hurt armor but needs testing
	"AX/LAS-5 \"Guard Dog\" Rover": {itemType.BACKPACK},
	"SH-20 Ballistic Shield Backpack": {itemType.BACKPACK},
	"ARC-3 Arc Thrower": {itemType.SUPPORT},
	"LAS-99 Quasar Cannon": {itemType.SUPPORT, itemType.BOT_DEFEATING, itemType.STRUCTURE_DEFEATING},
	"SH-32 Shield Generator Pack": {itemType.BACKPACK},

	"A/MG-43 Machine Gun Sentry": set(), # Technically can destroy heavies but you'd need to hit their weakpoint and this is static
	"A/G-16 Gatling Sentry": set(), # Technically can destroy heavies but you'd need to hit their weakpoint and this is static
	"A/M-12 Mortar Sentry": set(), # Technically can destroy structures but inconsistent due to being automated
	"AX/AR-23 \"Guard Dog\"": {itemType.BACKPACK},
	"A/AC-8 Autocannon Sentry": {itemType.BOT_DEFEATING},
	"A/MLS-4X Rocket Sentry": {itemType.BOT_DEFEATING},
	"A/M-23 EMS Mortar Sentry": set(),
	"EXO-45 Patriot Exosuit": {itemType.VEHICLE}, # Does everything but only two uses
	"EXO-49 Emancipator Exosuit": {itemType.VEHICLE} # Does everything but only two uses
}

def main(bots: bool, bugs: bool):
	myPrimary: str
	mySecondary: str
	myThrowable: str
	myStrats: set[str] = set()

	inventorySlotsList = [i for i in inventorySlots]
	random.shuffle(inventorySlotsList)

	haveBotDefeating: bool = False
	haveStructureDefeating: bool = False
	haveSupport: bool = False
	haveBackpack: bool = False

	for i in range(len(inventorySlotsList)):
		slot = inventorySlotsList[i]
		choices: dict[str, set[itemType]]
		if slot == inventorySlots.PRIMARY:
			choices = primaries
		elif slot == inventorySlots.SECONDARY:
			choices = secondaries
		elif slot == inventorySlots.THROWABLE:
			choices = throwables
		else:
			choices = stratagems

		itemFound = False
		item: str
		while not itemFound:
			item = random.choice(list(choices.keys()))
			
			if i == len(inventorySlotsList)-1 or (bots and i == len(inventorySlotsList)-2 and inventorySlotsList[len(inventorySlots)-1] == inventorySlots.THROWABLE): # Last inventory slot, we need to wrap it up
				if bots and not haveBotDefeating and not itemType.BOT_DEFEATING in choices[item]:
					del choices[item]
					continue
				if not haveStructureDefeating and not itemType.STRUCTURE_DEFEATING in choices[item]:
					del choices[item]
					continue
			
			if haveSupport and itemType.SUPPORT in choices[item]:
				del choices[item] 
				continue
			if haveBackpack and itemType.BACKPACK in choices[item]:
				del choices[item]
				continue

			itemFound = True
		
		if slot == inventorySlots.PRIMARY:
			myPrimary = item
		elif slot == inventorySlots.SECONDARY:
			mySecondary = item
		elif slot == inventorySlots.THROWABLE:
			myThrowable = item
		else:
			myStrats.add(item)

		haveBotDefeating = haveBotDefeating or itemType.BOT_DEFEATING in choices[item]
		haveStructureDefeating = haveStructureDefeating or itemType.STRUCTURE_DEFEATING in choices[item]
		haveSupport = haveSupport or itemType.SUPPORT in choices[item]
		haveBackpack = haveBackpack or itemType.BACKPACK in choices[item]

		del choices[item]
	
	print(f"Primary: {myPrimary}")
	print(f"Secondary: {mySecondary}")
	print(f"Throwable: {myThrowable}")
	print("Stratagems:\n\t", end="")
	print(*myStrats, sep="\n\t")
	os.system("pause")

parser = argparse.ArgumentParser("Helldivers 2 Randomizer Helper")
parser.add_argument("--enemy", help="Randomize specifically for fighting automatons or terminids.", choices={"bots", "bugs"})
#args = parser.parse_args(["--enemy", "bots"])
args = parser.parse_args()
bots = args.enemy == "bots"
bugs = args.enemy == "bugs"
main(bots, bugs)