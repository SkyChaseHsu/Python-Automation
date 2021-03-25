import urllib.request
import random
import requests
import os
# from lxml import html
import time

def get_user_agent():
	'''
	随机获取一个agent
	'''

	# agent池
	agent_pool = [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
		]

	# 从agent池中随机选出一个agent返回
	return agent_pool[random.randint(0, len(agent_pool)-1)]

def isimg(filename):
	'''
	判断filename是不是圖片文件
	'''
	return filename.lower().endswith(('.bmp','.dib','.png','.jpg','.jpeg','.pbm','.pgm', '.ppm','.tif','.tiff','.heic'))

def download_imgs(img_urls:list, save_dir="./save_dir"):
	'''
	从img_urls中下载图片到目的文件夹save_dir
	'''

	# 图片链接为空，直接返回
	if len(img_urls) == 0:
		return

	# 如果目的文件夹save_dir不存在，则创建一个
	if not os.path.exists(save_dir):
		os.mkdir(save_dir)

	# 开始爬取图片
	print(">> 开始爬取图片...")

	success_cnt = 0	# 下载成功的数目，用於結束時的總結提示
	total_cnt = len(img_urls)	# 需要下载的总数目，用于显示工作进度
	now_cnt = 0	# 已经处理过的数目，用于显示工作进度
	for img_url in img_urls:
		img_name = img_url.split("/")[-1]	# 获取图片名
		now_cnt += 1	# 已經處理+1

		# time.sleep(random.randint(1,3)) # 反爬，随机间隔1到3秒

		try:
			# agent池
			header = {'User-Agent':get_user_agent()}

			img_resource = requests.get(img_url, stream=True, headers=header)	# 获取图片数据

			# 将数据写入图片
			img_save_path = os.path.join(save_dir, img_name) # 获取图片保存路径

			with open(img_save_path, "wb")as f:
				# 分块写入
				for chunk in img_resource.iter_content(chunk_size=128):
					f.write(chunk)

			# 提示：工作進度，成功提示
			print("[{}/{}] 下载成功：{}".format(now_cnt,total_cnt,img_name))
			success_cnt += 1
		except:
			# 提示：工作進度，失敗提示
			print("[{}/{}] 下载失败：{}".format(now_cnt,total_cnt,img_name))
			continue

	# 结束爬取
	print("\n[爬取图片结束 {} 个成功，{} 个失败]\n".format(success_cnt, len(img_urls)-success_cnt))

def get_img_urls(target_url, img_rule=".//img/@src"):
	'''
	获取target_url页面中的所有图片链接，以img_urls列表返回

	参数：
		- img_rule: 目标图片的xpath, 默认是爬取所有图片
	'''
	# 開始提示
	print(">> 开始获取图片链接...")

	# agent池
	header = {'User-Agent':get_user_agent()}

	# 获取目标的html文件，etree解析
	req = requests.get(url=target_url, headers=header)
	req.encoding = req.apparent_encoding

	etree = html.etree
	req_html = etree.HTML(req.content)	# etree解析内容

	# 解析出图片的链接
	origin_img_urls = req_html.xpath("{}".format(img_rule))

	# 清洗掉不是图片的链接
	img_urls = [i for i in origin_img_urls if isimg(i.split("/")[-1])]

	# 提示信息：图片链接获取成功/失败
	if len(img_urls):
		print("\n[图片链接获取成功]\n")
	else:
		print("\n[图片链接获取失败]\n")

	return img_urls

def download_from_singlepage(target_url, img_rule=".//img/@src", save_dir="./save_dir"):
	'''
	从单个页面中下载图片

	Parameter:
		- target_url 需要爬取图片的网页
		- img_rule 要爬取图片的xpath
	'''
	img_urls = get_img_urls(target_url, img_rule)	# 图片链接列表
	download_imgs(img_urls, save_dir)	# 下载图片保存到

def download_from_SUNYAYA(target_url):
	'''
	这个网页的部分文章有密码保护，使用selenium输入密码，获取图片链接
	'''
	from selenium import webdriver

	# 初始化火狐浏览器
	browser = webdriver.Firefox() 

	# 获取页面
	browser.get(target_url)

	# 输入密码点击
	password = "SUNYAYA"
	browser.find_element_by_xpath(".//input[@type='password']").send_keys(password)
	browser.find_element_by_xpath(".//input[@type='submit']").click()

	# 获取html文件
	try:
		req_html_text = browser.execute_script("return document.documentElement.outerHTML")
		browser.quit()
		print("\n[html文件获取成功 {} ]\n".format(target_url))
	except:
		browser.quit()
		print("\n[html文件获取失败 {} ]\n".format(target_url))
		return

	# 将获得的html转为可以解析的格式
	etree = html.etree
	req_html = etree.HTML(req_html_text)	# etree解析内容

	# 退出浏览器
	browser.quit()

	# 解析出文章的标题，作为保存文件夹名称
	save_dir_title = req_html.xpath("//h2[@class='post-title']/a/@title")[0].split("|")[-1] # |不合文件名格式

	# 解析出图片的链接
	origin_img_urls = req_html.xpath("{}".format("//img/@src"))

	# 清洗掉不是图片的链接
	img_urls = [i for i in origin_img_urls if isimg(i.split("/")[-1])]

	# 提示信息：图片链接获取成功/失败
	if len(img_urls):
		print("\n[图片链接获取成功]\n")
	else:
		print("\n[图片链接获取失败]\n")
		return

	download_imgs(img_urls, os.path.join("save_dir", save_dir_title))


if __name__ == "__main__":
	# def download_imgs(img_urls:list, save_dir="./save_dir"):
	img_urls = ["https://www.hotcelebshome.com/wp-content/uploads/2021/03/Kristen-Stewart-Naked-Leaks-{}.jpg".format(i) for i in range(1, 42)]
	download_imgs(img_urls, "./savedir")