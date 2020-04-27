import keyboard
import os
import random
from colorama import Fore, Style
import telebot
from telebot import types

class Snake:
	def __init__(self, map_size=10, colored=True, FRUIT="$", SNAKE_BODY="s", SNAKE_HEAD="S", EMPTY="0", SPACE_AFTER_EMPTY=" "):
		self.map_size = map_size
		self.snake_pos = [[2, 0], [1, 0], [0, 0]]
		self.fruit = [0, 0, 0]
		self.colored = colored
		self.FRUIT = FRUIT
		self.SNAKE_BODY = SNAKE_BODY
		self.SNAKE_HEAD = SNAKE_HEAD
		self.EMPTY = EMPTY
		self.SPACE_AFTER_EMPTY = SPACE_AFTER_EMPTY

	def define_map(self):
		game_map = []

		for x in range(self.map_size):
			game_map.append([])

		for x in range(self.map_size):
			for y in range(self.map_size):
				game_map[x].append(self.EMPTY)

		return game_map

	def spawn_fruit(self):
		while True:
			rx = random.randrange(0, self.map_size)
			ry = random.randrange(0, self.map_size)

			for i in range(len(self.snake_pos)):
				if rx == self.snake_pos[i][0] and ry == self.snake_pos[i][1]:
					brk = False
					break
				else:
					brk = True

			if brk:
				self.fruit[0] = rx
				self.fruit[1] = ry
				self.fruit[2] = 1
				break

	def move_snake(self):

		while True:
			xdir = 0
			ydir = 0

			if keyboard.is_pressed("up_arrow"):
				ydir = -1
				break
			if keyboard.is_pressed("right_arrow"):
				xdir = 1
				break
			if keyboard.is_pressed("down_arrow"):
				ydir = 1
				break
			if keyboard.is_pressed("left_arrow"):
				xdir = -1
				break

		for i in range(len(self.snake_pos)):

			if i == 0:
				previous_pos = [self.snake_pos[i][0], self.snake_pos[i][1]]
				self.snake_pos[i][0] += xdir
				self.snake_pos[i][1] += ydir

				if self.snake_pos[i][0] == self.snake_pos[-1][0] and self.snake_pos[i][1] == self.snake_pos[-1][1]:
					return True

			else:
				pos = previous_pos
				previous_pos = [self.snake_pos[i][0], self.snake_pos[i][1]]
				self.snake_pos[i][0] = pos[0]
				self.snake_pos[i][1] = pos[1]

		if self.snake_pos[0][0] == self.fruit[0] and self.snake_pos[0][1] == self.fruit[1] and self.fruit[2] == 1:
			self.snake_pos.append([])
			self.snake_pos[-1].append(previous_pos[0])
			self.snake_pos[-1].append(previous_pos[1])

			if len(self.snake_pos) == self.map_size ** 2:
				return "win"
			else:
				self.fruit[2] = 0

		if (self.snake_pos[0][0] > self.map_size - 1 or self.snake_pos[0][0] < 0 
			or self.snake_pos[0][1] > self.map_size - 1 or self.snake_pos[0][1] < 0):
			return True

		for i in range(len(self.snake_pos)):
			for ii in range(len(self.snake_pos)):
				if self.snake_pos[i] == self.snake_pos[ii] and i != ii:
					return True

		return False

	def draw_game_map(self, selfgame_map):	
		os.system("cls")

		for i in range(len(self.snake_pos)):
			sx = self.snake_pos[i][0]
			sy = self.snake_pos[i][1]
			if i == 0:
				selfgame_map[sx][sy] = self.SNAKE_HEAD
			else:
				selfgame_map[sx][sy] = self.SNAKE_BODY

		if self.fruit[2] == 1:
			selfgame_map[self.fruit[0]][self.fruit[1]] = self.FRUIT

		for y in range(self.map_size):
			for x in range(self.map_size):
				prnt = str(selfgame_map[x][y]) + self.SPACE_AFTER_EMPTY

				if self.colored:
					if self.SNAKE_HEAD in prnt or self.SNAKE_BODY in prnt:
						prnt = Fore.GREEN + prnt
					elif self.FRUIT in prnt:
						prnt = Fore.RED + prnt
					else:
						print(Style.RESET_ALL, end="")

				if x != self.map_size - 1:
					print(prnt, end="")
				else:
					print(prnt)

		print(Style.RESET_ALL)

	def play(self):
		while True:
			game_map_ = self.define_map()

			if self.fruit[2] == 0:
				self.spawn_fruit()

			self.draw_game_map(selfgame_map=game_map_)
			var = self.move_snake()

			if var == True:
				print("----- GAME OVER -----")
				print(f"Your score: {str(len(self.snake_pos))}")
				break
			elif var == "win":
				print("----- YOU WON -----")
				break



