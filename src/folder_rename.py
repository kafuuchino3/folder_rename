import os

#创建一个类存储文件夹下内容分类
class InFolder:
	address = ''
	size = 0	#大小,单位为byte（字节）
	num = 0 	#文件数目（文件夹除外）
	folder = 0	#文件夹数量                                           
	photo = 0	#图片数量
	video = 0	#视频数量
	other = 0	#其他类型文件数量

	def get_size(self):
		the_size = ''
		the_size = byte_conversion(self.size)
		#print(self.size)
		return the_size



#统计单个文件的大小
def stat_file(file):
	info = os.stat(file)	#获取文件相关信息，并返回文件大小信息
	byte = info.st_size   #单位为B（字节）
	#kilobits = byte/1024           #计算机中计算内存大小时使用的是1000，而不是1024
	return byte	#返回文件的大小（单位为KB）



#字节转换
def byte_conversion(byte):
	units = ['B','KB','MB','GB','TB','PB']
	size = byte
	for unit in units:
		#print('当前大小：{:.2f}		当前单位:{}'.format(size,unit))	#测试
		if size > 1024:
			size = size / 1024
		else:
			the_size = '{:.2f}{}'.format(size,unit)		#返回型的格式化
			break
	return(the_size)	#返回大小以及单位



#文件分类
def file_classify(folder,file):
	file_type = os.path.splitext(file)

	picture = ('bmp','.jpg','.jpge','.png','webp')
	video = ('.avi','.flv','.mkv','.mov','.mpg','.mp4','.m4v','.rmvb','.webm','.wmv','.mts','.m2ts')
	if str.lower(file_type[1])  in picture:
		folder.photo += 1
	elif str.lower(file_type[1])  in video:
		folder.video += 1
	else:
		folder.other += 1
	return folder


#定义统计目录的函数
def stat_directory(directory):

	dir_list = os.listdir(directory)	#获取目录中的文件列表
	
	the_folder = InFolder()
	#遍历目录，对目录中的文件和子目录进行大小统计	
	for i in dir_list:			
		file_now = os.path.join(directory,i)	#把目录和文件名合成一个路径
		#判断是文件还是目录，并进行相应的操作
		if os.path.isfile(file_now):
			#是文件
			the_folder.size += stat_file(file_now) 	#当前文件夹内总文件大小		 
			the_folder.num += 1 	#统计文件总数+1 
			the_folder = file_classify(the_folder,file_now)

			#print('文件名：{}	{:.2f}MB\n'.format(i,Kb_to_Mb(stat_file(file_now))))
		elif os.path.isdir(file_now):
			#是目录，递归	
			the_folder.folder += 1	#目录包含文件夹+1
			sub_folder = InFolder()	#实例化子目录
			sub_folder = stat_directory(file_now)   #获取子目录统计
			#加上子目录包含的内容
			the_folder.size += sub_folder.size
			the_folder.num += sub_folder.num
			the_folder.folder += sub_folder.folder			
			the_folder.photo += sub_folder.photo
			the_folder.video += sub_folder.video
			the_folder.other += sub_folder.other
			
			sub_folder.address = file_now	#将当前地址存入类
			string = folder_rename(sub_folder)	#文件夹重命名
			os.rename(file_now,string)	#更改文件名
			
	#print('地址:{}'.format(the_folder.address))
	#print('当前文件夹是：{}\n		包含文件夹数目：{}\n		包含文件数目：{}\n		包含图片数目：{}\n		包含视频数目：{}\n		包含其它数目：{}\n		总计大小：{}\n'.format(directory,the_folder.folder,the_folder.num,the_folder.photo,the_folder.video,the_folder.other,the_folder.get_size()))
	
	return the_folder         #返回统计类



#更改后的文件夹名
def folder_rename(folder):
	#print('地址:{}'.format(folder.address))
	#print('{}P	{}V	{}O	{}'.format(folder.photo,folder.video,folder.other,folder.get_size()))

	#生成新文件夹名
	string = '{}['.format(folder.address)
	if folder.photo == 0:
		string_p = ''
	else:
		string_p = '{}P'.format(folder.photo)
	if folder.video == 0:
		string_v = ''
	else:
		string_v = '{}V'.format(folder.video)
	if folder.other == 0:
		string_o = ''
	else:
		string_o = '{}O'.format(folder.other)	
	string_size = ' {}]'.format(folder.get_size())
	string = string + string_p + string_v +string_o + string_size	#组合

	print(string)	#控制台输出新格式验证
	return string	#返回重命名的字符串



#测试统计目录的函数
folder = InFolder()	#实例化 InFolder 类
folder.address = 'L:\\TEST\\test'	#整理位置
os.chdir(folder.address)	#把当前工作目录改为目标位置
folder = stat_directory(folder.address)	#获取目录统计
print('更改文件夹是：{}\n		包含文件数目：{}\n		总计大小：{}\n'.format(folder.address,folder.num,folder.get_size()))

#os.chdir(address)	#把当前工作目录改为目标位置	
#string='{}[{}P{}V {:.2f}MB]'.format(i,photo,video,dir_big)	#格式化命名为 文件夹名[?P ??.??MB]
# print(string)	#控制台输出新格式验证
# os.rename(i,string)	#更改文件名