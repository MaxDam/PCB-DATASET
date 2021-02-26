import xml.etree.ElementTree as ET
from pathlib import Path
import os

'''
legge la seguente struttura:
<annotation>
<size>
	<width>959</width>
	<height>959</height>
	<depth>3</depth>
</size>
<object>
	<name>short</name>
	<pose>Unspecified</pose>
	<truncated>0</truncated>
	<difficult>0</difficult>
	<bndbox>
		<xmin>317</xmin>
		<ymin>671</ymin>
		<xmax>426</xmax>
		<ymax>546</ymax>
	</bndbox>
</object>
</annotation>

trasformandola in yolo3:
<class> <x> <y> <width> <height> 
0 0.25 0.44 0.5 0.8
'''

BASE_ANNOTATION_PATH = './Annotations'
BASE_OUTPUT_PATH = './AnnotationsYolo'

def convertLabels(x1, y1, x2, y2, height, width, cat):
	def sorting(v1, v2):
		if v1 > v2:
			vmax, vmin = v1, v2
			return vmax, vmin
		else:
			vmax, vmin = v2, v1
			return vmax, vmin
	size = (height, width)
	xmax, xmin = sorting(x1, x2)
	ymax, ymin = sorting(y1, y2)
	dw = 1. / size[1]
	dh = 1. / size[0]
	x = (xmin + xmax) / 2.0
	y = (ymin + ymax) / 2.0
	w = xmax - xmin
	h = ymax - ymin
	x = x * dw
	w = w * dw
	y = y * dh
	h = h * dh
	return cat, x, y, w, h
		
def convertAnnotations(categoryPath, category):
	listOfFiles = Path(BASE_ANNOTATION_PATH + '/' + categoryPath)
	for filePath in listOfFiles.iterdir():
		print(filePath)
		parser = ET.XMLParser(encoding="utf-8")
		targetTree = ET.parse(filePath, parser=parser)
		rootTag = targetTree.getroot()
		for sizeTag in rootTag.findall('size'):
			width = float(sizeTag.find('width').text)
			height = float(sizeTag.find('height').text)	
		for objectTag in rootTag.findall('object'):
			for bndboxTag in objectTag.findall('bndbox'):
				xmin = float(bndboxTag.find('xmin').text)
				ymin = float(bndboxTag.find('ymin').text)
				xmax = float(bndboxTag.find('xmax').text)
				ymax = float(bndboxTag.find('ymax').text)
				cat, x, y, w, h = convertLabels(xmin, ymin, xmax, ymax, height, width, category)
				dirOutput = BASE_OUTPUT_PATH + '/' + categoryPath
				if not os.path.exists(dirOutput):
					os.makedirs(dirOutput)
				fileOutput = str(os.path.basename(filePath)).replace("xml", "txt")
				if os.path.exists(dirOutput + '/' + fileOutput):
					append_write = 'a'
				else:
					append_write = 'w'
				f = open(dirOutput + '/' + fileOutput, append_write)
				f.write('{} {} {} {} {}\n'.format(cat, x, y, w, h))
				f.close()
	
convertAnnotations("Missing_hole", 0)
convertAnnotations("Mouse_bite", 1)
convertAnnotations("Open_circuit", 2)
convertAnnotations("Short", 3)
convertAnnotations("Spur", 4)
convertAnnotations("Spurious_copper", 5)


