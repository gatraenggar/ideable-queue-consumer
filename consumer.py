from decouple import config
from email_sender import send_email
import os, pika, sys

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config("HOST"))
    )

    channel = connection.channel()

    channel.exchange_declare(exchange='email_confirmation', exchange_type='direct')
    channel.queue_declare(queue='email_confirmation', durable=True)

    channel.queue_bind(
        exchange='email_confirmation',
        queue='email_confirmation',
        routing_key='email_confirmation',
    )

    def callback(ch, method, prop, body):
        print("sending to", body.decode())
        send_email(body.decode())
        print("done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue='email_confirmation',
        on_message_callback=callback,
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

