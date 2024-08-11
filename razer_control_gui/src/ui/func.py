import json
import os
from os.path import exists

data_raw: None
data: dict

if exists(os.environ["HOME"] + "/.local/share/razercontrol/data.json"):
	data_raw = open(os.environ["HOME"] + "/.local/share/razercontrol/data.json", "r+")
	data_raw.seek(0)
	try:
		data = json.loads(data_raw.read())
		data_raw.seek(0)
	except:
		data_raw.seek(0)
		os.system(
			"echo {} > " + os.environ["HOME"] + "/.local/share/razercontrol/data.json"
		)
		data_raw.seek(0)
		data_raw.seek(0)
		data = json.loads(data_raw.read())
		data_raw.seek(0)
else:
	data_raw = open(os.environ["HOME"] + "/.local/share/razercontrol/data.json", "w+")
	data = dict()


def read(file=data_raw):
	res = file.read()
	file.seek(0)
	return res


def overwrite():
	data_raw.seek(0)
	data_raw.truncate()
	data_raw.write(json.dumps(data))


if (
	"min_fan" not in data
	or "max_fan" not in data
	or "creator_mode" not in data
	or "boost" not in data
):
	laptops_raw = open("/usr/share/razercontrol/laptops.json")
	laptops = json.loads(laptops_raw.read())
	laptops_raw.close()

	for entry in os.popen("lsusb"):
		vid = entry[23:27]
		pid = entry[28:32]

		for laptop in laptops:
			# Assumes you only have one laptop, which will probably be fine in 99.99999% of cases but maybe someone somehow will have more than one
			if vid == laptop["vid"] and pid == laptop["pid"]:
				data["name"] = laptop["name"]
				data["vid"] = laptop["vid"]
				data["pid"] = laptop["pid"]
				data["min_fan"] = laptop["fan"][0]
				data["max_fan"] = laptop["fan"][1]

				if "creator_mode" in laptop:
					data["creator_mode"] = True
				else:
					data["creator_mode"] = False

				if "boost" in laptop:
					data["boost"] = True
				else:
					data["boost"] = False

				overwrite()


def get_min_fan():
	return data["min_fan"]


def get_max_fan():
	return data["max_fan"]


def get_fan_ac():
	if os.popen("razer-cli read fan ac").read().splitlines()[1][-2] == "0":
		data["fan_ac"] = 0
		overwrite()
		return 0
	else:
		data["fan_ac"] = int(
			os.popen("razer-cli read fan ac").read().splitlines()[0][-6:-2]
		)
		overwrite()
		return int(os.popen("razer-cli read fan ac").read().splitlines()[0][-6:-2])


def set_fan_ac(rpm):
	if rpm != 0:
		data["fan_ac_manual"] = rpm

	data["fan_ac"] = rpm
	overwrite()
	return os.popen("razer-cli write fan ac " + str(rpm)).read()


def get_fan_bat():
	if os.popen("razer-cli read fan bat").read().splitlines()[1][-2] == "0":
		data["fan_bat"] = 0
		overwrite()
		return 0
	else:
		data["fan_bat"] = int(
			os.popen("razer-cli read fan bat").read().splitlines()[0][-6:-2]
		)
		overwrite()
		return int(os.popen("razer-cli read fan bat").read().splitlines()[0][-6:-2])


def set_fan_bat(rpm):
	if rpm != 0:
		data["fan_bat_manual"] = rpm

	data["fan_bat"] = rpm
	overwrite()
	return os.popen("razer-cli write fan bat " + str(rpm)).read()


def get_fan_ac_manual():
	if "fan_ac_manual" not in data:
		data["fan_ac_manual"] = data["min_fan"]

	if get_fan_ac() != 0:
		data["fan_ac_manual"] = get_fan_ac()

	overwrite()
	return data["fan_ac_manual"]


def get_fan_bat_manual():
	if "fan_bat_manual" not in data:
		data["fan_bat_manual"] = data["min_fan"]

	if get_fan_bat() != 0:
		data["fan_bat_manual"] = get_fan_bat()

	overwrite()
	return data["fan_bat_manual"]


