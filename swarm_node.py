# -*- coding: utf-8 -*-
import iota

from config import SEED, PATH_LIB_DCURL

## Output transaction
TXN_TAG = 'TESTINGPYTHON'
TXN_OUTPUT_ADR = '9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC'
TXN_OUTPUT_VALUE = 90
TXN_MSG = 'HELLO'

## Input transaction
TXN_INPUT_ADR = 'INDTKDAH9GGWDAJDWQLWUKCIHSYNEFQUGVHOYWLZRYPEZIZYQHQJNDLDPCLWMMO9UAEZUWPHMWZRLWGOB'
TXN_INPUT_BALANCE = 100

## Unspent Address
UNSPENT_ADR = 'HWFZCLVY9RPTAWC9OIOSHXSWFIYMSYSYBHZER9BYZ9KUPUJTRUOLKSGISILWFCWJO9LNZOLWRCJMVDJGD'

## Configuration
TXN_SECURITY_LEVEL = 2

## Setting output transaction
print ("Setting output transaction ...")
tag = iota.Tag(TXN_TAG)
pt = iota.ProposedTransaction(
    address = iota.Address(TXN_OUTPUT_ADR),
    value = TXN_OUTPUT_VALUE,
    tag = tag,
    message = iota.TryteString(TXN_MSG)
)

print ("Proposing output transaction into bundle...")
pb = iota.ProposedBundle([pt])

## Setting intput transaction
print ("Setting input transaction...")
# pb.add_inputs([list])
# pb._create_input_transaction(addy)

addy = iota.Address(TXN_INPUT_ADR)
addy.balance = TXN_INPUT_BALANCE
addy.key_index = 2
addy.security_level = TXN_SECURITY_LEVEL
inputs = [
    iota.ProposedTransaction(
        address=addy,
        tag=tag,
        value=-addy.balance
    )
]

print ("Proposing intput transaction into bundle...")

for input in inputs:
    pb._transactions.append(input)
for _ in range(addy.security_level - 1):
    pb._transactions.append(iota.ProposedTransaction(
        address=addy,
        tag=tag,
        value=0
    ))

# send unspent inputs to
unspent = iota.Address(UNSPENT_ADR)
pb.send_unspent_inputs_to(unspent)

print ("Bundle finalize ...")

# This will get the bundle hash
pb.finalize()

print ("Signing...")
# If the transaction need sign, it will then sign-up the transaction
# to fill up signature fragements
kg = iota.crypto.signing.KeyGenerator(SEED)

# pb.sign_inputs(kg)
i = 0
while i < len(pb):
    txn = pb[i]
    if txn.value < 0:
        if txn.address.key_index is None or txn.address.security_level is None:
            raise ValueError
        # pb.sign_input_at(i, kg.get_key_for(txn.address))
        address_priv_key = kg.get_key_for(txn.address)

        # Fill in signature fragement
        # address_priv_key.sign_input_transactions(pb, i)
        from iota.crypto.signing import SignatureFragmentGenerator
        sfg = SignatureFragmentGenerator(address_priv_key, pb.hash)
        for j in range(address_priv_key.security_level):
            txn = pb[i + j]
            txn.signature_message_fragment = next(sfg)
        i += txn.address.security_level
    else:
        i += 1

# Now each transaction have their signature into bundle
# this is the end of the transaction construction.
# We can now propose the transaction to tangle
# At this moment, tips still not inside each transaction,
# and each transaction hash is not yet generated
trytes = pb.as_tryte_strings()

# Get tips by getTransactionsToApprove
# tips = getTransactionsToApprove()
trunk_hash = iota.Hash('')
branch_hash = iota.Hash('')

print ("Do POW...")
# Do PoW (attach to tangle)
prev_tx = None

for tx_tryte in trytes:
    print (tx_tryte)
    print ("\n\n\n")

    txn = iota.Transaction.from_tryte_string(tx_tryte)
    txn.trunk_transaction_hash = trunk_hash if prev_tx is None else prev_tx.hash
    txn.branch_transaction_hash = branch_hash if prev_tx is None else trunk_hash

    # Copy obsolete tag if tag field is empty
    if not txn.tag:
        txn.tag = txn.obsolete_tag

    # Copy timestamp
    txn.timestamp = None
    txn.timestamp_lower_bound = None
    txn.timestamp_upper_bound = None

    # Do the PoW for this transaction
    # pearlDiver.search(txn.as_trits(), min_weight_magniude, 0)

    # Validate PoW
    # transactionValidator.validate(txn.as_trits())
