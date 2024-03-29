import cv2
import numpy as np
import math
import argparse


class Perspective():
	optimalStep = 4
	def __init__(self, extremosDeOrigen):
		# Take the poligon cuted ROI IMAGE
		self.extremosDeOrigen= extremosDeOrigen # Expected something like srcPol = [[pt1],[pt2],[pt3],[pt4]]
		self.src_point1 = self.extremosDeOrigen[0]
		self.src_point2 = self.extremosDeOrigen[1]
		self.src_point3 = self.extremosDeOrigen[2]
		self.src_point4 = self.extremosDeOrigen[3]
		self.A = self._encontrarLongitudLado(self.src_point1,self.src_point2)
		self.B = self._encontrarLongitudLado(self.src_point2,self.src_point3)
		self.C = self._encontrarLongitudLado(self.src_point3,self.src_point4)
		self.D = self._encontrarLongitudLado(self.src_point4,self.src_point1)
		self.xmin = min(self.src_point1[0],self.src_point2[0],self.src_point3[0],self.src_point4[0])
		self.xmax = max(self.src_point1[0],self.src_point2[0],self.src_point3[0],self.src_point4[0])
		self.xmax = self.xmax - (self.xmax-self.xmin)%Perspective.optimalStep
		self.ymin = min(self.src_point1[1],self.src_point2[1],self.src_point3[1],self.src_point4[1])
		self.ymax = max(self.src_point1[1],self.src_point2[1],self.src_point3[1],self.src_point4[1])
		self.ymax = self.ymax - (self.ymax-self.ymin)%Perspective.optimalStep
		self.newWidth = int((self.xmax - self.xmin)/4)
		self.newHeight = int((self.ymax - self.ymin)/4)

		if self.A>self.C:
			lado1 = int(self.A)
		else:
			lado1 = int(self.C)
		if self.B>self.D:
			lado2 = int(self.B)
		else:
			lado2 = int(self.D)
		if lado1 < lado2:
			self.imageSize = (lado2, lado1)
		else:
			self.imageSize = (lado1, lado2)
		
		# como los lados se daran en orden se tomara la mayor longitud entre a y c y b y d:
		self.lienzoDestino = np.float32([[0,0], [self.imageSize[0],0], [self.imageSize[0],self.imageSize[1]], [0,self.imageSize[1]]])

		# For source points I'm grabbing the outer four detected corners
		self.extremosDeOrigen= np.float32([self.src_point4, self.src_point3, self.src_point2, self.src_point1])
		
		# Given self.extremosDeOrigenand lienzoDestino points, calculate the perspective transform matrix
		self.M = cv2.getPerspectiveTransform(self.extremosDeOrigen, self.lienzoDestino)

	def _encontrarLongitudLado(self,p1,p2):
		longitud = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
		return longitud

	def transformar(self,image,height = 0):

		image_np  = cv2.imread(image)

		if height == 0:	
			transformado = cv2.warpPerspective(image_np, self.M, self.imageSize)
		else:
			#if tamanoSalida == (0,0):
			transformado = cv2.warpPerspective(image_np, self.M, (height*self.imageSize[0]//self.imageSize[1],height))
			#else:
			#	transformado = cv2.warpPerspective(image, self.M, tamanoSalida)
		return transformado

	def enmarcar(self,imagen):
		nuevaImagen = imagen[self.ymin:self.ymax,self.xmin:self.xmax]
		imagen = cv2.resize(nuevaImagen,(self.newWidth,self.newHeight))
		return imagen

	def apoyarSobreUnLado(self,image):
		pass


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Handle image path')
	parser.add_argument('--path',  type=str,  help='Path of the image to process')
	args = parser.parse_args()

	image_path = args.path
	print("Image path: ", image_path)

	# Instantiate 
	my_perspective = Perspective(extremosDeOrigen = [[0,0], [200,0], [0,200],[200,200]]) # RANDOM POINTS  p1, p2, p3, p4

	# Transform the image
	transformado = my_perspective.transformar(image_path, height = 0)

	# Enmarcar 
	enmarcado = my_perspective.enmarcar(transformado)
	
	# Load original image
	original_image = cv2.imread(image_path)

	# Mostrar

	# Resite original image to fill in the screen
	original_image_resized = cv2.resize(original_image, (320, 240))
	cv2.imshow('Original', original_image_resized)

	# Mostrar enmarcado image
	cv2.imshow('Enmarcado', enmarcado)

	# Press "q" to exit
	cv2.waitKey(0)

	cv2.destroyAllWindows()




