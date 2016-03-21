import LeadPriceCalendar as LPC
import json
cal = LPC.LeadPriceCalendar()

cal.origin('ord')
cal.destination('yyz')
cal.lengthofstay([7, 9, 6, 7, 8])

# Return the JSON response, independent responses are also available from LPC's methods
print cal.call()
with open('leadpricecal_data.txt', 'w') as outfile:
			json.dump(cal.call(), outfile, sort_keys = True, indent = 4,
		ensure_ascii=False)
var = cal.call()
print var