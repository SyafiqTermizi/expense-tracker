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
    assert res.json()["errors"]["amount"][0]["code"] == "invalid"
    assert res.json()["errors"]["amount"][0]["message"] == "Enter a number."

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

    assert res.json()["errors"]["amount"][0]["code"] == "invalid"
    assert res.json()["errors"]["amount"][0]["message"] == "Enter a number."

    assert res.json()["errors"]["image"][0]["code"] == "invalid_image"
    assert (
        res.json()["errors"]["image"][0]["message"]
        == "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
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
    assert res.json()["errors"]["image"][0]["code"] == "invalid_image"
    assert (
        res.json()["errors"]["image"][0]["message"]
        == "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
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
        res.json()["errors"]["__all__"][0]["message"]
        == "You don't have enough balance in None account. Available balance is 0."
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


def test_update_expense_view_valid_expense_form(
    db,
    authenticated_client,
    user_expense,
):
    initial_expense_count = Expense.objects.count()

    res = authenticated_client.post(
        reverse("expenses:update", kwargs={"slug": user_expense.slug}),
        data={"description": "new description", "category": user_expense.category.slug},
    )

    assert res.status_code == 302

    updated_expense = Expense.objects.get(slug=user_expense.slug)

    assert updated_expense.slug == user_expense.slug

    # only description should be updated
    assert updated_expense.description != user_expense.description
    assert updated_expense.category.pk == user_expense.category.pk

    # no new expense should be created
    assert Expense.objects.count() == initial_expense_count


def test_update_expense_view_invalid_expense_form(
    db,
    authenticated_client,
    user_expense,
):
    initial_expense_count = Expense.objects.count()

    res = authenticated_client.post(
        reverse("expenses:update", kwargs={"slug": user_expense.slug}),
        data={"description": "new description", "category": "invalid category"},
    )

    assert res.status_code == 400
    assert (
        "Select a valid choice. That choice is not one of the available choices."
        in res.content.decode()
    )

    updated_expense = Expense.objects.get(slug=user_expense.slug)

    # nothing should change since the form is invalid
    assert updated_expense.slug == user_expense.slug
    assert updated_expense.description == user_expense.description
    assert updated_expense.category.pk == user_expense.category.pk

    # no new expense should be created
    assert Expense.objects.count() == initial_expense_count


def test_update_expense_view_valid_expense_form_valid_image_form(
    db,
    authenticated_client,
    user_expense_with_image,
):
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

    with open("expense/expenses/tests/testfiles/validpng2.png", "rb") as image:
        res = authenticated_client.post(
            reverse("expenses:update", kwargs={"slug": user_expense_with_image.slug}),
            data={
                "description": "new description",
                "category": user_expense_with_image.category.slug,
                "image": image,
            },
        )

    assert res.status_code == 302

    updated_expense = Expense.objects.get(slug=user_expense_with_image.slug)

    assert updated_expense.slug == user_expense_with_image.slug

    # only description should be updated
    assert updated_expense.description != user_expense_with_image.description
    assert updated_expense.category.pk == user_expense_with_image.category.pk

    # no new expense should be created
    assert Expense.objects.count() == initial_expense_count

    # no new image should be created
    assert Image.objects.count() == initial_image_count


def test_update_expense_view_invalid_expense_form_invalid_image_form(
    db,
    authenticated_client,
    user_expense_with_image,
):
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

    with open("expense/expenses/tests/testfiles/file.txt", "rb") as text_file:
        res = authenticated_client.post(
            reverse("expenses:update", kwargs={"slug": user_expense_with_image.slug}),
            data={
                "description": "new description",
                "category": "invalid_slug",
                "image": text_file,
            },
        )

    res_content = res.content.decode()
    assert res.status_code == 400
    assert (
        "Select a valid choice. That choice is not one of the available choices."
        in res_content
    )
    assert (
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        in res_content
    )

    updated_expense = Expense.objects.get(slug=user_expense_with_image.slug)

    assert updated_expense.slug == user_expense_with_image.slug

    # expense should not be updated since the forms are invalid
    assert updated_expense.description == user_expense_with_image.description
    assert updated_expense.category.pk == user_expense_with_image.category.pk

    # no new expense should be created since the form is invalid
    assert Expense.objects.count() == initial_expense_count

    # no new image should be created since the form is invalid
    assert Image.objects.count() == initial_image_count


def test_update_expense_view_valid_expense_form_invalid_image_form(
    db,
    authenticated_client,
    user_expense_with_image,
):
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

    with open("expense/expenses/tests/testfiles/file.txt", "rb") as text_file:
        res = authenticated_client.post(
            reverse("expenses:update", kwargs={"slug": user_expense_with_image.slug}),
            data={
                "description": "new description",
                "category": user_expense_with_image.category.slug,
                "image": text_file,
            },
        )

    res_content = res.content.decode()
    assert res.status_code == 400
    assert (
        "Select a valid choice. That choice is not one of the available choices."
        not in res_content
    )
    assert (
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        in res_content
    )

    updated_expense = Expense.objects.get(slug=user_expense_with_image.slug)

    assert updated_expense.slug == user_expense_with_image.slug

    # expense should not be updated since the forms are invalid
    assert updated_expense.description == user_expense_with_image.description
    assert updated_expense.category.pk == user_expense_with_image.category.pk

    # no new expense should be created since the form is invalid
    assert Expense.objects.count() == initial_expense_count

    # no new image should be created since the form is invalid
    assert Image.objects.count() == initial_image_count


def test_update_expense_view_invalid_expense_form_valid_image_form(
    db,
    authenticated_client,
    user_expense_with_image,
):
    initial_expense_count = Expense.objects.count()
    initial_image_count = Image.objects.count()

    with open("expense/expenses/tests/testfiles/validpng.png", "rb") as image:
        res = authenticated_client.post(
            reverse("expenses:update", kwargs={"slug": user_expense_with_image.slug}),
            data={
                "description": "new description",
                "category": "invalid_slug",
                "image": image,
            },
        )

    res_content = res.content.decode()
    assert res.status_code == 400
    assert (
        "Select a valid choice. That choice is not one of the available choices."
        in res_content
    )
    assert (
        "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        not in res_content
    )

    updated_expense = Expense.objects.get(slug=user_expense_with_image.slug)

    assert updated_expense.slug == user_expense_with_image.slug

    # expense should not be updated since the form is invalid
    assert updated_expense.description == user_expense_with_image.description
    assert updated_expense.category.pk == user_expense_with_image.category.pk

    # no new expense should be created since the form is invalid
    assert Expense.objects.count() == initial_expense_count

    # no new image should be created since the form is invalid
    assert Image.objects.count() == initial_image_count
