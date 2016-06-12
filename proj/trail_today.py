import imdb
import csv
import wikipedia

def toMillion(txt):
	try :
		li = txt.split(' ')
		if len(li) > 1:
			if li[-1] == 'million' or li[-1] == "illion":
				return float(li[0])
			elif li[-1] == 'billion':
				return float(li[0])*1000
			else:
				return '?'
				# print li[0]
				# print ('neither million or billion')
		# else:
		# 	return float(li[0])/1000
	except:
		return '?'


movy = open('filtered.csv', 'rb')
mvOrgLst = []
mvLst = []
mvYearLst = []
mvMvLst = []
movies = csv.reader(movy, delimiter='|',quotechar=' ')
output_writer = csv.writer(file('output1.csv', 'wb'))
movies.next()
array = []
for row in movies:
	temp = row[0].split(',')
	array.append(list(temp))
for x in array:
	mvOrgLst.append(x[1])
	mvLst.append(x[1] + ' (film)')
	mvYearLst.append(x[1] + ' (' + str(x[6]) + ' film)')
	mvMvLst.append(x[1] + ' (movie)')
count = 0


def parseBoxBudget(av, i):
		text = av.html()
		# Find Box Office
		box = ''
		budget = ''
		foundBo = text.find('<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Box office</th><td style="line-height:1.3em;">\n')
		boxStart = foundBo + 113
		foundBu = text.find('<th scope="row" style="white-space:nowrap;padding-right:0.65em;">Budget</th><td style="line-height:1.3em;">\n')
		budgetStart = foundBu + 109
		if foundBu != -1 or foundBo != -1:
			xBo = boxStart
			while text[xBo] != unicode('<'):
				if ord(text[xBo]) == 8211:
					box += ' '
				elif text[xBo] == '&':
					xBo += 6
					box += ' '
				else:
					box += text[xBo]
				xBo += 1
			xBu = budgetStart
			while text[xBu] != unicode('<'):
				if ord(text[xBu]) == 8211 or text[xBu] == '-' or ord(text[xBu]) == 8212:
					budget += ' '
				elif text[xBu] == '&':
					xBu += 6
					budget += ' '
				else:
					budget += text[xBu]
				xBu += 1
			print mv + ': ' + str(toMillion(box)) + 'bo|bu' + str(toMillion(budget))
			output_writer.writerow([i, mvOrgLst[i], toMillion(box), toMillion(budget)])
		else:

			print mv + ': ' + '??' + ' box|budget ' + '??'

			output_writer.writerow([i, mvOrgLst[i], '?', '?'])

for i in xrange(0, 1000):
	mv = mvLst[i]
	if count > 100:
		break
	print 'Processing movie ' + str(i)

	try:
		av = wikipedia.page(mv, auto_suggest=False, redirect=False)
	except:
		print mv + " (with film) has error"
		try:
			mv = mvMvLst[i]
			av = wikipedia.page(mv, auto_suggest=False, redirect=False)
		except:
			print mv + " (with movie) has error"
			try:
				mv = mvYearLst[i]
				av = wikipedia.page(mv, auto_suggest=False, redirect=False)
			except:
				print mv + " (with year film) has error"
				try:
					
					mv = mvOrgLst[i]
					av = wikipedia.page(mv, auto_suggest=False, redirect=False)
				except:
					print mv + " (original) has error"
					print 'all four failed'
					output_writer.writerow([i, mvOrgLst[i], '?', '?'])
				else:
					print 'original successful'
					parseBoxBudget(av, i)
			else:
				print 'year film successful'
				parseBoxBudget(av, i)
		else:
			print 'movie successful'
			parseBoxBudget(av, i)
	else:
		print 'film successful'
		parseBoxBudget(av, i)


