from decouple import config
from email_sender import send_email
import os, pika, sys

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config("HOST"))
    )

    channel = connection.channel()

    channel.exchange_declare(exchange='service_logs', exchange_type='direct')
    
    services = [
        "email_confirmation",
        "workspace_invitation",
    ]

    for service_name in services:
        channel.queue_declare(queue=service_name, durable=True)
        channel.queue_bind(
            exchange='service_logs',
            queue=service_name,
            routing_key=service_name,
        )

        def callback(ch, method, prop, body):
            print("[service] %r to %r" % (method.routing_key, body.decode().split()[0]))
            send_email(body.decode(), method.routing_key)
            print("done")
            ch.basic_ack(delivery_tag = method.delivery_tag)

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=service_name,
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

