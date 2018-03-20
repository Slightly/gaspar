# -*- coding: utf-8 -*-
def EvaulateBMI(BMI):
	if BMI < 18.5:
		response = 'Alultáplált'
	elif BMI >= 18.5 and BMI < 25:
		response = 'Normális'
	elif BMI >= 25 and BMI < 30:
		response = 'Túlsúlyos'
	elif BMI >= 30:
		response = 'Kórosan túlsúlyos'
	return response

def CalculateBMI(height, weight):
	response = ''
	if height > 225 or height < 150 or weight > 200 or weight < 40:
		response = 'Irreális értéket adtál meg'
	else:
		height = float(height/100)
		heightCoeff = height**2
		BMI = weight / heightCoeff
		evaluation = EvaulateBMI(BMI)
		BMI = '%.1f' % BMI
		response = 'A BMI-d ' + BMI + ' [' + evaluation + ']'
	return response

def CalculateIdealWeight(height):
	if height > 130 and height < 225:
		response = ''
		min_w = 18.5*((height/100)**2)
		max_w = 25*((height/100)**2)+1
		response = 'Az ideális testsúlyod %d és %d kg között van.' % (min_w, max_w)
		return response
	else:
		return 'Irreális érték'
