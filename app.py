# -*- coding: utf-8 -*-
import telebot
import requests
import json
from firebase import firebase
from firebase import jsonutil

bot = telebot.TeleBot("190173866:AAGDaAEXGCwYpxJ6y_NrfA6vAWFH2eequyw")
database = firebase.FirebaseApplication('https://mdkinokz.firebaseio.com/', authentication=None)

def getCities():
	data = {'k':'PU08TR1D'}
	cities_request = requests.post('http://ws.kino.kz/cities.data', data = data)
	cities_data = json.loads(cities_request.text)
	cities = cities_data['data']
	return cities

def getCinemas(city_id):
	data = {'k':'PU08TR1D', 'city':city_id}
	cinemas_request = requests.post('http://ws.kino.kz/cinemas.data', data = data)
	cinemas_data = json.loads(cinemas_request.text)
	cinemas = cinemas_data['data']
	return cinemas

@bot.message_handler(commands=['start'])
def get_city(message):
	city_markup = telebot.types.ReplyKeyboardMarkup(True, True)
	for city in CITIES:
		city_markup.row("/city "+city['name'])

	bot.send_message(message.from_user.id, "Приветик, с какого Вы города?", reply_markup = city_markup)

@bot.message_handler(commands=['city'])
def save_city(message):
	city_name = message.text[6:]
	for city in CITIES:
		if city['name'] == city_name:
			city_id = city['id']
			break

	new_user = {'id':message.chat.id,'first_name':message.chat.first_name, 'last_name':message.chat.last_name,'username':message.chat.username, 'city':city_name, 'city_id':city_id}
	# need to check before save, need to implement
	result = database.post_async('/users', new_user)

	cinemas = getCinemas(city_id)
	cinema_markup = telebot.types.ReplyKeyboardMarkup(True, True)
	for cinema in cinemas:
		cinema_markup.row('/cinema '+cinema['name'])

	bot.send_message(message.from_user.id, "Ваш город %s" % city_name.encode('utf-8'))
	bot.send_message(message.from_user.id, "Пожалуйста, Выберите кинотеатр ", reply_markup = cinema_markup)

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

CITIES = getCities()
bot.polling()