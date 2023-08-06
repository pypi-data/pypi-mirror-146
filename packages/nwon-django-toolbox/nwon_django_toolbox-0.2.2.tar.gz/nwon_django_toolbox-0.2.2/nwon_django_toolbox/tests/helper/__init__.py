from nwon_django_toolbox.tests.celery import (
    check_latest_task,
    check_number_of_created_tasks,
    check_task_has_been_enqueued,
    clean_all_celery_messages,
    create_celery_folder,
    get_path_to_celery_folder,
)
from nwon_django_toolbox.tests.helper.random_image import (
    get_path_to_random_image,
    get_random_image,
)
from nwon_django_toolbox.tests.helper.random_temporary_file import (
    get_random_tempfile_path,
)


def _base_name_from_model(model: ModelType[Model]) -> str:
    return _base_name_from_model_class(model.__class__)


def _base_name_from_model_class(model_class: Type[Model]) -> str:
    return model_class.__name__.lower()


__all__ = [
    "clean_all_celery_messages",
    "create_celery_folder",
    "get_path_to_celery_folder",
    "get_path_to_random_image",
    "get_random_image",
    "get_random_tempfile_path",
    "check_latest_task",
    "check_task_has_been_enqueued",
    "check_number_of_created_tasks",
]
