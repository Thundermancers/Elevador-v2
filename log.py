import serial, time
import numpy as np

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_RATE = 115200

def main():
	ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
	mode = 1
	print('Modo programador? Y\\n')
	answer = input()
	if answer == 'n':
		mode = 0
	
	while True:
		reading = ser.readline()
		reading = str(reading)
		arr = reading.split("_")[1:-1]
		out = []
		
		if not len(arr) == 7:
			continue
		else:
			for s in arr:
				s = s.split(' ')
				if not len(s) == 2: 
					continue				
				out.append( [s[0], s[1]] )

		if not len(out) == 7:
			continue

		if mode :
			for s in out:
				if len(s[1]) == 1:
					print(s[0] , ord(s[1])-ord('0'))
				else :
					print(s[0] , s[1] )
		else:

			# 1000 - STOP_ELE
			# 0000 - STOP
			# 0101 - DES_ELE
			# 0111 - RISE_ELE
			# 0001 - DES_OUT
			# 0011 - RISE_OUT

			'''
				E 0000
				OS 0000
				L 0
				O 0
				S 0000
				DC :
				FC 0
			'''			

			if int(out[4][1],2)&1 :
				print( 'Parado', end='')

			else :
				if int(out[4][1],2)&2 :
					print('Subindo para ', end='')
					print( int(np.log2(int(out[4][1],2))), end='' )
				else:
					print('Descendo para ', end='')
					v = int(out[4][1],2)
					l = int(out[2][1])
					bitmask = (1<<l) - 1
					v = v&bitmask
					print( int(np.log2(v)), end='' )				

				print(' pela chamada do ')
				if int(out[0][1],2):
					print('elevador')
				else
					print('andar')
			
			pass
		

if __name__ == "__main__":
	main()