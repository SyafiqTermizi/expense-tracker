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
    add_expense_view should redirect user to dashboard if expense form is valid
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
    add_expense_view should return 400 if the form data is not valid
    """
    res = authenticated_client.post(
        reverse("expenses:add"),
        data={"amount": "abc", "description": "Test"},
    )
    assert res.status_code == 400


# def test_add_expense_view_invalid_expense_and_invalid_image_form(
#     db,
#     authenticated_client,
#     user_data,
# ):
#     res = authenticated_client.post(
#         reverse("expenses:add"),
#         data={
#             "amount": "invalid_data",
#             "description": "Test",
#             "category": user_data["expense_categories"].slug,
#             "from_account": user_data["account"].slug,
#             "image": "invalid_data",
#         },
#     )
#     assert res.status_code == 400


# def test_add_expense_view_valid_expense_and_invalid_image_form(
#     db,
#     authenticated_client,
#     user_data,
# ):
#     assert f"{dir(authenticated_client)}" == "v"
#     res = authenticated_client.post(
#         reverse("expenses:add"),
#         data={
#             "amount": 10,
#             "description": "Test",
#             "category": user_data["expense_categories"].slug,
#             "from_account": user_data["account"].slug,
#             "image": 1,
#         },
#     )
#     assert res.status_code == 400


def test_add_expense_view_valid_expense_and_valid_image_form(
    db,
    authenticated_client,
    image,
    user_data,
):
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
