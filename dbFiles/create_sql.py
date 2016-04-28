#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Aku
# @Date:   2015-05-15 11:37:50
# @Last Modified by:   Aku
# @Last Modified time: 2015-05-15 13:52:42

from io import open
import json

with open("database.sql", 'w') as outfile, open('tags.json', 'r', encoding='utf-8') as data_file:
	data = json.load(data_file)
	for theme in data:
		outfile.write("INSERT INTO Theme (theme) VALUES ('" + theme.replace("'", "''") + "');\n")
		for category in data[theme]:
			select_theme = "(SELECT id from Theme t WHERE theme='" + theme + "')"
			outfile.write("INSERT INTO Category (id_theme, category) VALUES (" + select_theme + ", '" + category.replace("'", "''") + "');\n")
			for tag in data[theme][category]:
				select_category = "(SELECT id from Category c WHERE category='" + category + "')"
				tag = tag.replace("'", "''")
				outfile.write("INSERT INTO Tag (id_category, tag) VALUES (" + select_category + ", '" + tag + "');\n")

with open("database.sql", 'a') as outfile, open('itunes_data.json', 'r', encoding='utf-8') as data_file:
	data = json.load(data_file)
	for theme in data:
		outfile.write("INSERT INTO Theme (theme) VALUES ('" + theme.replace("'", "''") + "');\n")
		for category in data[theme]:
			select_theme = "(SELECT id from Theme t WHERE theme='" + theme + "')"
			outfile.write("INSERT INTO Category (id_theme, category) VALUES (" + select_theme + ", '" + category.replace("'", "''") + "');\n")
			for tag in data[theme][category]:
				select_category = "(SELECT id from Category c WHERE category='" + category + "')"
				tag = tag.replace("'", "''")
				outfile.write("INSERT INTO Tag (id_category, tag) VALUES (" + select_category + ", '" + tag + "');\n")

with open("database.sql", 'a') as outfile, open('giantbomb_data.json', 'r', encoding='utf-8') as data_file:
	data = json.load(data_file)
	for theme in data:
		outfile.write("INSERT INTO Theme (theme) VALUES ('" + theme.replace("'", "''") + "');\n")
		for category in data[theme]:
			select_theme = "(SELECT id from Theme t WHERE theme='" + theme + "')"
			outfile.write("INSERT INTO Category (id_theme, category) VALUES (" + select_theme + ", '" + category.replace("'", "''") + "');\n")
			for tag in data[theme][category]:
				select_category = "(SELECT id from Category c WHERE category='" + category + "')"
				tag = tag.replace("'", "''")
				outfile.write("INSERT INTO Tag (id_category, tag) VALUES (" + select_category + ", '" + tag + "');\n")