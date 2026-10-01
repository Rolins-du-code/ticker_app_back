import uuid


def initier_paiement_mobile_money(montant, numero_telephone):
    """
    Stub temporaire : simule l'appel à l'API MTN MoMo / Orange Money.
    Retourne une référence unique, comme le ferait le vrai opérateur.

    Plus tard, cette fonction fera un vrai appel HTTP (requests.post(...))
    vers l'API de l'opérateur, avec le montant et le numéro du client,
    et retournera SA référence à eux (pas une générée ici).
    """
    reference = f"MOCK-{uuid.uuid4().hex[:10].upper()}"
    return {"reference": reference, "statut": "en_attente"}

def rembourser_mobile_money(montant, numero_telephone):
    """
    Stub temporaire : simule un remboursement via Mobile Money.
    À remplacer plus tard par le vrai appel API opérateur.
    """
    reference = f"REFUND-{uuid.uuid4().hex[:10].upper()}"
    return {"reference": reference, "statut": "reussie"}