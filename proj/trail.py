import imdb
import csv
import wikipedia

def toMillion(txt):
    li = txt.split(' ')
    if len(li) > 1:
	    if li[-1] == 'million':
	        return float(li[0])
	    elif li[-1] == 'billion':
	        return float(li[0])*1000
	#     else:
	#     	print li[0]
	#     	print ('neither million or billion')
	# else:
	#    	print li[0]
	# 	print ('neither million or billion')

movy = open('filtered.csv', 'rb')
mvLst = []
movies = csv.reader(movy, delimiter='|',quotechar=' ')
output_writer = csv.writer(file('output.csv', 'wb'))
movies.next()
array = []
for row in movies:
	temp = row[0].split(',')
	array.append(list(temp))
for x in array:
	mvLst.append(x[1] + '(film)')
count = 0
mvLst[11] = 'Toy Story'
mvLst[12] = 'The Big Lebowski'
mvLst[16] = 'Star Wars: Episode I - The Phantom Menace'
mvLst[17] = 'Gladiator (2000 film)'
mvLst[22] = 'XXX (2002 film)'
mvLst[25] = 'Anchorman: The Legend of Ron Burgundy'
mvLst[28] = 'Star Wars: Episode III - Revenge of the Sith'
mvLst[33] = 'Casino Royale (2006 film)'
mvLst[36] = 'Iron Man (2008 film)'
mvLst[41] = 'Inglourious Basterds'
mvLst[46] = 'Zombieland'
mvLst[44] = 'Up (2009 film)'
mvLst[44] = 'Up (2009 film)'
mvLst[67] = 'In Time'



for mv in mvLst:
	if count > 100:
		break	
	print 'Processing ' + str(count)
	try:
		av = wikipedia.page(mv)

		count += 1
	except:
		print mv + " has error"
		output_writer.writerow([''])
	else:
		text = av.html()
		# Find Box Office
		box = ''
		budget = ''
		boxStart = text.find('<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Box office</th><td style="line-height:1.3em;">\n')+113
				
		x = boxStart
		while text[x] != unicode('<'):
			if ord(text[x]) == 8211:				
				box += ' '
			elif text[x] == '&':
				x += 6
				box += ' '
			else:
				box += text[x]
			x += 1
		
		budgetStart = text.find('<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Budget</th><td style="line-height:1.3em;">\n') + 109		
		x = budgetStart
		while text[x] != unicode('<'):
			if ord(text[x]) == 8211 or text[x] == '-':				
				budget += ' '
			elif text[x] == '&':
				x += 6
				budget += ' '
			else:
				budget += text[x]
			x += 1
		print mv + ': ' + budget

		output_writer.writerow([toMillion(box), toMillion(budget)])

# output_writer.close()



