from threading import Timer
from time import time
import json

from RequestsModule.Request import *


class RequestsProcessor(object):

    prefix = 'requests_processor'

    def __init__(self, networking):

        self.networking = networking
        self.answer_generating_callbacks = {}
        self.answer_received_callbacks = {}
        self.non_processed_requests = []

        self.process_requests()

    def send_request(self, peer, module_prefix, request_prefix, question_data):
        request = Request(peer, self.prefix, module_prefix, request_prefix, question_data)
        self.non_processed_requests.append(request)
        return request

    def register_answer_generator_callback(self, module_prefix, request_type, callback):
        if not module_prefix in self.answer_generating_callbacks:
            self.answer_generating_callbacks[module_prefix] = {}
        self.answer_generating_callbacks[module_prefix][request_type] = callback

    def register_answer_received_callback(self, module_prefix, request_type, callback):
        if not module_prefix in self.answer_received_callbacks:
            self.answer_received_callbacks[module_prefix] = {}
        self.answer_received_callbacks[module_prefix][request_type] = callback

    def process_requests(self):
        update_timeout = 0.1

        new_non_processed_requests = []
        for request in self.non_processed_requests:
            if not request.answer_received:
                new_non_processed_requests.append(request)
        self.non_processed_requests = new_non_processed_requests

        for request in self.non_processed_requests:
            if request.question_sending_needed():
                print('sending message')
                self.networking.send_message(request.generate_question_message())
                request.question_sent()

        messages = self.networking.get_messages(self.prefix)
        for message in messages:
            print('received: ' + message.get_body())
            message_body_json = message.get_body()
            message_body = json.JSONDecoder().decode(message_body_json)
            if message_body['text']['request_question_answer'] == 'question':
                self.process_question(message.peer, message_body)
            for request in self.non_processed_requests:
                if message_body['text']['request_question_answer'] == 'answer':
                    is_answer = request.check_message_is_answer(message)
                    if is_answer:
                        self.answer_received_callbacks[message_body['text']['module_prefix']][message_body['text']['request_prefix']](request)
        timer = Timer(update_timeout, self.process_requests)
        timer.start()

    def process_question(self, peer, message_body):
        module_prefix = message_body['text']['module_prefix']
        request_prefix = message_body['text']['request_prefix']
        request_data = message_body['text']['request_data']
        answer = None
        if module_prefix in self.answer_generating_callbacks:
            if request_prefix in self.answer_generating_callbacks[module_prefix]:
                callback = self.answer_generating_callbacks[module_prefix][request_prefix]
                answer = callback(request_data)
        answer_message = {
            'request_question_answer': 'answer',
            'request_id': message_body['text']['request_id'],
            'module_prefix': module_prefix,
            'request_prefix': request_prefix,
            'request_data': answer
        }
        print('answering: ' + repr(answer_message))
        self.networking.send_message(Message(peer, prefix=self.prefix, text=answer_message))