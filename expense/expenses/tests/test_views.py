from django.urls import reverse


def test_add_expense_view_unauthenticated_user(db, client):
    """
    Accessing expense add view with an unauthenticated user will return 302
    """

    res = client.get(reverse("expenses:add"))

    assert res.status_code == 302


def test_add_expense_view_authenticated_user(db, authenticated_client):
    """
    Accessing expense add view with an authenticated user will return 200
    """
    res = authenticated_client.get(reverse("expenses:add"))

    assert res.status_code == 200


def test_add_expense_view_valid_expense_form(db, authenticated_client, user_data):
    """
    add_expense_view should redirect user to dashboard if expense form is valid, with no image uploaded
    """
    res = authenticated_client.post(
        reverse("expenses:add"),
        data={
            "amount": 10,
            "description": "Test",
            "category": user_data["expense_categories"].slug,
            "from_account": user_data["account"].slug,
        },
    )

    assert res.status_code == 302


def test_add_expense_view_invalid_expense_form(db, authenticated_client):
    """
    add_expense_view should return 400 if the form data is not valid, with no image uploaded
    """
    res = authenticated_client.post(
        reverse("expenses:add"),
        data={"amount": "abc", "description": "Test"},
    )
    assert res.status_code == 400
    assert (
        "You don&#x27;t have enough balance in None account. Available balance is 0."
        in res.content.decode()
    )


def test_add_expense_view_invalid_expense_and_invalid_image_form(
    db,
    authenticated_client,
):
    """
    add_expense_view should return 400 if the
    - expense form data is not valid
    - image form data is not valid
    """
    with open("expense/expenses/tests/testfiles/file.txt", "rb") as text_file:
        res = authenticated_client.post(
            reverse("expenses:add"),
            data={
                "amount": "abc",
                "description": "Test",
                "image": text_file,
            },
        )
    assert res.status_code == 400

    res_content = res.content.decode()
    assert (
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        in res_content
    )
    assert (
        "You don&#x27;t have enough balance in None account. Available balance is 0."
        in res_content
    )


def test_add_expense_view_valid_expense_and_invalid_image_form(
    db,
    authenticated_client,
    user_data,
):
    """
    add_expense_view should return 400 if the
    - expense form data is valid
    - image form data is not valid
    """
    with open("expense/expenses/tests/testfiles/file.txt", "rb") as text_file:
        res = authenticated_client.post(
            reverse("expenses:add"),
            data={
                "amount": 10,
                "description": "Test",
                "category": user_data["expense_categories"].slug,
                "from_account": user_data["account"].slug,
                "image": text_file,
            },
        )
    assert res.status_code == 400
    assert (
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        in res.content.decode()
    )


def test_add_expense_view_invalid_expense_and_valid_image_form(
    db,
    authenticated_client,
    user_data,
):
    """
    add_expense_view should return 400 if the
    - expense form data is valid
    - image form data is not valid
    """
    with open("expense/expenses/tests/testfiles/validpng.png", "rb") as image:
        res = authenticated_client.post(
            reverse("expenses:add"),
            data={
                "amount": 10,
                "description": "Test",
                "category": user_data["expense_categories"].slug,
                "image": image,
            },
        )
    assert res.status_code == 400
    assert (
        "You don&#x27;t have enough balance in None account. Available balance is 0."
        in res.content.decode()
    )


def test_add_expense_view_valid_expense_and_valid_image_form(
    db,
    authenticated_client,
    user_data,
):
    with open("expense/expenses/tests/testfiles/validpng.png", "rb") as image:
        res = authenticated_client.post(
            reverse("expenses:add"),
            data={
                "amount": 10,
                "description": "Test",
                "category": user_data["expense_categories"].slug,
                "from_account": user_data["account"].slug,
                "image": image,
            },
        )
    assert res.status_code == 302