class TelegramSnake:
	def __init__(self, bot, mes, buttons, map_size=10, FRUIT="$", SNAKE_BODY="s", SNAKE_HEAD="S", EMPTY="0", SPACE_AFTER_EMPTY=" "):
		self.map_size = map_size
		self.snake_pos = [[2, 0], [1, 0], [0, 0]]
		self.fruit = [0, 0, 0]
		self.FRUIT = FRUIT
		self.SNAKE_BODY = SNAKE_BODY
		self.SNAKE_HEAD = SNAKE_HEAD
		self.EMPTY = EMPTY
		self.SPACE_AFTER_EMPTY = SPACE_AFTER_EMPTY
		self.bot = bot
		self.mes = mes
		self.buttons = buttons

	def define_map(self):
		game_map = []

		for x in range(self.map_size):
			game_map.append([])

		for x in range(self.map_size):
			for y in range(self.map_size):
				game_map[x].append(self.EMPTY)

		return game_map

	def spawn_fruit(self):
		while True:
			rx = random.randrange(0, self.map_size)
			ry = random.randrange(0, self.map_size)

			for i in range(len(self.snake_pos)):
				if rx == self.snake_pos[i][0] and ry == self.snake_pos[i][1]:
					brk = False
					break
				else:
					brk = True

			if brk:
				self.fruit[0] = rx
				self.fruit[1] = ry
				self.fruit[2] = 1
				break

	def move_snake(self, xdir, ydir):
		print(self.snake_pos)
		for i in range(len(self.snake_pos)):

			if i == 0:
				previous_pos = [self.snake_pos[i][0], self.snake_pos[i][1]]
				self.snake_pos[i][0] += xdir
				self.snake_pos[i][1] += ydir

				if self.snake_pos[i][0] == self.snake_pos[-1][0] and self.snake_pos[i][1] == self.snake_pos[-1][1]:
					return True
			else:
				pos = previous_pos
				previous_pos = [self.snake_pos[i][0], self.snake_pos[i][1]]
				self.snake_pos[i][0] = pos[0]
				self.snake_pos[i][1] = pos[1]

		if self.snake_pos[0][0] == self.fruit[0] and self.snake_pos[0][1] == self.fruit[1] and self.fruit[2] == 1:
			self.snake_pos.append([])
			self.snake_pos[-1].append(previous_pos[0])
			self.snake_pos[-1].append(previous_pos[1])

			if len(self.snake_pos) == self.map_size ** 2:
				return "win"
			else:
				self.fruit[2] = 0

		if (self.snake_pos[0][0] > self.map_size - 1 or self.snake_pos[0][0] < 0 
			or self.snake_pos[0][1] > self.map_size - 1 or self.snake_pos[0][1] < 0):
			return True

		for i in range(len(self.snake_pos)):
			for ii in range(len(self.snake_pos)):
				if self.snake_pos[i] == self.snake_pos[ii] and i != ii:
					return True

		return False

	def draw_game_map(self, selfgame_map):	
		os.system("cls")
		mp = ""

		for i in range(len(self.snake_pos)):
			sx = self.snake_pos[i][0]
			sy = self.snake_pos[i][1]
			if i == 0:
				selfgame_map[sx][sy] = self.SNAKE_HEAD
			else:
				selfgame_map[sx][sy] = self.SNAKE_BODY

		if self.fruit[2] == 1:
			selfgame_map[self.fruit[0]][self.fruit[1]] = self.FRUIT

		for y in range(self.map_size):
			for x in range(self.map_size):
				mp += str(selfgame_map[x][y]) + self.SPACE_AFTER_EMPTY
			mp += "\n"

		return(mp)


	def play(self):
		game_map_ = self.define_map()
		draw = self.draw_game_map(selfgame_map=game_map_)
		self.bot.edit_message_text(draw, chat_id=self.mes.chat.id, message_id=self.mes.message_id)
		while True:
			game_map_ = self.define_map()


			if self.fruit[2] == 0:
				self.spawn_fruit()

			@self.bot.callback_query_handler(func=lambda call: True)
			def handle_query(call):
				if call.data == "right":
					var = self.move_snake(xdir=1, ydir=0)
				if call.data == "left":
					var = self.move_snake(xdir=-1, ydir=0)
				if call.data == "up":
					var = self.move_snake(xdir=0, ydir=-1)
				if call.data == "down":
					var = self.move_snake(xdir=0, ydir=1)

				draw = self.draw_game_map(selfgame_map=game_map_)
				self.bot.edit_message_text(draw, chat_id=self.mes.chat.id, message_id=self.mes.message_id)
				print("yes")

				if var == True:
					print("----- GAME OVER -----")
					print(f"Your score: {str(len(self.snake_pos))}")
					self.bot.edit_message_text("Zjebałeś", chat_id=self.buttons.chat.id, message_id=self.buttons.message_id)
				elif var == "win":
					print("----- YOU WON -----")
					self.bot.edit_message_text("Wygrałeś", chat_id=self.buttons.chat.id, message_id=self.buttons.message_id)

s = Snake()
s.play()