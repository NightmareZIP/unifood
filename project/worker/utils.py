from .models import Worker


def get_worker(user_id):
    worker = Worker.objects.get(user_id=user_id)
    worker_id = worker.id
    return worker_id
