'''
GDPHelper.py - This file helps build and adjust GDP data
'''
import pandas as pd
import datetime

class FileInfo:
	'''
	FileInfo is used to organize a csv data file name, and columns to process.
	'''
	def __init__(self, filename, time_col_name, data_col_name):
		'''
		Parameters
		----------
		filename: str
			The location of the file and where it is located.
		time_col_name: str
			String that matches the csv's date column title.
		data_col_name: str
			String that matches the csv's data column title.
		'''
		self.filename = filename
		self.date = time_col_name
		self.data = data_col_name

class GDP:
	'''
	GDP is used to crunch and hold GDP Growth data. The growth data is calculated from the consumer price index, so two csv files are used.
	'''
	def __init__(self, cpi_fileinfo, gdp_fileinfo):
		'''
		Parameters
		----------
		cpi_fileinfo: FileInfo
			Consumer Price Index file info.
		gdp_fileinfo: FileInfo
			GDP (Gross Domestic Product) file info.
		'''
		self.cpi_fileinfo = cpi_fileinfo
		self.gdp_fileinfo = gdp_fileinfo

		self.__calc_cpi_inflation()
		self.__calc_gdp_growth()
		self.gdp_data = self.__gdp_df[['date', 'growth']]


	def __calc_gdp_growth(self):
		df = pd.read_csv(self.gdp_fileinfo.filename)
		df = self.__cpi_df.merge(df)
		df = df.rename(columns = {
			self.gdp_fileinfo.date : 'date'
			})

		prev_gdp = None

		growth_rate = []
		inflation_gdp = zip(self.__cpi_df['inflation'],
			df[self.gdp_fileinfo.data])
		for inflation, gdp in inflation_gdp:
			gdp_f = float(gdp.replace(',', ''))

			if prev_gdp == None:
				growth_rate.append(0)
			else:
				if_amount = (inflation * prev_gdp) + prev_gdp
				growth = (gdp_f - if_amount) / if_amount
				growth_rate.append(growth)

			prev_gdp = gdp_f

		df['growth'] = growth_rate
		df['date'] = df['date'].apply(convert_year_int_to_date)
		self.__gdp_df = df

	def __calc_cpi_inflation(self):
		df = pd.read_csv(self.cpi_fileinfo.filename)

		prev_cpi = None

		inflation_rate = []
		for cpi in df[self.cpi_fileinfo.data]:
			if prev_cpi == None:
				inflation_rate.append(0)
			else:
				if_rate = (cpi - prev_cpi) / prev_cpi
				inflation_rate.append(if_rate)
			
			prev_cpi = cpi
						
		df['inflation'] = inflation_rate
		self.__cpi_df = df

def convert_year_int_to_date(i_int):
	return datetime.datetime(year=i_int,month=1,day=1)

"""
Checks answer to question to see if it should iterate 
to next question or stops asking questions.

Parameters
----------
ans: str
		The input from the user.
		
Returns
----------
return: bool
		Shows if answer matches expected input.
		
"""