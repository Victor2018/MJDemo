#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

#android项目更目录
project_path = "D:\\GitProjects\\android-hok"

#加固开关
reinforcerEnabled = False

#apk编译完成
buildApkCompleted = False

#编译渠道
onlineChannels = ["Online","Huawei","Xiaomi","Oppo","Vivo","Samsung","Tencent"]
# onlineChannels = ["Vivo"]

devChannels = ["Online","Huawei","Xiaomi","Oppo","Vivo","Samsung","Tencent"]
# devChannels = ["Dev"]

#360登录用户名
login_360_name = "18813938924"
login_360_password = "Xx423099"

#签名配置
keystore_path = "D:\\GitProjects\\android-hok\\docs\\hok_keystore.jks"
#keystore_password
keystore_password = "android"
#alias
alias = "hok"
#alias_password
alias_password = "android"

# 360加固工具目录
jgPath = "D:\\soft\\360jiagubao_windows_x64\\jiagu\\"
#360加固后apk输出目录
output_path = "C:\\Users\\BS-WX\\Desktop\\apk_360_output"

# 查找当前目录apk文件
def get_apk_path(path):
	dirs = os.listdir(path)
	for f in dirs:
		print("遍历文件:", f)
		if f.endswith(".apk"):
			return f
	return None

#360加固
def reinforcer(channel):
	# 安装包地址
	build_out_path = project_path + "\\app\\build\\outputs\\apk\\" + channel.lower() + "\\release"
	apk_path = get_apk_path(build_out_path)

	print ("build_out_path = %s" %build_out_path)
	print ("apk_path = %s" %apk_path)

	if (len(apk_path) > 0):
		print ("---------------------开始加固apk---------------------")

		#加固目录不存在自动创建
		if not os.path.exists(output_path):
			os.makedirs(output_path)

		# 进入加固目录
		os.chdir(jgPath)

		#登录360账号
		os.system("java\\bin\\java -jar jiagu.jar -login " + login_360_name + " " + login_360_password)

		# 签名配置
		os.system("java\\bin\\java -jar jiagu.jar -importsign " + keystore_path + " " + keystore_password + " " + alias + " " + alias_password)

		# 查看当前签名 keystore 信息
		os.system("java\\bin\\java -jar jiagu.jar -showsign")

		# 执行加固命令
		os.system("java\\bin\\java -jar jiagu.jar -showconfig")
		cmd = "java\\bin\\java -jar jiagu.jar -jiagu " + build_out_path + "\\" + apk_path + " " + output_path + " -autosign"
		os.system(cmd)
		print("---------------------加固成功，加固apk放置在这里---------------------")

		print("output_path = %s" %output_path)
	else:
		print ("---------------------哦哦,没有找到apk文件---------------------")

#打包
def buildChannelApk(channel):

	if buildApkCompleted == True:
		reinforcer(channel)
	else:
		# 进入项目根目录
		os.chdir(project_path)

		print("---------------------开始编译apk---------------------")
		# 执行编译命令
		buildCmd = "gradlew assemble%sRelease" %channel
		print("buildCmd = %s" %buildCmd)
		r = os.system(buildCmd)

		print("---------------------apk编译完成---------------------")
		if r == 0:
			if reinforcerEnabled:
				reinforcer(channel)
			else:
				print("---------------------360加固未开启---------------------")
		else:
			print ("---------------------哦哦,编译apk失败---------------------")


def start():

	#加固开启编译线上包
	if reinforcerEnabled == True:
		print ("---------------------本次编译%s个渠道---------------------" %len(onlineChannels))
		print ("本次编译渠道:%s" %onlineChannels)

		for channel in onlineChannels:
			buildChannelApk(channel)
	#加固关闭编译测试包
	else:
		print ("---------------------本次编译%s个渠道---------------------" %len(devChannels))
		print ("本次编译渠道:%s" %devChannels)

		for channel in devChannels:
			buildChannelApk(channel)

if __name__ == "__main__":
	start()