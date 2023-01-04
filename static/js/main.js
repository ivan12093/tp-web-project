$(".btn-outline-success").on('click', function () {
    const object_type = $(this).data('type')
    const request = new Request(
        '/like',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'object_type=' + object_type + '&id=' + $(this).data('id')
        }
    )
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => $('#' + object_type + '-rating-' + $(this).data('id')).text(response_json.rating)
        )
    );
})

$(".btn-outline-danger").on('click', function () {
    const object_type = $(this).data('type')
    const request = new Request(
        '/dislike',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'object_type=' + object_type + '&id=' + $(this).data('id')
        }
    )
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => $('#' + object_type + '-rating-' + $(this).data('id')).text(response_json.rating)
        )
    );
})

$(".form-check-input").on('click', function () {
    const answer_id = $(this).data('id');
    const question_id = $('.question-btn').data('id');
    const correct = $(this).is(':checked');
    console.log(answer_id, question_id, correct);
    const request = new Request(
        '/correct',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'question_id=' + question_id + '&answer_id=' + answer_id + '&correct=' + correct
        }
    )
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => console.log(response_json)
        )
    );
})
