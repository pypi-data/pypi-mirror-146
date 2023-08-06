
x1 = ["","z","u","p","k","f","a"]
x2 = ["","v","q","l","g","b"]
x3 = ["","w","r","m","h","c"]
x4 = ["","x","s","n","i","d"]
x5 = ["","y","t","o","j","e"]


y1 = ["","z","","","",""]
y2 = ["","u","v","w","x","y"]
y3 = ["","p","q","r","s","t"]
y4 = ["","k","l","m","n","o"]
y5 = ["","f","g","h","i","j"]
y6 = ["","a","b","c","d","e"]



def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 


final_code = []


# name = input("Enter your text:")

def encode(plain_text):
	for i in plain_text:
		if i in y1:
			if i in x1:
				final_code.append(str(y1.index(i))+","+str(x1.index(i)))
		if i in y2:
			if i in x1:
				final_code.append(str(y2.index(i))+","+str(x1.index(i)))
			if i in x2:
				final_code.append(str(y2.index(i))+","+str(x2.index(i)))
			if i in x3:
				final_code.append(str(y2.index(i))+","+str(x3.index(i)))
			if i in x4:
				final_code.append(str(y2.index(i))+","+str(x4.index(i)))
			if i in x5:
				final_code.append(str(y2.index(i))+","+str(x5.index(i)))


		if i in y3:
			if i in x1:
				final_code.append(str(y3.index(i))+","+str(x1.index(i)))
			if i in x2:
				final_code.append(str(y3.index(i))+","+str(x2.index(i)))
			if i in x3:
				final_code.append(str(y3.index(i))+","+str(x3.index(i)))
			if i in x4:
				final_code.append(str(y3.index(i))+","+str(x4.index(i)))
			if i in x5:
				final_code.append(str(y3.index(i))+","+str(x5.index(i)))


		if i in y4:
			if i in x1:
				final_code.append(str(y4.index(i))+","+str(x1.index(i)))
			if i in x2:
				final_code.append(str(y4.index(i))+","+str(x2.index(i)))
			if i in x3:
				final_code.append(str(y4.index(i))+","+str(x3.index(i)))
			if i in x4:
				final_code.append(str(y4.index(i))+","+str(x4.index(i)))
			if i in x5:
				final_code.append(str(y4.index(i))+","+str(x5.index(i)))
		if i in y5:
			if i in x1:
				final_code.append(str(y5.index(i))+","+str(x1.index(i)))
			if i in x2:
				final_code.append(str(y5.index(i))+","+str(x2.index(i)))
			if i in x3:
				final_code.append(str(y5.index(i))+","+str(x3.index(i)))
			if i in x4:
				final_code.append(str(y5.index(i))+","+str(x4.index(i)))
			if i in x5:
				final_code.append(str(y5.index(i))+","+str(x5.index(i)))
		if i in y6:
			if i in x1:
				final_code.append(str(y6.index(i))+","+str(x1.index(i)))
			if i in x2:
				final_code.append(str(y6.index(i))+","+str(x2.index(i)))
			if i in x3:
				final_code.append(str(y6.index(i))+","+str(x3.index(i)))
			if i in x4:
				final_code.append(str(y6.index(i))+","+str(x4.index(i)))
			if i in x5:
				final_code.append(str(y6.index(i))+","+str(x5.index(i)))

	decode = {
		"1":"A",
		"2":"B",
		"3":"C",
		"4":"D",
		"5":"E",
		"6":"F",
		"7":"G",
		"8":"H",
		"9":"I",
		"10":"J",
		"11":" ",
	}

	alpha = []

	for code in final_code:
		x = decode[str(code.split(",")[0])]
		y = decode[str(code.split(",")[1])]
		alpha.append(x+y)

	return listToString(alpha)




def decode(encoded_text):
	string = encoded_text
	x1 = [" ","z","u","p","k","f","a"]
	x2 = [" ","v","q","l","g","b"," "," "]
	x3 = [" ","w","r","m","h","c"," "," "]
	x4 = [" ","x","s","n","i","d"," "," "]
	x5 = [" ","y","t","o","j","e"," "," "]


	y1 = [" ","z"," "," "," "," "," "," "," "," "]
	y2 = [" ","u","v","w","x","y"," "," "," "]
	y3 = [" ","p","q","r","s","t"," "," "," "]
	y4 = [" ","k","l","m","n","o"," "," "," "]
	y5 = [" ","f","g","h","i","j"," "," "," "]
	y6 = [" ","a","b","c","d","e"," "," "," "]



	decode = {
		"A":"1",
		"B":"2",
		"C":"3",
		"D":"4",
		"E":"5",
		"F":"6",
		"G":"7",
		"H":"8",
		"I":"9",
		"J":"10",
		" ":"11",
	}

	plain = []
	alpha = []
	for i in string:
		code = decode[i]
		plain.append(code)
		alpha.append(i)



	# print(plain)

	final_main_plain_text = []

	def GOD(x,y):
		mix_alpha_1 = []
		mix_alpha_2 = []
		mix_alpha_1.append(y1[x])
		mix_alpha_1.append(y2[x])
		mix_alpha_1.append(y3[x])
		mix_alpha_1.append(y4[x])
		mix_alpha_1.append(y5[x])
		mix_alpha_1.append(y6[x])

		mix_alpha_2.append(x1[y])
		mix_alpha_2.append(x2[y])
		mix_alpha_2.append(x3[y])
		mix_alpha_2.append(x4[y])
		mix_alpha_2.append(x5[y])

		for same_string in mix_alpha_1:
			if same_string in mix_alpha_2:
				# print(same_string)
				final_main_plain_text.append(same_string)
			else:
				pass



	main_cordinats = []

	def new_way(x,y):
		# print(x+","+y)
		main_cordinats.append(x+","+y)

	def listToString(s): 
	    
	    # initialize an empty string
	    str1 = "" 
	    
	    # traverse in the string  
	    for ele in s: 
	        str1 += ele  
	    
	    # return string  
	    return str1 



	x = []
	y = []

	for i in range(len(plain)):
		if i%2 == 0:
			x.append(plain[i])
		else:
			y.append(plain[i])


	# print(x)
	# print(y)

	for k in range(len(x)):
		GOD(int(x[0]),int(y[0]))
		x.pop(0)
		y.pop(0)


	data = listToString(final_main_plain_text)
	return data

