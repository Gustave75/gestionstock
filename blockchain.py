from web3 import Web3

# Connexion au réseau Sepolia
w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/aiTvxLzzSxtMVDutW-vFj"))

# Adresse du contrat déployé
CONTRAT_ADRESSE = "0xE37164091FB4F388CF83476DF853fC549D52cdcb"

# ABI minimal du contrat (juste la fonction dont on a besoin)
CONTRAT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "produitId", "type": "string"},
            {"internalType": "string", "name": "action", "type": "string"}
        ],
        "name": "enregistrerAction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Wallet pour signer les transactions
PRIVATE_KEY = "0x8bd531bc4ad6e725d33c2192ed093cf0c75eabb621a9578e79a169940504c5ff"
compte = w3.eth.account.from_key(PRIVATE_KEY)

contrat = w3.eth.contract(address=CONTRAT_ADRESSE, abi=CONTRAT_ABI)

def enregistrer_sur_blockchain(produit_id: str, action: str):
    """Enregistre une action sur un produit dans la blockchain."""
    try:
        tx = contrat.functions.enregistrerAction(produit_id, action).build_transaction({
            "from": compte.address,
            "nonce": w3.eth.get_transaction_count(compte.address),
            "gas": 100000,
            "gasPrice": w3.eth.gas_price
        })
        tx_signe = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(tx_signe.raw_transaction)
        return tx_hash.hex()
    except Exception as e:
        print(f"Erreur blockchain : {e}")
        return None
