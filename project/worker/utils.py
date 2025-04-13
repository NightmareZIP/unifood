from .models import Worker


def get_worker(user_id):
    user = user_id
    worker = Worker.objects.get(user_id=user)
    worker_id = worker.id
    return worker_id
