from django.urls import reverse

from expense.expenses.models import Expense, Image


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
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

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

    # new expense should be created
    assert Expense.objects.count() > initial_expense_count

    # no image should be created, because no image is uploaded
    assert Image.objects.count() == initial_image_count


def test_add_expense_view_invalid_expense_form(db, authenticated_client):
    """
    add_expense_view should return 400 if the form data is not valid, with no image uploaded
    """
    initial_expense_count = Expense.objects.count()

    res = authenticated_client.post(
        reverse("expenses:add"),
        data={"amount": "abc", "description": "Test"},
    )
    assert res.status_code == 400
    assert (
        "You don&#x27;t have enough balance in None account. Available balance is 0."
        in res.content.decode()
    )

    # no new expense should be created
    assert Expense.objects.count() == initial_expense_count


def test_add_expense_view_invalid_expense_and_invalid_image_form(
    db,
    authenticated_client,
):
    """
    add_expense_view should return 400 if the
    - expense form data is not valid
    - image form data is not valid
    """
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

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

    assert Expense.objects.count() == initial_expense_count
    assert Image.objects.count() == initial_image_count


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
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

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

    # no new data should be created if either of the form is not valid
    assert Expense.objects.count() == initial_expense_count
    assert Image.objects.count() == initial_image_count


def test_add_expense_view_invalid_expense_and_valid_image_form(
    db,
    authenticated_client,
    user_data,
):
    """
    add_expense_view should return 400 if the
    - expense form data is invalid
    - image form data is valid
    """
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

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

    # no new data should be created if either of the form is not valid
    assert Expense.objects.count() == initial_expense_count
    assert Image.objects.count() == initial_image_count


def test_add_expense_view_valid_expense_and_valid_image_form(
    db,
    authenticated_client,
    user_data,
):
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

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

    assert Expense.objects.count() > initial_expense_count
    assert Image.objects.count() > initial_image_count
