from app.core.celery import celery


@celery.task(acks_late=True)
def test(tickets_info):
    print("Tickets info: ", tickets_info)
