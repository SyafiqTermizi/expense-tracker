from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

CURRENCIES = [
    ("ALL", "Albania Lek"),
    ("AFN", "Afghanistan Afghani"),
    ("ARS", "Argentina Peso"),
    ("AWG", "Aruba Guilder"),
    ("AUD", "Australia Dollar"),
    ("AZN", "Azerbaijan Manat"),
    ("BSD", "Bahamas Dollar"),
    ("BBD", "Barbados Dollar"),
    ("BYN", "Belarus Ruble"),
    ("BZD", "Belize Dollar"),
    ("BMD", "Bermuda Dollar"),
    ("BOB", "Bolivia Bolíviano"),
    ("BAM", "Bosnia and Herzegovina Convertible Mark"),
    ("BWP", "Botswana Pula"),
    ("BGN", "Bulgaria Lev"),
    ("BRL", "Brazil Real"),
    ("BND", "Brunei Darussalam Dollar"),
    ("KHR", "Cambodia Riel"),
    ("CAD", "Canada Dollar"),
    ("KYD", "Cayman Islands Dollar"),
    ("CLP", "Chile Peso"),
    ("CNY", "China Yuan Renminbi"),
    ("COP", "Colombia Peso"),
    ("CRC", "Costa Rica Colon"),
    ("HRK", "Croatia Kuna"),
    ("CUP", "Cuba Peso"),
    ("CZK", "Czech Republic Koruna"),
    ("DKK", "Denmark Krone"),
    ("DOP", "Dominican Republic Peso"),
    ("XCD", "East Caribbean Dollar"),
    ("EGP", "Egypt Pound"),
    ("SVC", "El Salvador Colon"),
    ("EUR", "Euro Member Countries"),
    ("FKP", "Falkland Islands (Malvinas) Pound"),
    ("FJD", "Fiji Dollar"),
    ("GHS", "Ghana Cedi"),
    ("GIP", "Gibraltar Pound"),
    ("GTQ", "Guatemala Quetzal"),
    ("GGP", "Guernsey Pound"),
    ("GYD", "Guyana Dollar"),
    ("HNL", "Honduras Lempira"),
    ("HKD", "Hong Kong Dollar"),
    ("HUF", "Hungary Forint"),
    ("ISK", "Iceland Krona"),
    ("INR", "India Rupee"),
    ("IDR", "Indonesia Rupiah"),
    ("IRR", "Iran Rial"),
    ("IMP", "Isle of Man Pound"),
    ("ILS", "Israel Shekel"),
    ("JMD", "Jamaica Dollar"),
    ("JPY", "Japan Yen"),
    ("JEP", "Jersey Pound"),
    ("KZT", "Kazakhstan Tenge"),
    ("KPW", "Korea (North) Won"),
    ("KRW", "Korea (South) Won"),
    ("KGS", "Kyrgyzstan Som"),
    ("LAK", "Laos Kip"),
    ("LBP", "Lebanon Pound"),
    ("LRD", "Liberia Dollar"),
    ("MKD", "Macedonia Denar"),
    ("MYR", "Malaysia Ringgit"),
    ("MUR", "Mauritius Rupee"),
    ("MXN", "Mexico Peso"),
    ("MNT", "Mongolia Tughrik"),
    ("MNT", "Moroccan-dirham"),
    ("MZN", "Mozambique Metical"),
    ("NAD", "Namibia Dollar"),
    ("NPR", "Nepal Rupee"),
    ("ANG", "Netherlands Antilles Guilder"),
    ("NZD", "New Zealand Dollar"),
    ("NIO", "Nicaragua Cordoba"),
    ("NGN", "Nigeria Naira"),
    ("NOK", "Norway Krone"),
    ("OMR", "Oman Rial"),
    ("PKR", "Pakistan Rupee"),
    ("PAB", "Panama Balboa"),
    ("PYG", "Paraguay Guarani"),
    ("PEN", "Peru Sol"),
    ("PHP", "Philippines Peso"),
    ("PLN", "Poland Zloty"),
    ("QAR", "Qatar Riyal"),
    ("RON", "Romania Leu"),
    ("RUB", "Russia Ruble"),
    ("SHP", "Saint Helena Pound"),
    ("SAR", "Saudi Arabia Riyal"),
    ("RSD", "Serbia Dinar"),
    ("SCR", "Seychelles Rupee"),
    ("SGD", "Singapore Dollar"),
    ("SBD", "Solomon Islands Dollar"),
    ("SOS", "Somalia Shilling"),
    ("KRW", "South Korean Won"),
    ("ZAR", "South Africa Rand"),
    ("LKR", "Sri Lanka Rupee"),
    ("SEK", "Sweden Krona"),
    ("CHF", "Switzerland Franc"),
    ("SRD", "Suriname Dollar"),
    ("SYP", "Syria Pound"),
    ("TWD", "Taiwan New Dollar"),
    ("THB", "Thailand Baht"),
    ("TTD", "Trinidad and Tobago Dollar"),
    ("TRY", "Turkey Lira"),
    ("TVD", "Tuvalu Dollar"),
    ("UAH", "Ukraine Hryvnia"),
    ("AED", "UAE-Dirham"),
    ("GBP", "United Kingdom Pound"),
    ("USD", "United States Dollar"),
    ("UYU", "Uruguay Peso"),
    ("UZS", "Uzbekistan Som"),
    ("VEF", "Venezuela Bolívar"),
    ("VND", "Viet Nam Dong"),
    ("YER", "Yemen Rial"),
    ("ZWD", "Zimbabwe Dollar"),
]


class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    username_validator = UnicodeUsernameValidator()

    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(
        "username",
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    currency = models.CharField(max_length=255, choices=CURRENCIES)

    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_absolute_url(self):
        return reverse("users:profile")
