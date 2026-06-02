"""Données des sociétés fictives utilisées pour les documents générés."""
import random
from dataclasses import dataclass, field
from typing import Optional
from faker import Faker

_fake = Faker("fr_FR")


@dataclass
class Company:
    name: str
    address: str
    city: str
    zip_code: str
    phone: str
    email: str
    siret: str
    tva_number: str
    logo_path: Optional[str] = None  # chemin vers assets/logos/<fichier>
    primary_color: tuple = field(default_factory=lambda: (0.1, 0.3, 0.6))   # RGB 0-1


def random_company(seed: Optional[int] = None) -> Company:
    """Génère une société fictive aléatoire."""
    rng = random.Random(seed)
    fake = Faker("fr_FR")
    if seed is not None:
        Faker.seed(seed)

    colors = [
        (0.10, 0.28, 0.58),  # bleu professionnel
        (0.70, 0.12, 0.12),  # rouge bordeaux
        (0.08, 0.47, 0.28),  # vert forêt
        (0.40, 0.20, 0.60),  # violet
        (0.80, 0.45, 0.00),  # orange
    ]

    return Company(
        name=fake.company(),
        address=fake.street_address(),
        city=fake.city(),
        zip_code=fake.postcode(),
        phone=fake.phone_number(),
        email=fake.company_email(),
        siret="".join([str(rng.randint(0, 9)) for _ in range(14)]),
        tva_number=f"FR{rng.randint(10,99)}{rng.randint(100_000_000, 999_999_999)}",
        primary_color=rng.choice(colors),
    )
