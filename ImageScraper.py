from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import re
import urllib2
import os, sys
import getopt

websiteLink = ""
folderName = "scarapped_images"

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "l:f:", ["link=", "folder="])
	except getopt.GetoptError:
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-l", "--link"):
			global websiteLink
			websiteLink = arg
		elif opt in ("-f", "--folder"):
			global folderName
			folderName = arg

	if websiteLink == "":
		print "Please provide the website link !!!"
		sys.exit(0)

if __name__ == '__main__':
	main(sys.argv[1:])

	folderPath = os.path.join(os.getcwd(), folderName)
	broswer = webdriver.Chrome()

	try:
		broswer.get(websiteLink)
	except WebDriverException as error:
		print error
		broswer.quit()
		sys.exit(0)

	htmlCode = broswer.page_source
	images = re.findall(r'<\s*img.*?src=\"(.*?)\".*?>', htmlCode)
	imageCount = 0
	consideredImages = {}

	if not os.path.exists(folderPath):
		os.mkdir(folderPath)

	for image in images:
		print image
		validImageLink = len(re.findall(r'^http.*?(png|jpeg|jpg|svg|gif)', image)) > 0 

		if validImageLink and image not in consideredImages:
			imageCount += 1
			consideredImages[image] = True

			extension = re.findall(r'^http.*?(png|jpeg|jpg|svg|gif)', image)[0]
			imageFileName = str(imageCount) + "." + extension
			imageFile = open(folderName + "/" + imageFileName, 'wb')
			imageFile.write(urllib2.urlopen(image).read())
			imageFile.close()

	broswer.quit()