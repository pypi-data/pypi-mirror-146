import time
import api


def create_account(master_account, amount=10**24):
    account_id = "testtest-%s.test.near" % int(time.time() * 10000)
    master_account.create_account(account_id, master_account.signer.public_key,
                                  amount)
    signer = api.signer.Signer(account_id, master_account.signer.key_pair)
    account = api.account.Account(master_account.provider, signer, account_id)
    return account
