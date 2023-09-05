from rest_framework.exceptions import APIException


class ReviewAlreadyExists(APIException):
    status_code = 400
    default_detail = 'Вы уже оставили отзыв к этому произведению.'
    default_code = 'review_already_exists'