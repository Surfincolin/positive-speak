# Run some test
import GDPHelper
import pandas as pd
import datetime
# import SentimentHelper


def test_FileInfoClass():
	file = '../data/USCPI_1774-2018.csv'
	file_info = GDPHelper.FileInfo(file, 'Year', 'CPI')
	assert type(file_info) == GDPHelper.FileInfo
	assert type(file_info.filename) == str
	assert type(file_info.date) == str
	assert type(file_info.data) == str

def test_GDP():
	cpifile = '../data/USCPI_1774-2018.csv'
	gdpfile = '../data/USGDP_1790-2018.csv'
	cpifile_info = GDPHelper.FileInfo(cpifile, 'Year', 'CPI')
	gdpfile_info = GDPHelper.FileInfo(gdpfile, 'Year', 'Nominal GDP (million of Dollars)')

	gdp = GDPHelper.GDP(cpifile_info, gdpfile_info)

	assert type(gdp) == GDPHelper.GDP
	assert type(gdp.gdp_data) == pd.DataFrame

def test_convert_year_int_to_date():
	d = GDPHelper.convert_year_int_to_date(1970)
	assert type(d) == datetime.datetime

test_FileInfoClass()
test_GDP()
test_convert_year_int_to_date()