def get_power_ac():
	data["power_ac"] = os.popen("razer-cli read power ac").read().splitlines()[0][-3]
	overwrite()
	return int(os.popen("razer-cli read power ac").read().splitlines()[0][-3])


def set_power_ac(mode, cpu, gpu):
	if mode == 4:
		data["power_ac"] = mode
		data["cpu"] = cpu
		data["gpu"] = gpu
		overwrite()
		return os.popen(
			"razer-cli write power ac 4 " + str(cpu) + " " + str(gpu)
		).read()

	data["power_ac"] = mode
	return os.popen("razer-cli write power ac " + str(mode)).read()


def get_cpu_boost():
	if "cpu" not in data:
		data["cpu"] = 0
		overwrite()

	if get_power_ac() == 4:
		data["cpu"] = int(
			os.popen("razer-cli read power ac").read().splitlines()[2][-3]
		)
		overwrite()
		return data["cpu"]
	else:
		return data["cpu"]


def get_gpu_boost():
	if "gpu" not in data:
		data["gpu"] = 0
		overwrite()

	if get_power_ac() == 4:
		data["gpu"] = int(
			os.popen("razer-cli read power ac").read().splitlines()[4][-3]
		)
		overwrite()
		return data["gpu"]
	else:
		return data["gpu"]


def set_boost(cpu, gpu):
	return os.popen("razer-cli write power ac 4 " + str(cpu) + " " + str(gpu)).read()


def get_creator_mode():
	return data["creator_mode"]


def get_boost():
	return data["boost"]


def get_brightness_ac():
	if os.popen("razer-cli read brightness ac").read().splitlines()[1][-3] == "1":
		return 100
	else:
		return int(os.popen("razer-cli read brightness ac").read().splitlines()[1][-2:])


def set_brightness_ac(percent):
	return os.popen("razer-cli write brightness ac " + str(int(percent))).read()


def get_brightness_bat():
	if os.popen("razer-cli read brightness bat").read().splitlines()[1][-3] == "1":
		return 100
	else:
		return int(
			os.popen("razer-cli read brightness bat").read().splitlines()[1][-2:]
		)


def set_brightness_bat(percent):
	return os.popen("razer-cli write brightness bat " + str(int(percent))).read()


def get_logo_ac():
	return int(os.popen("razer-cli read logo ac").read().splitlines()[0][-3])


def set_logo_ac(mode):
	return os.popen("razer-cli write logo ac " + str(mode)).read()


def get_logo_bat():
	return int(os.popen("razer-cli read logo bat").read().splitlines()[0][-3])


def set_logo_bat(mode):
	return os.popen("razer-cli write logo bat " + str(mode)).read()


def set_logo_manual(mode):
	data["logo_manual"] = mode
	return set_logo_ac(mode)


def set_logo_ac_manual(mode):
	data["logo_ac_manual"] = mode
	return set_logo_ac(mode)


def set_logo_bat_manual(mode):
	data["logo_bat_manual"] = mode
	return set_logo_bat(mode)


def get_sync():
	if os.popen("razer-cli read sync").read().splitlines()[1][-2] == "u":
		return True
	else:
		return False


def set_sync(boolean):
	if boolean:
		return os.popen("razer-cli write sync on").read()
	else:
		return os.popen("razer-cli write sync off").read()


def get_logo_manual():
	if "logo_manual" not in data:
		if get_sync():
			data["logo_manual"] = get_logo_ac()
		else:
			data["logo_manual"] = 1

	return data["logo_manual"]


def get_logo_ac_manual():
	if "logo_ac_manual" not in data:
		data["logo_ac_manual"] = get_logo_ac()

	return data["logo_ac_manual"]


def get_logo_bat_manual():
	if "logo_bat_manual" not in data:
		data["logo_bat_manual"] = get_logo_bat()

	return data["logo_bat_manual"]


def set_effect(*args):
	all_args = ""
	for arg in args:
		all_args += str(arg) + " "
	return os.popen("razer-cli write " + all_args)
