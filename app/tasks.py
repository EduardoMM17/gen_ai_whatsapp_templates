from app.core.celery import celery

@celery.task(acks_late=True)
def test(raw_conversations, tickets_info):
    print("Raw conversations: ", raw_conversations)
    print("Tickets info: ", tickets_info)