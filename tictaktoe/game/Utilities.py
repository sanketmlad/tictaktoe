import MySQLdb
import string
import random
import re

class Utilities:
	def __init__(self):
		self.conn = None
		self.dbcursor = None

	def connect(self):
		self.conn = MySQLdb.connect('localhost', 'root', 'guest123', 'tictaktoe')
		self.dbcursor = self.conn.cursor()

	def disconnect(self):
		self.conn.close()

	def hello(self):
		return " this is test keyword hello"

	def insert_preference(self,preference):
		query = "update user_preference set preference = '%s' where id=1" %preference
		self.execute_query(query)

	def first_move(self):
		#corner_number=[1,3,7,9]
		#x = random.choice(corner_number)
		#query = "update box_number set value = 'X' where id='%d'"%x
		query = "update box_number set value = 'X' where id=1"
		self.execute_query(query)

	def game_progress(self):
		return "Game is in Progress"
			
	def execute_query(self,query):	
		self.connect()
		try:
			self.dbcursor.execute(query)
			self.conn.commit()
		except MySQLdb.Error, e:
			sys.exit("Error! %d: %s" % (e.args[0], e.args[1]))
		self.disconnect()	

	def reset_game(self):
		query = "update box_number set value = 'N'"			
		self.execute_query(query)

	def call_to_ai_for_new_value(self,user_input):
		if not re.match("^\d$",user_input):
			return "Please enter number in between 1-9"
		user_input = float(user_input.strip())
		user_input = int(user_input)
		query = "select id from box_number where value='N'"
		query_array = "select value from box_number"
		self.connect()
		self.dbcursor.execute(query)
		n_value_id_list = []
		raw_op= self.dbcursor.fetchall()
		for i in raw_op:
			n_value_id_list.append(i[0])
		print n_value_id_list
		self.disconnect()
		user_variable = self.get_preference()
		if user_input not in n_value_id_list:
			return "Please Enter in empty spaces"
		query_update = "update box_number set value='%s' where id=%d"%(user_variable,user_input)
		self.execute_query(query_update)
		self.connect()
		self.dbcursor.execute(query_array)
		array_value = []
		raw_op= self.dbcursor.fetchall()
		for i in raw_op:
			array_value.append(i[0])
		print array_value
		self.disconnect()
		return self.do_ai_move(array_value,user_variable)		
		

	def do_ai_move(self,array_value,user_variable):
		'''
		'''
		if self.is_complete(array_value,user_variable)=='yes':
			return "User Wins"
		grid = [[0 for x in xrange(3)] for x in xrange(3)]
		column1=['N','N','N'] 
		column2=['N','N','N'] 
		column3=['N','N','N'] 
		row1=array_value[:3]
		row2=array_value[3:6]
		row3=array_value[6:9]
		for i in xrange(3):
			column1[i] = array_value[i*3]
		for i in xrange(3):
			column2[i] = array_value[i*3+1]
		for i in xrange(3):
			column3[i] = array_value[i*3+2]
		print row1,row2,row3,column1,column2,column3
		x_positions = [i for i, j in enumerate(array_value) if j == "X"]
		y_positions = [i for i, j in enumerate(array_value) if j == "Y"]
		n_positions = [i for i, j in enumerate(array_value) if j == "N"]
		if n_positions == "" or n_positions == []:
			return "Match Drawn please start again"
		n_count = array_value.count('N')
		filled_places = 9 - n_count
		ai_entry = 10
		ai_variable = 'Y'
		if user_variable == 'Y':
			ai_variable = 'X'
			dummy_array_value = array_value
			for i in n_positions:
				dummy_array_value[i]=ai_variable
				if(self.is_complete(dummy_array_value,ai_variable)=='yes'):
					ai_entry = i+1
					break
				dummy_array_value[i]='N'
			if ai_entry != 10:
				pass
			elif filled_places == 2:
				if array_value[4]=='Y':
					ai_entry = 9
				elif row1.count('Y')==1:
					ai_entry = 7
				else:
					ai_entry = 3
			elif (filled_places == 4) and (array_value[4]!=user_variable):
				if row1.count(user_variable)==1 and column1.count(user_variable)==1:
					ai_entry = 9
				if row3.count(user_variable)==1 and column1.count(user_variable)==1:
					ai_entry = 3
				if row1.count(user_variable)==1 and column3.count(user_variable)==1:
					ai_entry = 7
				
			else :
				ai_dummy_array_value = array_value
				u_dummy_array_value = array_value
				for i in n_positions:
					ai_dummy_array_value[i]=ai_variable
			 		u_dummy_array_value[i]=user_variable
					if(self.is_complete(ai_dummy_array_value,ai_variable)=='yes'):
						ai_entry = i+1
						break
					elif(self.is_complete(u_dummy_array_value,user_variable)=='yes'):
						ai_entry = i+1
						break
					ai_dummy_array_value[i]='N'
					u_dummy_array_value[i]='N'
				
		else:
			dummy_array_value = array_value
			for i in n_positions:
				dummy_array_value[i]=ai_variable
				if(self.is_complete(dummy_array_value,ai_variable)=='yes'):
					ai_entry = i+1
					break
				dummy_array_value[i]='N'
			if ai_entry != 10:
				pass
			elif filled_places == 1:
				if array_value[4] == 'N':
					ai_entry = 5
				else:
					ai_entry = 1
			elif filled_places == 3:
				ai_location = array_value.index('Y')
				if ai_location == 4:
					if x_positions == [0,8] or x_positions == [2,6] or row2.count('X')==2:
						ai_entry = 2
					elif x_positions in [[0,2],[6,8],[0,6],[2,8]]:
						ai_entry = sum(x_positions)/2 +1
					elif (row1.count('X')==1) and (column3.count('X')==1) and (row1!=column3):
						ai_entry = 3
					elif (row3.count('X')==1) and (column1.count('X')==1) and (row3!=column1):
						ai_entry = 7
					elif (row1.count('X')==1) and (column1.count('X')==1) and (row1!=column1):
						ai_entry = 1
					elif (row3.count('X')==1) and (column3.count('X')==1) and (row3!=column3):
						ai_entry = 9
					elif (row1.count('X')==2):
						ai_entry = row1.index('N') +1
					elif (row3.count('X')==2):
						ai_entry = row3.index('N') +7
					elif (column1.count('X')==2):
						ai_entry = column1.index('N')*3 +1
					elif (column3.count('X')==2):
						ai_entry = column3.index('N')*3 +3
					else:
						ai_entry = 4
				else:
					if (row2.count('X')==2):
						ai_entry = row2.index('N') + 4
					elif (column2.count('X')==2):
						ai_entry = column2.index('N')*3 +2
					elif (array_value[2]=='X'):
						ai_entry = 7
					elif (array_value[6]=='X') or (array_value[8]=='X'):
						ai_entry = 3

				print ai_entry
			elif filled_places == 5 or filled_places == 7:
				u_dummy_array_value = array_value
				for i in n_positions:
			 		u_dummy_array_value[i]=user_variable
					if(self.is_complete(u_dummy_array_value,user_variable)=='yes'):
						ai_entry = i+1
						break
					u_dummy_array_value[i]='N'
				if ai_entry == 10:
					n_positions = [i for i, j in enumerate(array_value) if j == "N"]
					ai_entry = n_positions[0]+1
		
		
		query_update = "update box_number set value='%s' where id=%d"%(ai_variable,ai_entry)
		self.execute_query(query_update)
		array_value[ai_entry-1]=ai_variable
		if self.is_complete(array_value,ai_variable)=='yes':
			return "Computer Wins"
		n_positions = [i for i, j in enumerate(array_value) if j == "N"]
		if n_positions == "" or n_positions == []:
			return "Match Drawn please start again"
		else:
			return "Game is in progress"
						

	def is_complete(self,array_value,entry):
		if ((array_value[0]==array_value[1]==array_value[2]==entry) or
		(array_value[3]==array_value[4]==array_value[5]==entry) or
		(array_value[6]==array_value[7]==array_value[8]==entry) or
		(array_value[0]==array_value[3]==array_value[6]==entry) or
		(array_value[1]==array_value[4]==array_value[7]==entry) or
		(array_value[2]==array_value[5]==array_value[8]==entry) or
		(array_value[0]==array_value[4]==array_value[8]==entry) or
		(array_value[2]==array_value[4]==array_value[6]==entry)):
			return 'yes'
		
		

	def get_preference(self):
		query = "select preference from user_preference where id=1"
		self.connect()
		self.dbcursor.execute(query)
		preference =  self.dbcursor.fetchone()
		self.disconnect()
		return preference[0]

