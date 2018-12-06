import xlrd

# Open the workbook and define the worksheet
book = xlrd.open_workbook("pytest.xls")
sheet = book.sheet_by_name("source")

for r in range(1, sheet.nrows):
		product = sheet.cell(r,).value
		customer = sheet.cell(r,1).value
		rep = sheet.cell(r,2).value
		date = sheet.cell(r,3).value
		actual = sheet.cell(r,4).value
		expected = sheet.cell(r,5).value
		open = sheet.cell(r,6).value
		closed = sheet.cell(r,7).value
		city = sheet.cell(r,8).value


		# Assign values from each row
		values = (product, customer, rep, date, actual, expected, open, closed, city)


columns = str(sheet.ncols)
rows = str(sheet.nrows)
